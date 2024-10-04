from .nodes import EasyResolutionPicker, BlockLayerStringGenerator
from .unet_save_mod import ModelSave
from .bnb_otf import CheckpointLoaderBNB, UNETLoaderBNB

NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "ModelSave": ModelSave,
    "CheckpointLoaderBNB": CheckpointLoaderBNB,
    "UNETLoaderBNB": UNETLoaderBNB,
    "BlockLayerStringGenerator": BlockLayerStringGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "ModelSave": "Save Diffusion Model",
    "CheckpointLoaderBNB": "Checkpoint Loader BNB On the fly",
    "UNETLoaderBNB": "UNET Loader BNB On the fly",
    "BlockLayerStringGenerator": "Flux Block Weight String",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
