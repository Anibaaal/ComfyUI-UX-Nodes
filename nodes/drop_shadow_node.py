import torch
import torch.nn.functional as F
import numpy as np

class DropShadowNode:
    """Node that composites a foreground over a background with configurable drop shadow."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "foreground": ("IMAGE",),
                "background": ("IMAGE",),
                "mask": ("MASK",),  # Changed from IMAGE to MASK
                "shadow_blur": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 100,
                    "step": 1
                }),
                "shadow_opacity": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
                "offset_x": ("INT", {
                    "default": 10,
                    "min": -200,
                    "max": 200,
                    "step": 1
                }),
                "offset_y": ("INT", {
                    "default": 10,
                    "min": -200,
                    "max": 200,
                    "step": 1
                }),
                "shadow_color": ("STRING", {
                    "default": "#000000",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_shadow"
    CATEGORY = "image/composite"

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB values normalized to 0-1."""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return [x/255.0 for x in rgb]

    def gaussian_kernel(self, radius, sigma=None):
        """Generate 2D Gaussian kernel."""
        if sigma is None:
            sigma = radius / 3
            
        size = 2 * radius + 1
        x = torch.linspace(-radius, radius, size)
        kernel = torch.exp(-(x.view(-1, 1) ** 2 + x.view(1, -1) ** 2) / (2 * sigma ** 2))
        return kernel / kernel.sum()

    def apply_gaussian_blur(self, x, radius):
        """Apply Gaussian blur using separable convolution."""
        if radius == 0:
            return x
            
        device = x.device
        kernel = self.gaussian_kernel(radius)
        kernel = kernel.to(device)
        
        # Prepare kernels for separable convolution
        kernel_v = kernel.view(1, 1, -1, 1)
        kernel_h = kernel.view(1, 1, 1, -1)
        
        padding = radius
        # Apply vertical then horizontal blur
        x = F.conv2d(x, kernel_v, padding=(padding, 0))
        x = F.conv2d(x, kernel_h, padding=(0, padding))
        
        return x

    def offset_tensor(self, x, offset_x, offset_y, target_size):
        """Offset a tensor by x and y pixels, ensuring output matches target size."""
        if offset_x == 0 and offset_y == 0:
            return x
            
        device = x.device
        b, c, h, w = target_size
        
        # Create translation matrix
        theta = torch.tensor([[1, 0, offset_x / (w/2)],
                            [0, 1, offset_y / (h/2)]], dtype=torch.float32)
        theta = theta.unsqueeze(0).repeat(b, 1, 1).to(device)
        
        # Create grid for target size
        grid = F.affine_grid(theta, target_size, align_corners=False)
        
        # Apply translation and ensure output size matches target
        return F.grid_sample(x, grid, align_corners=False, mode='bilinear')

    def resize_to_match(self, tensor, target_size):
        """Resize tensor to match target size."""
        if tuple(tensor.shape[-2:]) != tuple(target_size[-2:]):
            return F.interpolate(tensor, size=target_size[-2:], mode='bilinear', align_corners=False)
        return tensor

    def apply_shadow(self, foreground, background, mask, shadow_blur=10, 
                    shadow_opacity=0.5, offset_x=10, offset_y=10, 
                    shadow_color="#000000"):
        """Apply drop shadow and composite images."""
        device = foreground.device
        
        # Convert inputs to correct format for processing
        # From (batch, height, width, channels) to (batch, channels, height, width)
        fg = foreground.permute(0, 3, 1, 2)
        bg = background.permute(0, 3, 1, 2)
        
        # Handle mask differently since it's now a MASK type (already single channel)
        mask = mask.unsqueeze(1) if mask.dim() == 3 else mask
        
        # Resize all inputs to match background size
        target_size = bg.shape
        fg = self.resize_to_match(fg, target_size)
        mask = self.resize_to_match(mask, target_size)
        
        # Create shadow from mask
        shadow = mask.clone()
        
        # Offset shadow using target size to ensure consistent dimensions
        shadow = self.offset_tensor(shadow, offset_x, offset_y, target_size)
        
        # Blur shadow
        shadow = self.apply_gaussian_blur(shadow, shadow_blur)
        
        # Ensure shadow matches background size after all operations
        shadow = self.resize_to_match(shadow, target_size)
        
        # Apply shadow color and opacity
        shadow_rgb = torch.tensor(self.hex_to_rgb(shadow_color)).to(device)
        shadow_rgb = shadow_rgb.view(1, 3, 1, 1)
        shadow = shadow * shadow_opacity
        
        # Ensure proper channel expansion
        if shadow.shape[1] == 1:
            shadow = shadow.repeat(1, 3, 1, 1)
        shadow = shadow * shadow_rgb
        
        # Ensure mask has proper channels for compositing
        if mask.shape[1] == 1:
            mask = mask.repeat(1, 3, 1, 1)
            
        # Composite shadow onto background
        comp = bg * (1 - shadow) + shadow
        
        # Composite foreground
        comp = comp * (1 - mask) + fg * mask
        
        # Convert back to ComfyUI format
        # From (batch, channels, height, width) to (batch, height, width, channels)
        comp = comp.permute(0, 2, 3, 1).contiguous()
        
        return (comp,)
