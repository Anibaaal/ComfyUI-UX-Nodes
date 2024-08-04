from .resolution_picker import EasyResolutionPicker
from .step_calculator import StepCalculator


NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "StepCalculator": StepCalculator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "StepCalculator": "Step Calculator"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']