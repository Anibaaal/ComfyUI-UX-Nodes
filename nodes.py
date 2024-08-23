import numpy as np
from scipy.interpolate import interp1d

class EasyResolutionPicker:
    NAME = "Easy Resolution Picker"
    
    def __init__(self):
        self.resolution_str = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (
                    [
                        '1:1',
                        '5:4',
                        '4:3',
                        '3:2',
                        '7:4',
                        '16:10',
                        '16:9',
                        '2:1'
                    ], { "default": "1:1" }),
                "orientation": (
                    [
                        'Horizontal',
                        'Vertical'
                    ], { "default": "Horizontal" }),
                "length_type": (
                    [
                        'Long Side',
                        'Short Side'
                    ], { "default": "Long Side" }),
                "side_length": ("INT", {
                    "default": 1024,
                    "min": 0,
                    "max": 1000000,
                    "step": 2
                }),
                "other_side": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 1000000,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution_string")
    FUNCTION = "calculate_resolution"
    OUTPUT_NODE = False
    CATEGORY = "UX Nodes"

    def calculate_resolution(self, aspect_ratio, orientation, length_type, side_length, other_side):
        aspect_ratios = {
            '1:1': (1, 1),
            '5:4': (5, 4),
            '4:3': (4, 3),
            '3:2': (3, 2),
            '7:4': (7, 4),
            '16:10': (16, 10),
            '16:9': (16, 9),
            '2:1': (2, 1)
        }

        ar_width, ar_height = aspect_ratios[aspect_ratio]

        if length_type == 'Long Side':
            long_side = side_length
            short_side = other_side if other_side != 0 else int(side_length * ar_height / ar_width)
        else:
            short_side = side_length
            long_side = other_side if other_side != 0 else int(side_length * ar_width / ar_height)

        if orientation == 'Horizontal':
            width, height = long_side, short_side
        else:
            width, height = short_side, long_side

        # Ensure dimensions are divisible by 2
        width = width - (width % 2)
        height = height - (height % 2)

        # Generate resolution string
        resolution_str = f"{width}x{height}"
        self.resolution_str = resolution_str

        # Return calculated values
        return width, height, resolution_str
