## Blender Install Notes

Please refer to the [Official Blender Install guide](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html#download-blender).

Here are our notes from getting a couple self-hosted instances running (untested on Mac OS X).

### Install Packages

```bash
sudo apt install build-essential git subversion cmake libx11-dev libxxf86vm-dev libxcursor-dev libxi-dev libxrandr-dev libxinerama-dev libglew-dev libwayland-dev wayland-protocols libegl-dev libxkbcommon-dev libdbus-1-dev linux-libc-dev bison libtool yasm patchelf texinfo
```

### Install Blender on the Command Line

#### Blender 4.0 - Hypervisor Ubuntu 22.04 without GPU

If your system can support Blender 4.0, here's how to install it:

```bash
snap install blender --classic
```

#### Blender 3.0 - WSL 2 Windows 11 Ubuntu 22.04 with GPU

Until this [issue](https://devtalk.blender.org/t/ubuntu-22-04-lts-alsoft-ee-failed-to-set-real-time-priority-blender-crashes/30413) is fixed 3.0 is the preferred option for WSL 2.

```bash
sudo apt-get install -y blender
```

Reach out if you know how to fix this error for Blender version 4.0:

```bash
blender
EGL Error (0x3009): EGL_BAD_MATCH: Arguments are inconsistent (for example, a valid context requires buffers not supplied by a valid surface).
Segmentation fault
```

### Prepare the Blender Python Runtime and Custom Modules

Going forward, please make sure to use the correct version when running theses commands:

```bash
mkdir -p ~/.config/blender/3.0/scripts/modules
mkdir -p ~/.config/blender/4.0/scripts/modules
```

#### Install Pips into Blender Scripts Modules Directory

Install the pips using only pip3.10 (the version Blender supports):

```bash
pip3.10 install -t ~/.config/blender/3.0/scripts/modules scikit-image numexpr seaborn scipy safetensors numpy torch matplotlib
pip3.10 install -t ~/.config/blender/4.0/scripts/modules scikit-image numexpr seaborn scipy safetensors numpy torch matplotlib
```

#### Optional - Install Development Bampe Weights for Blender's Python Runtime

Link the bampe weights into the Blender modules directory:

```bash
ln -s $(pwd)/bw ~/.config/blender/3.0/scripts/modules/
ln -s $(pwd)/bw ~/.config/blender/4.0/scripts/modules/
```

#### Confirm your Blender environment is ready for extracting model weights

```bash
ls -lrth ~/.config/blender/3.0/scripts/modules/safetensors/
ls -lrth ~/.config/blender/4.0/scripts/modules/safetensors/
```

### Visualize an AI Model's Weights from a Local model.safetensors File

By default the following command will analyze and render a 3d mesh from the default environment variable values:

```bash
time blender -p 400 400 800 800 --python ./examples/show-model.py
rm -rf .tmp/*; time blender -p 400 400 800 800 --python ./examples/show-model.py
```

