#!/usr/bin/env python3

import os
import logging
import bw.diff.generators as gen

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


def generate_model_weight_chunk_as_tiff():
    """
    generate_model_weight_chunk_as_tiff

    use ai to predict new weights as
    a tiff file from a tiff file

    need to add argparse here for picking a model layer
    and tensor weight name - if missing on the cli then
    show to stdout the list of availaable model tensor
    weights by name and let the user
    pick which one to rip out with rust/mmap
    """

    # other model tensors we have experimented with chunking
    # Llama-2-7B-Chat-GPT
    # model_layer_key = "model.layers.0.mlp.up_proj.qweight"
    # Llama-2-70B-Chat-GPT
    # model_layer_key = "model.layers.0.mlp.up_proj.qweight"
    # CodeLlama-34B-Instruct-GPTQ
    # model_layer_key = "model.layers.0.mlp.up_proj.qweight"
    # GPT2
    model_layer_key = "h.0.attn.c_attn.weight"

    guidance_scale = 0.000000001

    device = os.getenv("DEVICE", "cpu")

    # settings for cpu demos

    # ~785kb in ~13s on cpu
    num_inference_steps = 3
    height = 512
    width = 512

    # ~3.1mb in ~2 min
    # height = 1024
    # width = 1024

    if device != "cpu":
        # nvidia 4070 ti settings
        num_inference_steps = 200  # ~3m
        num_inference_steps = 50  # ~45s
        num_inference_steps = 10  # ~40s
        num_inference_steps = 5  # ~34s
        num_inference_steps = 3  # ~30s
        # 5mb float16
        # 12mb float32
        # in ~30s on nvidia 4070 ti
        height = 2000
        width = 2000

    tiff_input_file = (
        f"./tiff/idata__{model_layer_key}.tiff"
    )
    cond_subject = ""
    tgt_subject = ""
    prompt = ""
    neg_prompt = ""

    output_file = (
        "./chunks/"
        "predicted-model-weights__"
        f"layer__{model_layer_key}"
        "__chunk__0.tiff"
    )

    gen.run_stable_diffusion_to_generate_model_weight_layer_as_image(
        input_file=tiff_input_file,
        prompt=prompt,
        neg_prompt=neg_prompt,
        output_file=output_file,
        cond_subject=cond_subject,
        tgt_subject=tgt_subject,
        device=device,
        height=height,
        width=width,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
    )
    if os.path.exists(output_file):
        log.info(
            "done predicting new llm weights - \n"
            "please compare source tensor weight "
            "image file:\n"
            f"{tiff_input_file}\n"
            "to the predicted weights file by "
            "the generative image ai model:\n"
            f"{output_file}\n"
        )
    else:
        log.error("did not generate predicted weights")


if __name__ == "__main__":
    generate_model_weight_chunk_as_tiff()
