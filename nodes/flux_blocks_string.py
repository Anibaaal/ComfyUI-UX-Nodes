class BlockLayerStringGenerator:
    NAME = "Block Layer String Generator"
    
    def __init__(self):
        self.comma_separated_string = ""

    @classmethod
    def INPUT_TYPES(cls):
        double_blocks = {f"DOUBLE{i}": ("FLOAT", {"default": 1.0}) for i in range(19)}
        single_blocks = {f"SINGLE{i}": ("FLOAT", {"default": 1.0}) for i in range(38)}
        base_block = {"final_layer": ("FLOAT", {"default": 1.0})}

        return {
            "required": {**double_blocks, **single_blocks, **base_block},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("comma_separated_string",)
    FUNCTION = "generate_string"
    OUTPUT_NODE = False
    CATEGORY = "Custom Nodes"

    def generate_string(self, **kwargs):
        # Define the correct order of keys
        keys_order = (
            [f"DOUBLE{i}" for i in range(19)] +
            [f"SINGLE{i}" for i in range(38)] +
            ["final_layer"]
        )
        
        # Collect values in the defined order
        values = [str(kwargs[key]) for key in keys_order]
        
        # Join the values with commas
        self.comma_separated_string = ",".join(values)
        
        # Return the string as a tuple
        return (self.comma_separated_string,)
