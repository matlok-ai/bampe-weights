## Can an AI visualizer help us build and audit AI models?

Building large AI models has a learning curve, and is both time and resource intensive. Until recently, we thought of a pre-trained AI’s model weights as ambiguous 2d arrays of decimal numbers, but what if there was something more.

![Using Blender and Marching Cubes to Extract and View Shapes in Model Weights](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/images/blender/viewing-gpt2-tensor-weights-as-shapes-using-marching-cubes.png)

Today we want to share how we are exploring AI model weights, but first let’s see how we got here.

![Extract and View Configurable Model Layer Weights using Blender](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/images/blender/gpt2-tensor-weights-in-blender-legend.png)

### Background

1.  We read these key papers

    - [ImageNet classification with deep convolutional neural networks](https://dl.acm.org/doi/10.1145/3065386)

    - [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

1.  Takeaways / Highlights

    - Transformers and attention are used for encoding and decoding training data
    - Architecture enables making predictions using math and matrices by hosting the weights in memory
    - Everything needed to reproduce Transformer behaviors are stored and shared as weights in model files
    - Weights are saved as numerical data in a model file (usually 2d float 32 arrays)

1.  Key Questions

    -   What else works with matrices and high resolution float 32 data? (TIFF images)?

        -   Graphics / gaming engines / ffmpeg
        -   [Brain image scanning with FMRI / CAT / MEG](https://www.ncbi.nlm.nih.gov/books/NBK2602/)
        -   [Nasa Earthdata GeoTiff](https://www.earthdata.nasa.gov/esdis/esco/standards-and-practices/geotiff)

    -   Why can’t we reuse similar techniques from these systems that have large, high resolution datasets to navigate “the weights” with a different type of iterator? With the current rust and mmap performance loading a 100 GB file on disk, who knows maybe this approach could work without a GPU for smaller models constrained to CPU-only.
    -   What technical pieces are missing/required to get started?
        -   What do the weights look like?
        -   How can we teach AI to learn what weights mean?
        -   What can we do with time series training data based on how an AI model’s weights changed over time?

### Conclusion

-   What

    - We have built a prototype for extracting and hopefully identifying how weights:

        - relate back to the original source training data

        - change over many training generations

        - appear to represent a dense 3d field of training knowledge saved as embedded “weights” (unproven but this is our hypothesis based on the techniques that appear to be working)

-   Why

    -   We wanted to understand why LLMs are special and how the weights fit into this innovative technology.

    -   By choosing to spend our time trying to view what LLM weights are, we believe we can apply well-known visualization techniques for analyzing human brain scans to extract, identify, reuse and audit what the weights are.

    -   Before large generative AI Transformer weights were widely available, these types of dense, high resolution training datasets were very expensive and not frequently shared

-   How

    -   We built this prototype using digital signal processing algorithms (DSP) for volumetric analysis of high resolution data and combined the analysis engine with Blender (an open source visualization tool).

    -   We will open source and track how an AI learns from the ground up and use Blender to export and share what the weights look like as we go.

    -   By choosing to use Blender to analyze model weights in a 3d volume, we built in animation capabilities that let us design our initial v1 API for capturing a time series training dataset. This training dataset is focused on capturing how an AI foundational model learns through each training phase using high performance weight analysis on volumetric data.

    -   We believe we need to share how these models look so we can understand them and train AI’s to build and audit themselves.

    -   We want to see what mixtures of experts looks like too (download the newest Dolphin 2.5 Mixtral 8x7B STL/glTF mesh versions below).

### Overview

This repository is for profiling, extracting, visualizing and reusing generative AI weights to hopefully build more accurate AI models and audit/scan weights at rest to identify knowledge domains for risk(s).

![Viewing an Extracted Marching Cubes 3D Mesh from a Large Generative AI Model's Weights using Blender](https://raw.githubusercontent.com/matlok-ai/gen-ai-datasets-for-bampe-weights/main/docs/images/blender/gpt2-tensor-weights-in-blender.png)

Note: today's version only includes how to profile, extract and visualize existing model weights. Now that we can visualize how AI models learn, foundational model training is next. The training visualization will start by teaching a new AI model about "how the [bampe-weights repository](https://github.com/matlok-ai/bampe-weights/) integrated numpy, pandas and Blender". We have ~190 python/(task,prompt,answer) files to organize before sharing.

### What do extracted weights look like?

This repository is exploring visualizations of model's learning over time and building training datasets from extracted "weight shapes" to build and predict new AI model weights (hopefully faster than traditional training methods too).

Here's what Llama 2 7B Chat GPTQ looks like inside Blender and exported as a gif using this repository:

- [View extracted shapes from Llama 2 7B Chat GPTQ in a 75 MB gif - https://i.imgur.com/9vdATAt.mp4](https://i.imgur.com/9vdATAt.mp4)

#### Catalog of Available Generative AI Blender 3D Visualizations in glTF and STL files hosted on Google Drive

The following google drive folders contain the emerging index of large language model glTF and STL visualizations. The files range from ~1 MB to +2 GB.

Reach out if you want to see a new model/density!

- [Dolphin 2.5 Mixtral 8x7B GPTQ](https://drive.google.com/drive/folders/1xAO8vAi6NPVql8eye5RqsPntWO9xXDYV?usp=sharing)
- [Phind CodeLlama 34B v2 GPTQ](https://drive.google.com/drive/folders/1FhcG3fQzFJ_F36jZ3RiQccZTkhpHtNFx?usp=sharing)
- [DeepSeek Coder 34B GPTQ](https://drive.google.com/drive/folders/1uM498ZEUWj5s-89opmYJI7gnws3I1hc3?usp=sharing)
- [Mistral 7B OpenOrca GPTQ](https://drive.google.com/drive/folders/1Snnh8QO3X2VmwdTLHxij4higW90g17u2?usp=sharing)
- [Llama 2 7B Chat GPTQ](https://drive.google.com/drive/folders/1ZL85E_otE-X8ypb9znaVBhfmWq8chadR?usp=drive_link)
- [GPT 2](https://drive.google.com/drive/folders/1TlI14Ha5voglO4w__4CPVhNwmgk8rNj6?usp=drive_link)

#### Datasets on GitHub

##### Viewing STL Files on GitHub

If an STL file is small enough, then GitHub can automatically render the 3d meshes. Note: viewing GitHub STL on mobile is not ideal at the moment, but on a desktop you can zoom into the layers using a mouse wheel in reverse and rotate with the left/right mouse buttons:

- [Dolphin 2.5 Mixtral 8x7b](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/blob/main/docs/images/blender/dolphin-2.5-mixtral-8x7b/demo-dolphin-2.5-mixtral-8x7b-dim_512_shapes_500000_layers_2.stl)
- [Phind Code Llama 2 34B v2](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/blob/main/docs/images/blender/phind-34b-v2/demo-phind-34b-v2-dim_512_shapes_500000_layers_2.stl)
- [Mistral 7B OpenOrca](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/blob/main/docs/images/blender/mistral-7b-openorca/demo-mistral-7b-openorca-dim_512_shapes_500000_layers_2.stl)

##### GitHub Dataset Repository

We try to stay under the 50 MB limit and store assets on our [repo on GitHub - https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/docs/images/blender](https://github.com/matlok-ai/gen-ai-datasets-for-bampe-weights/tree/main/docs/images/blender)

### Using Blender to Visualize Generative AI Models the AI Training Process

#### Viewing Extracted Shapes from AI Model Weights Using a Blender Container Image

Self-host Blender in a container to help see what generative AI weights look like locally:

1.  Blender Demo Container Image with exported STL/GLB files already included

    The [matlok/blender-ai-demos](https://hub.docker.com/repository/docker/matlokai/blender-ai-demos/general) image was created from the [LinuxServer Blender image](https://github.com/linuxserver/docker-blender) and includes 3D STL and GLB files that you can view in a browser. The blender-ai-demos extracted container image is >4.0 GB on disk and uses about 3 GB ram to process STL or glTF files >40 MB:

    The demo visualizations are found in this directory inside the container:

    **/config/bampe-visualizations**

    **Docker**

    ```
    docker rm blender; docker-compose -f compose/blender-demos.yaml up -d
    ```

    **Podman**

    ```
    podman rm -t 0 -f blender; podman-compose -f compose/blender-demos.yaml up -d
    ```

1.  Base LinuxServer image

    Run the [LinuxServer/docker-blender image (lscr.io/linuxserver/blender:latest)](https://github.com/linuxserver/docker-blender/) and generate new STL/GLB files that are ready to view using an already-mounted volume between the host and the Blender container (**.blender** directory). The docker-blender extracted container image is ~3 GB on disk.

    **Docker**

    ```
    docker rm blender; docker-compose -f compose/blender-demos.yaml up -d
    ```

    **Podman**

    ```
    podman rm -t 0 -f blender; podman-compose -f compose/base.yaml up -d
    ```

    Note: newly-created visual artifacts (STL and glTF glb files) only show up once the container is restarted in this directory inside the Blender container:

    **/config/bampe**

1.  Open up Blender in a browser

    Blender is listening at this url:

    [http://localhost:3000](http://localhost:3000)

1.  Load a 3D Blender AI Visualization Manually

    Once Blender is running in the browser, you can import STL or glTF files by clicking these menus:

    1.  **File**

    2.  **Import**

    3.  **STL** or **glTF**

    4.  Files are either in the **/config/bampe** or **/config/bampe-visualizations** depending on the running container version

### Blender Navigation Mode Tips

#### Navigation Mode - Walk

- Use **Shift + `** to enable navigation mode with the mouse and W, A, S, D for first person movement.

- Holding the **Shift** button will move with turbo speed too.

#### Adjust Navigation Mouse Sensitivity and Walk Speed

1.  Open **Edit** -> **Preferences** -> **Navigation** -> **Fly & Walk** -> **Walk Toggle Arrow**

1.  Adjust **Mouse Sensitivity** -> **0.1**

1.  Adjust **Walk Speed** -> **20 m/s**

#### Viewing AI Models like a Video Game with Blender on the Command Line

##### Setting up a Development Environment

This repository is for researching alternative approaches to building AI using pretrained AI weights. It is a work in progress so please refer to the [Setting up a Development Environment](https://bampe-weights.readthedocs.io/en/latest/sdk/setting-up-a-development-environment/) for more details on running this from the command line.

### Where else can I view exported glTF and STL files?

We can share and view these shapes using online tools.

##### Online glTF viewers

- [https://gltf-viewer.donmccurdy.com/](https://gltf-viewer.donmccurdy.com/)

##### Online STL viewers

- [https://stlviewer.kwebpia.net](https://stlviewer.kwebpia.net)

### Supported Platforms

This repository was tested on the following platforms:

#### Windows WSL

- Blender 3 on Ubuntu 22.04 (apt package) - wsl2 Windows 11 gpu

#### Linux Ubuntu 22.04 Bare Metal

- Blender 4 on Ubuntu 22.04 (snap package) - hypervisor no gpu

#### Blender Container Image Sources

- [Demos - matlokai/blender-ai-demos](https://hub.docker.com/repository/docker/matlokai/blender-ai-demos/general)
- [Base - LinuxServer/docker-blender](https://github.com/linuxserver/docker-blender)
