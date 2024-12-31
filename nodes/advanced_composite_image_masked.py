import torch
import torch.nn.functional as F

class AdvancedCompositeImageMasked:
    """
    ComfyUI Custom Node for advanced image compositing.

    Allows for negative positioning, anchor point selection, and offset values 
    for precise and consistent image placement.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_image": ("IMAGE",),
                "overlay_image": ("IMAGE",),
                "mask": ("MASK",),
                "x_position": ("INT", {"default": 0, "step": 1}),
                "y_position": ("INT", {"default": 0, "step": 1}),
                "anchor": (["top-left", "top-center", "top-right",
                            "center-left", "center", "center-right",
                            "bottom-left", "bottom-center", "bottom-right"], 
                           {"default": "top-left"}),
                "x_offset": ("INT", {"default": 0, "step": 1}),
                "y_offset": ("INT", {"default": 0, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "composite"
    CATEGORY = "image/advanced"

    def composite(self, base_image, overlay_image, mask, x_position, y_position, anchor, x_offset, y_offset):
        """
        Composites the overlay image onto the base image using the mask,
        with advanced positioning options.
        """
        # Ensure tensors are on the same device
        base_image = base_image.to("cuda")
        overlay_image = overlay_image.to("cuda")
        mask = mask.to("cuda")

        # Convert images to float for manipulation
        base_image = base_image.float()
        overlay_image = overlay_image.float()

        # Expand mask dimensions if needed
        if mask.dim() == 2:  # Single channel mask (H, W)
            mask = mask.unsqueeze(0).unsqueeze(-1)  # (1, H, W, 1)
        elif mask.dim() == 3:  # Could be (B, H, W) or (H, W, 1)
            if mask.shape[-1] == 1:  # (H, W, 1)
                mask = mask.unsqueeze(0)  # (1, H, W, 1)
            else:
                mask = mask.unsqueeze(-1)  # (B, H, W, 1)

        # Handle batches
        batch_size = base_image.shape[0]
        composite_images = []

        for b in range(batch_size):
            base = base_image[b].unsqueeze(0)  # (1, C, H, W)
            overlay = overlay_image[b].unsqueeze(0)  # (1, C, H, W)
            m = mask[b % mask.shape[0]].unsqueeze(0)  # (1, 1, H, W)

            # Calculate anchor point offsets
            overlay_height, overlay_width = overlay.shape[2], overlay.shape[3]
            anchor_x, anchor_y = self.calculate_anchor_offset(overlay_width, overlay_height, anchor)

            # Calculate top-left corner for overlay placement
            paste_x = x_position + x_offset - anchor_x
            paste_y = y_position + y_offset - anchor_y

            # Pad overlay and mask for negative positions
            pad_left = max(0, -paste_x)
            pad_top = max(0, -paste_y)
            pad_right = max(0, paste_x + overlay_width - base.shape[3])
            pad_bottom = max(0, paste_y + overlay_height - base.shape[2])

            padded_overlay = F.pad(overlay, (0, 0, pad_left, pad_right, pad_top, pad_bottom), "constant", 0)
            padded_mask = F.pad(m, (pad_left, pad_right, pad_top, pad_bottom), "constant", 0)

            # Adjust paste coordinates after padding
            paste_x += pad_left
            paste_y += pad_top

            # Crop overlay and mask to fit base image
            crop_left = max(0, paste_x)
            crop_top = max(0, paste_y)
            crop_right = min(base.shape[3], paste_x + overlay_width)
            crop_bottom = min(base.shape[2], paste_y + overlay_height)

            crop_overlay = padded_overlay[:, :, crop_top:crop_bottom, crop_left:crop_right]
            crop_mask = padded_mask[:, :, crop_top:crop_bottom, crop_left:crop_right]

            # Ensure mask is the same size as overlay
            crop_mask = crop_mask.expand(crop_overlay.shape)

            # Composite images
            base_crop = base[:, :, crop_top:crop_bottom, crop_left:crop_right]
            composite_crop = base_crop * (1 - crop_mask) + crop_overlay * crop_mask

            # Place composite crop back into the base image
            base[:, :, crop_top:crop_bottom, crop_left:crop_right] = composite_crop
            composite_images.append(base)

        return (torch.cat(composite_images, dim=0),)

    def calculate_anchor_offset(self, width, height, anchor):
        """Calculates anchor point offset."""
        if anchor == "top-left":
            return 0, 0
        elif anchor == "top-center":
            return width // 2, 0
        elif anchor == "top-right":
            return width, 0
        elif anchor == "center-left":
            return 0, height // 2
        elif anchor == "center":
            return width // 2, height // 2
        elif anchor == "center-right":
            return width, height // 2
        elif anchor == "bottom-left":
            return 0, height
        elif anchor == "bottom-center":
            return width // 2, height
        elif anchor == "bottom-right":
            return width, height
        else:
            return 0, 0  # Default to top-left
