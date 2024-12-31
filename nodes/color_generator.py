import torch
import numpy as np
from PIL import Image

class ColorGeneratorNode:
    """Node that generates a solid color image with specified dimensions."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 64, "max": 8192}),
                "hex_color": ("STRING", {"default": "#FF0000"})
            }
        }
    
    RETURN_TYPES = ("IMAGE", "LATENT")
    FUNCTION = "generate_color"
    CATEGORY = "image/color"

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB values."""
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        # Convert to RGB
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def generate_color(self, width, height, hex_color):
        """Generate a solid color image with the specified dimensions and color."""
        # Convert hex to RGB
        rgb_color = self.hex_to_rgb(hex_color)
        
        # Create PIL Image
        img = Image.new('RGB', (width, height), rgb_color)
        
        # Convert to numpy array and normalize to 0-1 range
        img_np = np.array(img).astype(np.float32) / 255.0
        
        # Create tensor for IMAGE output (batch, height, width, channels)
        img_tensor = torch.from_numpy(img_np).unsqueeze(0)
        
        # Create latent tensor (batch, channels, height/8, width/8)
        # Note: Standard SD latent space is 4 channels and 1/8 resolution
        latent_height = height // 8
        latent_width = width // 8
        
        # Create a normalized color tensor in latent space
        # This is a simplified representation - in practice, you might want to
        # use a more sophisticated method to convert RGB to latent space
        rgb_normalized = [x/255.0 for x in rgb_color]
        latent = torch.ones(1, 4, latent_height, latent_width, dtype=torch.float32)
        for i in range(3):
            latent[:, i, :, :] *= rgb_normalized[i]
        
        return (img_tensor, {"samples": latent})
        