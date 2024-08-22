from .nodes import EasyResolutionPicker, SmoothCurveMergerFlux
from .unet_save_mod import ModelSave
from .bnb_otf import CheckpointLoaderBNB, UNETLoaderBNB

NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "ModelSave": ModelSave,
    "SmoothCurveMergerFlux": SmoothCurveMergerFlux,
    "CheckpointLoaderBNB": CheckpointLoaderBNB,
    "UNETLoaderBNB": UNETLoaderBNB
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "ModelSave": "Save Diffusion Model",
    "SmoothCurveMergerFlux": "Smooth Curve Merger Flux",
    "CheckpointLoaderBNB": "Checkpoint Loader BNB On the fly",
    "UNETLoaderBNB": "UNET Loader BNB On the fly",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
