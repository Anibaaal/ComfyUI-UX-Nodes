from .nodes.ez_resolution import EasyResolutionPicker
from .nodes.flux_blocks_string import BlockLayerStringGenerator
from .nodes.color_generator import ColorGeneratorNode
from .nodes.lerp_node import LerpNode
from .nodes.blur_node import BlurNode
from .nodes.drop_shadow_node import DropShadowNode
from .nodes.advanced_composite_image_masked import AdvancedCompositeImageMasked

NODE_CLASS_MAPPINGS = {
    "EasyResolutionPicker": EasyResolutionPicker,
    "BlockLayerStringGenerator": BlockLayerStringGenerator,
    "ColorGeneratorNode": ColorGeneratorNode,
    "LerpNode": LerpNode,
    "BlurNode": BlurNode,
    "DropShadowNode": DropShadowNode,
    "AdvancedCompositeImageMasked": AdvancedCompositeImageMasked,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "EasyResolutionPicker": "Easy Resolution Picker",
    "BlockLayerStringGenerator": "Flux Block Weight String",
    "ColorGeneratorNode": "Generate Solid Color",
    "LerpNode": "Lerp (Float)",
    "BlurNode": "Fast Blur (GPU)",
    "DropShadowNode": "Drop Shadow Composite",
    "AdvancedCompositeImageMasked": "Advanced Composite Image Masked",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
