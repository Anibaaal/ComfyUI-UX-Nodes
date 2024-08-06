class DenoiseCalculator:
    NAME = "Denoise Calculator"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_steps": ("INT", {
                    "default": 20,
                    "min": 1,
                    "max": 500,
                    "step": 1
                }),
                "ratio": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.01,
                    "max": 1.0,
                    "step": 0.01
                })
            },
        }

    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("total_steps", "denoise")
    FUNCTION = "calculate_denoise"
    OUTPUT_NODE = False
    CATEGORY = "UX Nodes"

    def calculate_denoise(self, target_steps, ratio):
        total_steps = round(target_steps / ratio)
        denoise = ratio
        
        return total_steps, denoise