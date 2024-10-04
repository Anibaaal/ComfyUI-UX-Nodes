import numpy as np
from scipy.interpolate import interp1d

class EasyResolutionPicker:
    NAME = "Easy Resolution Picker"

    def __init__(self):
        self.resolution_str = ""
        self.use_megapixels = False

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (
                    [
                        '1:1 (Square)', '5:4 (Standard)', '4:3 (Standard)', '3:2 (Classic)', '16:10 (Widescreen)',
                        '7:4 (IMAX)', '16:9 (HD)', '2:1 (Univisium)', '21:9 (Cinematic)', '2.35:1 (Anamorphic)',
                        '2.39:1 (Anamorphic)', '3:1 (Ultra-Wide)'
                    ],
                    {"default": "16:9 (HD)"}
                ),
                "orientation": (['Horizontal', 'Vertical'], {"default": "Horizontal"}),
                "length_type": (['Long Side', 'Short Side'], {"default": "Long Side"}),
                "side_length": ("INT", {"default": 1024, "min": 1, "step": 1}),
                "other_side": ("INT", {"default": 0, "min": 0, "step": 1}),
                "divisible_by": ("INT", {"default": 2, "min": 1, "step": 1}),
                "megapixels": ("FLOAT", {"default": 1.05, "min": 0.0001, "step": 0.01}),
            },
            "optional": {
                "use_megapixels": ("BOOLEAN", {"default": False}),
            }
        }

    @staticmethod
    def calculate_resolution(aspect_ratio, orientation, length_type, side_length, other_side, divisible_by, megapixels, use_megapixels):
        # Aspect ratio parsing
        ar_width, ar_height = map(int, aspect_ratio.split()[0].split(':'))

        # Calculate the other side based on the aspect ratio
        if length_type == 'Long Side':
            long_side = side_length
            short_side = int(long_side * ar_height / ar_width)
        else:
            short_side = side_length
            long_side = int(short_side * ar_width / ar_height)

        # Use megapixels to calculate the resolution if required
        if use_megapixels:
            total_pixels = int(megapixels * 1e6)
            ar_factor = (ar_width / ar_height) if length_type == 'Long Side' else (ar_height / ar_width)
            long_side = int(np.sqrt(total_pixels * ar_factor))
            short_side = int(long_side * ar_height / ar_width)

        # Swap width and height if the orientation is vertical
        if orientation == 'Vertical':
            long_side, short_side = short_side, long_side

        # Ensure the sides are divisible by the specified number
        width = (long_side if length_type == 'Long Side' else short_side) // divisible_by * divisible_by
        height = (short_side if length_type == 'Long Side' else long_side) // divisible_by * divisible_by

        # If 'other_side' is provided and greater than zero, use it
        if other_side > 0:
            if orientation == 'Vertical':
                height = other_side
            else:
                width = other_side

        # Generate the resolution string
        resolution_str = f"{width}x{height} ({aspect_ratio}, {orientation}, {length_type})"

        return width, height, resolution_str

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution_string")
    FUNCTION = "calculate_resolution"
    OUTPUT_NODE = False
    CATEGORY = "UX Nodes"


class BlockLayerStringGenerator:
    NAME = "Block Layer String Generator"
    
    def __init__(self):
        self.comma_separated_string = ""

    @classmethod
    def INPUT_TYPES(cls):
        double_blocks = {f"DOUBLE{i}": ("FLOAT", {"default": 1.0}) for i in range(19)}
        single_blocks = {f"SINGLE{i}": ("FLOAT", {"default": 1.0}) for i in range(38)}
        base_block = {"final_layer": ("FLOAT", {"default": 1.0})}

        return {
            "required": {**double_blocks, **single_blocks, **base_block},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("comma_separated_string",)
    FUNCTION = "generate_string"
    OUTPUT_NODE = False
    CATEGORY = "Custom Nodes"

    def generate_string(self, **kwargs):
        # Define the correct order of keys
        keys_order = (
            [f"DOUBLE{i}" for i in range(19)] +
            [f"SINGLE{i}" for i in range(38)] +
            ["final_layer"]
        )
        
        # Collect values in the defined order
        values = [str(kwargs[key]) for key in keys_order]
        
        # Join the values with commas
        self.comma_separated_string = ",".join(values)
        
        # Return the string as a tuple
        return (self.comma_separated_string,)

