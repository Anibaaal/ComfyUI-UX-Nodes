from .resolution_picker import EasyResolutionPicker
from .step_calculator import StepCalculator
from .denoise_calculator import DenoiseCalculator


NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "StepCalculator": StepCalculator,
    "DenoiseCalculator": DenoiseCalculator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "StepCalculator": "Step Calculator",
    "DenoiseCalculator": "Denoise Calculator"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']