from .nodes import EasyResolutionPicker, SmoothCurveMerger
from .utils import UNETSave

NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "UNETSave": UNETSave,
    "SmoothCurveMerger": SmoothCurveMerger
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "UNETSave": "Save Diffusion Model",
    "SmoothCurveMerger": "Smooth Curve Merger"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
