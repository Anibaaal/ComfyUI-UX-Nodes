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
                        '16:10',
                        '7:4',
                        '16:9',
                        '1.85:1',
                        '2:1',
                        '2.35:1'
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
                })
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "resolution_str")
    FUNCTION = "calculate_resolution"
    OUTPUT_NODE = False
    CATEGORY = "Utility"

    def calculate_resolution(self, aspect_ratio, orientation, length_type, side_length):
        aspect_ratios = {
            '1:1': (1, 1),
            '5:4': (5, 4),
            '4:3': (4, 3),
            '3:2': (3, 2),
            '16:10': (16, 10),
            '7:4': (7, 4),
            '16:9': (16, 9),
            '1.85:1': (1.85, 1),
            '2:1': (2, 1),
            '2.35:1': (2.35, 1)
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

        # Update the node title with the resolution preview
        self.NAME = f"Easy Resolution Picker ({resolution_str})"
        
        return width, height, resolution_str

    @classmethod
    def OUTPUT_TYPES(cls):
        return {
            "required": {
                "resolution_text": ("STRING", {"default": "", "multiline": True})
            }
        }

    def run(self, resolution_str):
        return {"ui": {"resolution_text": self.resolution_str}, "result": (self.resolution_str,)}