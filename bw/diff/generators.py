import os
import logging
import diffusers.pipelines as bdp
import diffusers.utils as dutils
import torch


log = logging.getLogger(__name__)


def run_stable_diffusion_to_generate_model_weight_layer_as_image(
    input_file: str,
    output_file: str,
    prompt: str,
    neg_prompt: str,
    cond_subject: str,
    tgt_subject: str,
    guidance_scale: float = 7.5,
    num_inference_steps: int = 5,
    model_name: str = "Salesforce/blipdiffusion",
    device: str = "cpu",
    height: int = 2000,
    width: int = 2000,
    auto_save: bool = True,
):
    """
    run_stable_diffusion_to_generate_model_weight_layer_as_image

    generate a predicted llm model weight layer chunk (~5mb)
    using an existing image from an extracted tensor weight
    file (also saved as a tiff image). by default, a 2000x2000
    tiff file is ~5mb each time this method is called.

    if you call this method 20 times, then you have 20 model
    weight chunks to reassemble

    uses this api on the diffusers repo

    [diffusers/pipelines/blip_diffusion/pipeline_blip_diffusion.py](https://
    github.com/huggingface/diffusers/blob/main/src/
    diffusers/pipelines/blip_diffusion/pipeline_blip_diffusion.py#L188)

    Save the predicted (weights) buffer as a tiff image file to the
    ``output_file`` path on disk.

    :param input_file: path to the input weights file (tiff)
    :param output_file: path to save the predicted
        model layer chunk
    :param prompt: question for the prediction
    :param neg_prompt: negative prompt for the prediction
    :param guidance_scale: guidance for the stable diffusion
        pipeline
    :param num_inference_steps: number of inference steps
        for the Stable Diffusion Blip2 pipeline
    :param model_name: name of the gen ai image transformer
        to use for the prediction buffer chunk
    :param device: name of the device for hosting the gen
        ai workloads
        with default set to cpu vs cuda for running on gpus
    :param height: number of pixels for the predicted image's
        height with default 2000
    :param width: number of pixels for the predicted image's
        width with default 2000
    :param auto_save: flag to save the predicted image to
        disk with default True
    """
    if not os.path.exists(input_file):
        log.error(f"unable to find input_file={input_file}")
        return None
    log.info(
        f"loading {model_name} gen ai "
        f"pipeline on device={device} "
        f"prediction with "
        f"num_inf={num_inference_steps} "
        "buffer size "
        f"width={width} "
        f"height={height}"
    )
    if device == "cpu":
        blip_diffusion_pipe = bdp.BlipDiffusionPipeline.from_pretrained(
            model_name,
            # does not work on
            # ubuntu 22 wslv2 windows 11
            # torch_dtype=torch.float16,
            torch_dtype=torch.float,
        ).to(
            device
        )
    else:
        blip_diffusion_pipe = bdp.BlipDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            # use_safetensors=True,
        ).to(
            device
        )
    log.info(
        f"loading image={input_file} "
        f"gen {height}x{width} prompt={prompt[0:10]}"
    )
    ref_image = dutils.load_image(input_file)
    output = blip_diffusion_pipe(
        prompt=prompt,
        reference_image=ref_image,
        source_subject_category=cond_subject,
        target_subject_category=tgt_subject,
        latents=None,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        neg_prompt=neg_prompt,
        height=height,
        width=width,
    ).images
    if auto_save:
        log.info(f"saving chunk to: {output_file}")
        for idx, node in enumerate(output):
            log.info(f"output[{idx}]={node}")
        output[0].save(output_file)
    return output
