#!/usr/bin/env python3

import os
import logging
import bw.converter.convert_tensor_weights_to_tiff as convert

level = logging.INFO
log_level = os.getenv("LOG", "info")
if log_level == "debug":
    level = logging.DEBUG

logging.basicConfig(
    level=level,
    format=(
        "%(asctime)s.%(msecs)03d %(levelname)s "
        "%(module)s - %(funcName)s - %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger(__name__)


if __name__ == "__main__":
    # need to add argparse here for picking a model layer
    # and tensor weight name - if missing on the cli then
    # show to stdout the list of availaable model tensor
    # weights by name and let the user
    # pick which one to rip out with rust/mmap

    # Llama-2-7B-Chat-GPT
    # model_layer_key = "model.layers.0.mlp.up_proj.qweight"
    # Llama-2-70B-Chat-GPT
    # model_layer_key = "model.layers.0.mlp.up_proj.qweight"
    # CodeLlama-34B-Instruct-GPTQ
    # model_layer_key = "model.layers.0.mlp.up_proj.qweight"
    # GPT2
    model_layer_key = "h.0.attn.c_attn.weight"

    npy_file = f"./npy/weights/tdata__{model_layer_key}.npy"
    model_layer_weight_chunk_file = (
        f"./tiff/idata__{model_layer_key}.tiff"
    )
    convert.convert_tiff_from_model_tensor_weight_npy_file(
        input_file=npy_file,
        output_file=model_layer_weight_chunk_file,
    )
    if os.path.exists(model_layer_weight_chunk_file):
        print(
            f"success - created {model_layer_key} "
            f"tiff={model_layer_weight_chunk_file}"
        )
    else:
        print(
            f"failed to create {model_layer_key} "
            f"tiff={model_layer_weight_chunk_file}"
        )
