class StepCalculator:
    NAME = "Step Calculator"

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "steps": ("INT", {
                    "default": 4,
                    "min": 1,
                    "max": 100,
                    "step": 1
                }),
                "ratio": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.01,
                    "max": 1.0,
                    "step": 0.01
                })
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("calculated_steps", "start_at_step")
    FUNCTION = "calculate_steps"
    OUTPUT_NODE = False
    CATEGORY = "Utility"

    def calculate_steps(self, steps, ratio):
        calculated_steps = round(steps / ratio)
        start_at_step = round(calculated_steps - steps)
        
        return calculated_steps, start_at_step
