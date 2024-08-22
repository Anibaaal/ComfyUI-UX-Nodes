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
                    "min": 512,
                    "max": 3072,
                    "step": 2
                }),
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution_string")
    FUNCTION = "calculate_resolution"
    OUTPUT_NODE = False
    CATEGORY = "UX Nodes"

    def calculate_resolution(self, aspect_ratio, orientation, length_type, side_length):
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
            short_side = int(side_length * ar_height / ar_width)
        else:
            short_side = side_length
            long_side = int(side_length * ar_width / ar_height)

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



class SmoothCurveMergerFlux:
    NAME = "Smooth Curve Merger Flux"
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "curve1_points": ("STRING", {
                    "default": "0.0,0.1,0.25,0.5,0.75,0.9,1.0",
                    "multiline": False,
                }),
                "curve2_points": ("STRING", {
                    "default": "1.0,0.9,0.75,0.5,0.25,0.1,0.0",
                    "multiline": False,
                }),
                "adjustment_point": ("INT", {
                    "default": 19,
                    "min": 0,
                    "max": 57,
                    "step": 1
                }),
                "smoothness": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
            }
        }

    RETURN_TYPES = ("FLOAT",) * 58 + ("STRING",)
    RETURN_NAMES = tuple(f"value_{i}" for i in range(58)) + ("values_preview",)
    FUNCTION = "generate_values"
    OUTPUT_NODE = False
    CATEGORY = "Utility"

    def generate_values(self, curve1_points, curve2_points, adjustment_point, smoothness):
        # Parse the input strings into lists of floats
        curve1_points = list(map(float, curve1_points.split(',')))
        curve2_points = list(map(float, curve2_points.split(',')))

        # Create x values based on the number of points
        x1 = np.linspace(0, 1, len(curve1_points))
        x2 = np.linspace(0, 1, len(curve2_points))

        # Create the interpolation functions with adjustable smoothness
        interp_func1 = interp1d(x1, curve1_points, kind='quadratic' if smoothness > 0.5 else 'linear', fill_value="extrapolate")
        interp_func2 = interp1d(x2, curve2_points, kind='quadratic' if smoothness > 0.5 else 'linear', fill_value="extrapolate")

        # Interpolate values
        curve1_values = interp_func1(np.linspace(0, 1, adjustment_point + 1))
        curve2_values = interp_func2(np.linspace(0, 1, 58 - adjustment_point - 1))

        # Apply smoothness effect (smoothing out the linear interpolation)
        if smoothness < 1.0:
            curve1_values = self.apply_smoothness(curve1_values, smoothness)
            curve2_values = self.apply_smoothness(curve2_values, smoothness)

        # Combine both curve segments
        values = np.concatenate((curve1_values, curve2_values))

        # Generate a multiline string for the preview
        values_preview = "\n".join([f"{i}: {values[i]:.4f}" for i in range(58)])
        
        # Generate ASCII art curve preview
        ascii_curve_preview = self.generate_ascii_art(values)

        # Combine the numerical preview with the ASCII art preview
        preview = f"Numerical Preview:\n{values_preview}\n\nASCII Art Curve Preview:\n{ascii_curve_preview}"

        return tuple(float(v) for v in values) + (preview,)

    def apply_smoothness(self, values, smoothness):
        # Simple linear interpolation to smooth values
        smoothed_values = values * smoothness + np.linspace(values[0], values[-1], len(values)) * (1 - smoothness)
        return smoothed_values

    def generate_ascii_art(self, values):
        # Determine the height of the ASCII art
        height = 10  # number of rows
        width = 58  # number of columns, one for each value

        # Normalize the values to fit within the height
        normalized_values = np.interp(values, (0, 1), (height - 1, 0))

        # Create a grid to hold the ASCII art
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        # Plot the values onto the grid
        for i, val in enumerate(normalized_values):
            grid[int(val)][i] = '*'

        # Convert the grid to a string
        ascii_art = "\n".join(["".join(row) for row in grid])
        return ascii_art


