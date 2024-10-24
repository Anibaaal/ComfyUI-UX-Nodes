from .nodes import EasyResolutionPicker, BlockLayerStringGenerator
from .unet_save_mod import ModelSave
from .bnb_otf import CheckpointLoaderBNB, UNETLoaderBNB
from .merging import ModelMergeSD3_Large

NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "ModelSave": ModelSave,
    "CheckpointLoaderBNB": CheckpointLoaderBNB,
    "UNETLoaderBNB": UNETLoaderBNB,
    "BlockLayerStringGenerator": BlockLayerStringGenerator,
    "ModelMergeSD3_Large": ModelMergeSD3_Large,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "ModelSave": "Save Diffusion Model",
    "CheckpointLoaderBNB": "Checkpoint Loader BNB On the fly",
    "UNETLoaderBNB": "UNET Loader BNB On the fly",
    "BlockLayerStringGenerator": "Flux Block Weight String",
    "ModelMergeSD3_Large": "Model Merge SD3 Large",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
