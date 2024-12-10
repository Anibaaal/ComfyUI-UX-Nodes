from .nodes import EasyResolutionPicker, BlockLayerStringGenerator

NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "BlockLayerStringGenerator": BlockLayerStringGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "BlockLayerStringGenerator": "Flux Block Weight String",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
