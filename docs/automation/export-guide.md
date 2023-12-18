## Automation and Reproducibility

### Overview

This guide hopefully makes it easier to reproduce and export 3d visualizations and animations on your own hardware.

It also assumes you have already set these up:

-   [Development Environment](https://bampe-weights.readthedocs.io/en/latest/sdk/setting-up-a-development-environment/)
-   [Install Blender for the Command Line](https://bampe-weights.readthedocs.io/en/latest/sdk/blender/blender-install-notes/)

## Datasets

### How do I Convert an Existing AI Model File to a HuggingFace SafeTensors Format?

For now the only supported model file is a HuggingFace safetensors file (a GPTQ model file). Below are one-time options to download example model.safetensors file(s). HuggingFace can also convert model bin files to safetensors with these supported options:

- [HuggingFace Convert a Model Online](https://huggingface.co/spaces/diffusers/convert)
- [HuggingFace Convert a Model to a SafeTensors file](https://huggingface.co/docs/safetensors/convert-weights)
- [HuggingFace Convert Script](https://github.com/huggingface/safetensors/blob/main/bindings/python/convert.py)

### GPT2 model.safetensors

```bash
export MODEL=./gpt2.model.safetensors
wget https://huggingface.co/gpt2/resolve/main/model.safetensors -O "${MODEL}"
```

### Llama 2 7B Chat GPTQ model.safetensors

```bash
export MODEL=./llama-2-7b-chat.model.safetensors
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GPTQ/resolve/main/model.safetensors -O "${MODEL}"
```

### Mistral 7B OpenOrca GPTQ model.safetensors

```bash
export MODEL=./mistral-7b-openorca.model.safetensors
wget https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GPTQ/resolve/main/model.safetensors -O "${MODEL}"
```

### Dolphin 2.5 Mixtral - 8x7B GPTQ model.safetensors

```bash
export MODEL=./dolphin-2.5-mixtral-8x7b.model.safetensors
wget https://huggingface.co/TheBloke/dolphin-2.5-mixtral-8x7b-GPTQ/resolve/main/model.safetensors?download=true -O "${MODEL}"
```

### Phind 34B v2 GPTQ model.safetensors

```bash
export MODEL=./phind-34b-v2.model.safetensors
wget https://huggingface.co/TheBloke/Phind-CodeLlama-34B-v2-GPTQ/resolve/main/model.safetensors?download=true -O "${MODEL}"
```

### DeepSeek Coder 33B Instruct GPTQ model.safetensors

```bash
export MODEL=./deepseek-coder-33B-instruct.model.safetensors
wget https://huggingface.co/TheBloke/deepseek-coder-33B-instruct-GPTQ/resolve/main/model.safetensors?download=true -O "${MODEL}"
```

## Visualizations, Animations and Exporting to STL and glTF Binary (glb) Files

### Run Blender Automation and Export to an Animated GIF

Note: gif creation is more resource intensive than just exporting to STL and glTF. Please be patient.

```bash
# pick a model safetensors file
# name="gpt2"
# name="llama-2-7b-chat"
name="mistral-7b-openorca"
echo "start: ${name}"
export ROWS=256
export COLS=256
export FACES=10000
# how many layers do you want to extract
export MAX_LAYERS=50
# automatic shutdown once done
export SHUTDOWN_ENABLED=1
export FRAMES=50
mkdir -p "/tmp/blender/${name}"
export MODEL="./${name}.model.safetensors"
export GIF="/tmp/blender/${name}/${name}-${ROWS}x${COLS}"
unset GLTF STL
rm -rf .tmp/*; time blender -p 400 400 800 800 --python ./examples/show-model.py
```

### Run Blender Automation and Export to STL and glTF Binary

Run this following code to generate your own artifacts from a list of models using bash into the **output_dir** directory.

```bash
ls -lrth blender/*
blender/gpt2:
total 473M
-rw-r--r-- 1 matlok matlok 210M Dec 15 08:26 gpt2-256x256.stl
-rw-r--r-- 1 matlok matlok 264M Dec 15 08:26 gpt2-256x256-gltf.glb

blender/llama-2-7b-chat:
total 210M
-rw-r--r-- 1 matlok matlok  96M Dec 15 08:27 llama-2-7b-chat-256x256.stl
-rw-r--r-- 1 matlok matlok 115M Dec 15 08:27 llama-2-7b-chat-256x256-gltf.glb

blender/mistral-7b-openorca:
total 219M
-rw-r--r-- 1 matlok matlok 101M Dec 15 08:27 mistral-7b-openorca-256x256.stl
-rw-r--r-- 1 matlok matlok 118M Dec 15 08:27 mistral-7b-openorca-256x256-gltf.glb
```

Once you generate the artifacts, you can view each visualization with the [Viewing AI Models with a Blender Container Image](https://github.com/matlok-ai/bampe-weights/tree/main/README.md#viewing-ai-models-with-a-blender-container-image).

### Analyze and Export 128x128 Five Layer Mesh Demos with Configurable Extracted Shapes

```bash
profile_models="gpt2 llama-2-7b-chat mistral-7b-openorca dolphin-2.5-mixtral-8x7b phind-34b-v2 deepseek-coder-33B-instruct"
dims="128"
layers="5"
echo "profiling: ${profile_models} dimensions: ${dims} layers: ${layers}"
# automatic shutdown once done
export SHUTDOWN_ENABLED=1
# gif creation is more resource intense
unset GIF
label=""
# where to store the artifacts
output_dir="./blender"
if [[ ! -e "${output_dir}" ]]; then
    mkdir "${output_dir}"
fi
echo "processing models: ${profile_models}"
for use_layer in ${layers}; do
    export MAX_LAYERS="${use_layer}"
    for use_dim in ${dims}; do
        export ROWS="${use_dim}"
        export COLS="${use_dim}"
        if [[ "${use_dim}" == "128" ]]; then
            export FACES=200000
        elif [[ "${use_dim}" == "256" ]]; then
            export FACES=100000
        elif [[ "${use_dim}" == "512" ]]; then
            export FACES=20000
        elif [[ "${use_dim}" == "1024" ]]; then
            export FACES=10000
        fi
        label="dim_${use_dim}_shapes_${FACES}_layers_${MAX_LAYERS}"
        echo "processing ${use_dim} - ${label}"
        for name in ${profile_models}; do
            echo "starting: ${name} - ${label}"
            mkdir -p "${output_dir}/${name}"
            export MODEL="./${name}.model.safetensors"
            # GLTF supports colors
            export GLTF="${output_dir}/${name}/${name}-${label}-gltf"
            export GLTF="${output_dir}/demo-${name}-${label}-gltf"
            # STL does not support colors
            export STL="${output_dir}/${name}-${label}.stl"
            export STL="${output_dir}/demo-${name}-${label}.stl"
            # clear any previous temp images
            rm -rf .tmp/*; time blender -p 400 400 800 800 --python ./examples/show-model.py
            echo "done: ${name} - ${label}"
        done
    done
done
```

### Analyze and Export Dense 512x512 Two Layer Mesh Demos (targeting 500k shapes extracted per model layer)

```bash
profile_models="gpt2 llama-2-7b-chat mistral-7b-openorca dolphin-2.5-mixtral-8x7b phind-34b-v2 deepseek-coder-33B-instruct"
layers="2"
dims="512"
echo "profiling: ${profile_models} dimensions: ${dims} layers: ${layers}"
# automatic shutdown once done
export SHUTDOWN_ENABLED=1
# gif creation is more resource intense
unset GIF
label=""
# where to store the artifacts
output_dir="./blender"
if [[ ! -e "${output_dir}" ]]; then
    mkdir "${output_dir}"
fi
echo "processing models: ${profile_models}"
for use_layer in ${layers}; do
    export MAX_LAYERS="${use_layer}"
    for use_dim in ${dims}; do
        export ROWS="${use_dim}"
        export COLS="${use_dim}"
        export FACES=500000
        label="dim_${use_dim}_shapes_${FACES}_layers_${MAX_LAYERS}"
        echo "processing ${use_dim} - ${label}"
        for name in ${profile_models}; do
            echo "starting: ${name} - ${label}"
            mkdir -p "${output_dir}/${name}"
            export MODEL="./${name}.model.safetensors"
            # GLTF supports colors
            export GLTF="${output_dir}/${name}/${name}-${label}-gltf"
            export GLTF="${output_dir}/demo-${name}-${label}-gltf"
            # STL does not support colors
            export STL="${output_dir}/${name}-${label}.stl"
            export STL="${output_dir}/demo-${name}-${label}.stl"
            # clear any previous temp images
            rm -rf .tmp/*; time blender -p 400 400 800 800 --python ./examples/show-model.py
            echo "done: ${name} - ${label}"
        done
    done
done
unset MAX_LAYERS
for use_dim in ${dims}; do
    export ROWS="${use_dim}"
    export COLS="${use_dim}"
    export FACES=200000
    label="dim_${use_dim}_shapes_${FACES}_layers_all"
    echo "processing ${use_dim} - ${label}"
    for name in ${profile_models}; do
        echo "starting: ${name} - ${label}"
        mkdir -p "${output_dir}/${name}"
        export MODEL="./${name}.model.safetensors"
        # GLTF supports colors
        export GLTF="${output_dir}/${name}/${name}-${label}-gltf"
        # STL does not support colors
        export STL="${output_dir}/${name}/${name}-${label}.stl"
        # clear any previous temp images
        rm -rf .tmp/*; time blender -p 400 400 800 800 --python ./examples/show-model.py
        echo "done: ${name} - ${label}"
    done
done
```

### Analyze and Export 256x256 50 Layer Mesh Demos (targeting 10k shapes extracted per model layer)

```bash
profile_models="gpt2 llama-2-7b-chat mistral-7b-openorca"
echo "profiling: ${profile_models}"
export ROWS=256
export COLS=256
export FACES=10000
# how many layers do you want to extract
export MAX_LAYERS=50
# automatic shutdown once done
export SHUTDOWN_ENABLED=1
# gif creation is more resource intense
unset GIF
# where to store the artifacts
output_dir="./blender"
if [[ ! -e "${output_dir}" ]]; then
    mkdir "${output_dir}"
fi
echo "processing models: ${profile_models}"
for name in ${profile_models}; do
    echo "starting: ${name}"
    mkdir -p "${output_dir}/${name}"
    export MODEL="./${name}.model.safetensors"
    # GLTF supports colors
    export GLTF="${output_dir}/${name}/${name}-${ROWS}x${COLS}-gltf"
    # STL does not support colors
    export STL="${output_dir}/${name}/${name}-${ROWS}x${COLS}.stl"
    # clear any previous temp images
    rm -rf .tmp/*; time blender -p 400 400 800 800 --python ./examples/show-model.py
    echo "done: ${name}"
done
```
