import json

class RemoveJSONMarkdownFormatting:
    """
    A custom node for ComfyUI that removes Markdown JSON formatting from a text string.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "remove_formatting"

    CATEGORY = "utils"

    def remove_formatting(self, text):
        """
        Removes Markdown JSON formatting if present in the input string.

        Args:
            text: The input text string.

        Returns:
            The cleaned text string without Markdown JSON formatting.
        """
        # Check if the text starts and ends with ```json and ```
        if text.strip().startswith("```json") and text.strip().endswith("```"):
            try:
                # Extract the JSON part
                start_index = text.find("{")
                end_index = text.rfind("}") + 1
                json_string = text[start_index:end_index]
                
                # check if it is valid json before returning to avoid errors
                json.loads(json_string)

                return (json_string,)
            except ValueError:
                # Handle invalid JSON or incorrect formatting (e.g. no JSON present inside the markdown)
                return (text,)
        else:
            # Return the original text if no Markdown JSON formatting is found
            return (text,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "RemoveJSONMarkdownFormatting": RemoveJSONMarkdownFormatting
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RemoveJSONMarkdownFormatting": "Remove JSON Markdown"
}