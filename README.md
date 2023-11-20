## An Alternative Approach to Building Generative AI Models?

This project is an approach for building generative models by extracting model weights then using those weights with another generative AI model to predict new weights for reuse in one or many new generative ai model(s). If proven, this approach would hopefully reduce the traditional expensive training costs and enable faster model vetting with a flexible, stream-lined process.

The [bampe-weights](https://github.com/matlok-ai/bampe-weights) repo includes an initial proof of concept for building small, modular weights from a few generative ai model.safetensors files with included benchmarks. In its current state, this PoC is capable of predicting a customizable chunk of predicted weights that you can view to verify whether this idea is feasible or not.

We believe we have found a design pattern for assembling generative ai models faster because our predicted 2d image is visually-similar "enough" to the original multi-dimensional, embedded space tensor image that includes most of the "intelligence" and learning.

Here's the PoC results and dataset so you can download and view with any tool that can view TIFF image files:

### Review the input model's sample weights on GitHub

![Screenshot of tensor weights for GPT2 layer key - h.0.attn.c_attn.weight](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/images/safetensors/gpt2/in/idata__h.0.attn.c_attn.weight.png)

- Source: [Tensor Weight as a Tiff file](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/blob/main/safetensors/gpt2/in/idata__h.0.attn.c_attn.weight.tiff)

### Review the AI's predicted weights on GitHub:

#### CPU-Generated Weights

![Screenshot of CPU-Generated tensor weights for the GPT2 layer key - h.0.attn.c_attn.weight](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/images/safetensors/gpt2/out/cpu-generated_predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.png)

- Source: [CPU-generated Tiff](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/blob/main/safetensors/gpt2/out/cpu-generated_predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff)

#### GPU-Generated WeightPredicteds

![Screenshot of GPU-Generated tensor weights for the GPT2 layer key - h.0.attn.c_attn.weight](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/images/safetensors/gpt2/out/gpu-generated_predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.png)

- Source: [GPU-generated Tiff](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/blob/main/safetensors/gpt2/out/gpu-generated_predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff)

### Sample Weights for the PoC

The PoC input sample weights were extracted from the HuggingFace **model.safetensors** file:

[https://huggingface.co/gpt2/tree/main](https://huggingface.co/gpt2/tree/main)

The results below are available for anyone and let us know if you have any issues trying out the PoC!

### Sources for Inspiration and Help Pushing the Community Forward!

- Tom Jobbins
- Georgi Gerganov
- HuggingFace
- LAVIS
- Stable Diffusion
- LocalLLaMAs
- LLama.cpp
- Weights and Biases

### Getting Started

Extract, Generate, Reuse and Predict new Generative AI Model Weights for LLMs or Text-to-Image or Image-to-Image or Text-to-Audio or Audio-to-Audio Models

#### Download a model.safetensors file

This version only supports model.safetensors files downloaded from [GPTQ models on the HuggingFace leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard).

As of 2023-11-17 here are some of the current GPTQ model leaders and most-downloads that include a huge file with the pre-trained weights (download the model.safetensors file).

The below model is good for a lightweight PoC (weight is ~6.8 MB):

- [Review the 523 MB GPT2 model.safetensors file on HuggingFace](https://huggingface.co/gpt2/tree/main)

Larger examples we are already using:

- [Llama-2-7B-Chat-GPTQ](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GPTQ/tree/main)
- [Llama-2-70B-Chat-GPTQ](https://huggingface.co/TheBloke/Llama-2-70B-Chat-GPTQ/tree/main)
- [CodeLlama-34B-Instruct-GPTQ](https://huggingface.co/TheBloke/CodeLlama-34B-Instruct-GPTQ/tree/main)
- [Airoboros-L2-70B-2.1-GPTQ](https://huggingface.co/TheBloke/Airoboros-L2-70B-2.1-GPTQ/tree/main)

```bash
# wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GPTQ/resolve/main/model.safetensors
# wget https://huggingface.co/TheBloke/Llama-2-70B-Chat-GPTQ/resolve/main/model.safetensors
wget https://huggingface.co/gpt2/resolve/main/model.safetensors
```

#### Install

##### Clone

```bash
git clone https://github.com/matlok-ai/bampe-weights
cd bampe-weights
```

##### Install

Install the latest pip:

```bash
pip install bampe-weights
```

Or install the development build:

```bash
pip install -e .
```

### Supports GPU or CPU

#### Current Performance Benchmarks

Customizable weight prediction sizes based off resource constraints (IoT, embedded devices will have different profiles)

Use Case | Size | Time | Hardware |
--- | --- | --- | --- |
small | ~780 KB | 13s | cpu-only on m2 SSD m2 |
small | ~780 KB | 40s | cpu-only on SAS hdd |
medium | ~3 mb | 120s | cpu-only on m2 SSD |
large | ~5-12 mb | >3m | cpu-only on SAS hdd |
large | ~5-12 mb | 30s | gpu-only on SAS hdd |

**Notes:**

- Testing shows you can generate a 5-12 MB chunk of predicted weights in ~30s on an Nvidia 4070 ti.
- By default the included examples run on cpu, but if you have a gpu the examples will run faster by setting this environment variable before starting:

By default, the included examples run on cpu, but if you have a gpu the examples will run faster by setting this environment variable before starting:

```bash
export DEVICE=cuda
```

### Extract Weights

By default this will extract to the ``./npy/weights`` directory.

```bash
time ./examples/step-1-extract-tensors.py
```

### Convert Weights to Tiff Format

By default this will store the new Tiff file in the ``./tiff`` directory.

```bash
time ./examples/step-2-convert-npy-to-tiff.py
```

### Predict LLM Weights using Stable Diffusion

By default this will store the new LLM weight chunk bufffer Tiff file in the ``./chunks`` directory. If you have not run this before, the command will download the [~8GB Salesforce BLIP-2 generative ai image model (image2image)](https://huggingface.co/docs/transformers/main/en/model_doc/blip-2) from HuggingFace.

Note: I included more detailed benchmarks in the [./examples/step-3-generate-model-weight-chunk-as-tiff.py](https://github.com/matlok-ai/bampe-weights/blob/main/examples/step-3-generate-model-weight-chunk-as-tiff.py) script. Hopefully other hardware has consistent performance with this gaming machine running wsl2 Ubuntu 22.04 with python 3.11.

#### Predicting ~780 KB of new Generative AI model tensor weights using Stable Diffusion on CPU

##### Predictions on SSD takes 13 seconds

```bash
time ./examples/step-3-generate-model-weight-chunk-as-tiff.py
2023-11-17 12:00:47.212 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - loading Salesforce/blipdiffusion gen ai pipeline on device=cpu prediction with num_inf=3 buffer size width=512 height=512
vision_encoder/model.safetensors not found
Loading pipeline components...: 100%|█████████████████████████████████████████████████████████████████████████| 7/7 [00:02<00:00,  2.56it/s]2023-11-17 12:00:50.502 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - loading image=./tiff/idata__h.0.attn.c_attn.weight.tiff gen 512x512 prompt=
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:05<00:00,  1.43s/it]2023-11-17 12:00:59.750 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - saving chunk to: ./chunks/predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff
2023-11-17 12:00:59.750 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - output[0]=<PIL.Image.Image image mode=RGB size=512x512 at 0x7F97912B7D90>
2023-11-17 12:00:59.764 INFO step-3-generate-model-weight-chunk-as-tiff - <module> - done predicting new llm weights - please compare
source tensor weight image file:
./tiff/idata__h.0.attn.c_attn.weight.tiff
to the predicted weights file by the generative image ai model:
./chunks/predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff


real    0m13.522s
user    1m43.081s
sys     0m9.837s
```

##### Predictions on SAS hard drive takes ~40 seconds

```bash
2023-11-17 17:16:52.699 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - loading Salesforce/blipdiffusion gen ai pipeline on device=cpu prediction with num_inf=3 buffer size width=512 height=512
vae/diffusion_pytorch_model.safetensors not found
Loading pipeline components...: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:09<00:00,  1.33s/it]2023-11-17 17:17:03.005 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - loading image=./tiff/idata__h.0.attn.c_attn.weight.tiff gen 512x512 prompt=
  0%|                                                                                                                                                                                        | 0/4 [00:00<?, ?it/s][W NNPACK.cpp:64] Could not initialize NNPACK! Reason: Unsupported hardware.
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:14<00:00,  3.66s/it]2023-11-17 17:17:28.070 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - saving chunk to: ./chunks/predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff
2023-11-17 17:17:28.070 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - output[0]=<PIL.Image.Image image mode=RGB size=512x512 at 0x7F634949B7D0>
2023-11-17 17:17:28.377 INFO step-3-generate-model-weight-chunk-as-tiff - <module> - done predicting new llm weights - please compare
source tensor weight image file:
./tiff/idata__h.0.attn.c_attn.weight.tiff
to the predicted weights file by the generative image ai model:
./chunks/predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff


real    0m39.590s
user    7m20.328s
sys     2m18.198s
```

#### Predicting 12 MB of new Generative AI model tensor weights using Stable Diffusion on GPU in 33 seconds

For the demo GPT 2 model, this usually is more LLM tensor weights than the original seed tensor weight data (6.8 mb was used to predict ~11.8mb)

```bash
export DEVICE=cuda; time  ./examples/step-3-generate-model-weight-chunk-as-tiff.py
2023-11-17 12:04:20.558 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - loading Salesforce/blipdiffusion gen ai pipeline on device=cuda prediction with num_inf=3 buffer size width=2000 height=2000
vision_encoder/model.safetensors not found
Loading pipeline components...: 100%|█████████████████████████████████████████████████████████████████████████| 7/7 [00:02<00:00,  3.20it/s]2023-11-17 12:04:23.932 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - loading image=./tiff/idata__h.0.attn.c_attn.weight.tiff gen 2000x2000 prompt=
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:03<00:00,  1.23it/s]2023-11-17 12:04:52.293 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - saving chunk to: ./chunks/predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff
2023-11-17 12:04:52.293 INFO generators - run_stable_diffusion_to_generate_model_weight_layer_as_image - output[0]=<PIL.Image.Image image mode=RGB size=2000x2000 at 0x7FD65B68BED0>
2023-11-17 12:04:52.304 INFO step-3-generate-model-weight-chunk-as-tiff - <module> - done predicting new llm weights - please compare
source tensor weight image file:
./tiff/idata__h.0.attn.c_attn.weight.tiff
to the predicted weights file by the generative image ai model:
./chunks/predicted-model-weights__layer__h.0.attn.c_attn.weight__chunk__0.tiff


real    0m33.368s
user    0m32.405s
sys     0m5.949s
```

## Linting

```bash
black --line-length 60 *.py bw/*/*.py examples/*.py
```

#### Coming Soon

- Build a foundational model with a File transformer that can predict any type of file contents (llm tensor weights are just the first use case - json/tcp/protocols should work too)
- Use the file transformer to build new model weights for model weight reassembly and testing
- Support for GGUF/bin and other model file formats. I have a poc using llama.cpp GGUF, but it is not ready for release due to how the quantization process works. It made me worried that additional byte-level compression would invalidate this early approach.

#### Learn More

- [Homepage - https://matlok.ai](https://matlok.ai)
- [ReadTheDocs - bampe-weights](https://bampe-weights.readthedocs.io/en/latest/)
- [PyPi - bampe-weights](https://pypi.org/project/bampe-weights/)

##### Who made this?

Made with <3 by smooth-brained ai models,

Hakinge and Bampe

![Made by the AI-generated matlok avatars Hakinge and Bampe](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/users/hakinge-jonter-and-bampe-hic-small.jpg)

Reach out if you want to catch up and thanks for reading,

hello@matlok.ai

