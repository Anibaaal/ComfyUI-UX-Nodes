import torch
import torch.nn.functional as F

class BlurNode:
    """Node that applies Gaussian or bokeh blur to an image using GPU acceleration."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "blur_type": (["gaussian", "bokeh"],),
                "radius": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "sigma": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 20.0,
                    "step": 0.1
                }),
            },
            "optional": {
                "bokeh_shape": (["circular", "hexagonal"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_blur"
    CATEGORY = "image/filter"
    
    def gaussian_kernel(self, radius, sigma):
        """Generate 2D Gaussian kernel."""
        size = 2 * radius + 1
        x = torch.linspace(-radius, radius, size)
        kernel = torch.exp(-(x.view(-1, 1) ** 2 + x.view(1, -1) ** 2) / (2 * sigma ** 2))
        return kernel / kernel.sum()
    
    def bokeh_kernel(self, radius, shape="circular"):
        """Generate bokeh blur kernel."""
        size = 2 * radius + 1
        x = torch.linspace(-radius, radius, size)
        y = torch.linspace(-radius, radius, size)
        X, Y = torch.meshgrid(x, y, indexing='ij')
        R = torch.sqrt(X ** 2 + Y ** 2)
        
        if shape == "circular":
            kernel = (R <= radius).float()
        else:  # hexagonal
            # Approximate hexagonal shape
            hex_mask = ((abs(X) * 2 + abs(Y)) <= 2 * radius).float() * \
                      ((abs(X) + abs(Y) * 2) <= 2 * radius).float()
            kernel = hex_mask
            
        return kernel / kernel.sum()
    
    def apply_blur(self, image, blur_type="gaussian", radius=5, sigma=1.0, bokeh_shape="circular"):
        """Apply blur effect to the image."""
        # Ensure image is on GPU if available
        device = image.device
        
        # Generate appropriate kernel
        if blur_type == "gaussian":
            kernel = self.gaussian_kernel(radius, sigma)
        else:  # bokeh
            kernel = self.bokeh_kernel(radius, bokeh_shape)
        
        # Move kernel to same device as image
        kernel = kernel.to(device)
        
        # Prepare kernel for conv2d (out_channels, in_channels, height, width)
        kernel = kernel.view(1, 1, kernel.shape[0], kernel.shape[1])
        kernel = kernel.repeat(3, 1, 1, 1)  # Repeat for RGB channels
        
        # Reshape image for convolution
        # From: (batch, height, width, channels) to (batch, channels, height, width)
        x = image.permute(0, 3, 1, 2)
        
        # Apply separable convolution for Gaussian (faster)
        if blur_type == "gaussian":
            # Separate into vertical and horizontal passes
            kernel_1d = self.gaussian_kernel(radius, sigma).to(device)
            kernel_v = kernel_1d.view(1, 1, -1, 1).repeat(3, 1, 1, 1)
            kernel_h = kernel_1d.view(1, 1, 1, -1).repeat(3, 1, 1, 1)
            
            # Apply vertical then horizontal blur
            padding = radius
            x = F.conv2d(x, kernel_v, padding=(padding, 0), groups=3)
            x = F.conv2d(x, kernel_h, padding=(0, padding), groups=3)
        else:
            # Apply full 2D convolution for bokeh
            padding = radius
            x = F.conv2d(x, kernel, padding=padding, groups=3)
        
        # Reshape back to ComfyUI format
        # From: (batch, channels, height, width) to (batch, height, width, channels)
        x = x.permute(0, 2, 3, 1)
        
        return (x,)