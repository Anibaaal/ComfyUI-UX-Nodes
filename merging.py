import comfy_extras.nodes_model_merging

class ModelMergeSD3_Large(comfy_extras.nodes_model_merging.ModelMergeBlocks):
    CATEGORY = "advanced/model_merging/model_specific"

    @classmethod
    def INPUT_TYPES(s):
        arg_dict = { "model1": ("MODEL",),
                              "model2": ("MODEL",)}

        argument = ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01})

        arg_dict["pos_embed."] = argument
        arg_dict["x_embedder."] = argument
        arg_dict["context_embedder."] = argument
        arg_dict["y_embedder."] = argument
        arg_dict["t_embedder."] = argument

        for i in range(38):
            arg_dict["joint_blocks.{}.".format(i)] = argument

        arg_dict["final_layer."] = argument

        return {"required": arg_dict}
