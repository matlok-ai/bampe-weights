# Blender APIs

These api's were designed and built for training a foundational Blender AI model.

## Blender Foundational AI Model Visualization

Visualize how a foundational model learns in blender

::: bw.bl.run_ai_training_visualizer

### Draw Model Weight Layers in a 3D Marching Cubes Mesh

Load a model's weights into blender

::: bw.bl.draw_model_layers

### Draw 3D mesh from 3D array

Create a 3d marching cubes representation as a mesh from a 3d array

::: bw.bl.generate_3d_from_3d

## Blender 3D Object APIs

Here are the supported 3d apis.

### Assign Colors based off Weighted Value vs rest of the 3D array

::: bw.bl.assign_color

### Assign Material

::: bw.bl.assign_material

### Add Colorized 3D Rectangle, Cube, or Wall in Blender

Add a 3d rectangle, cube or wall.

::: bw.bl.create_rectangle

### Add Colorized 3D Text in Blender

Convert a text string to a 3d text message in blender at an (x, y, z) position with coloring, font style, size and extrusion depth

::: bw.bl.add_text

### Clear all Objects in Blender

Remove all objects in the blender workspace

::: bw.bl.clear_all_objects

## Decimators

### Reduce the Active Object with a Blender Decimator

Note: decimators are great because they reduce the host requirements to run the visualizer, but they also remove a ton of shape details. Use at your own risk. This is why the [skimage.measure.marching_cubes](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.marching_cubes) algorithm is used for preprocess shape (vertices, faces, normals, values) detection before decimation and coloring.

Using a decimator in Blender is beneficial for rendering performance because it reduces the polygon count of a 3D model. This optimization helps decrease the computational load during rendering, making the process faster and more efficient. The decimator simplifies complex geometry, maintaining the overall shape while reducing the number of vertices, edges, and faces. This is especially useful when working with intricate models or scenes to achieve a balance between visual quality and rendering speed.

::: bw.bl.decimator_on_object

::: bw.bl.decimator_on_active_object

## Blender 3D Camera and Animation APIs

### Render Camera Animation

Render the camera animation key frames.

::: bw.bl.render_animation

### Save Camera Animation as a GIF

Note: saving a gif animation over many **FRAMES** is resource intensive. Please monitor utilization.

::: bw.bl.save_animation

### Set up Animation for Camera and Key Frames

Set up the animation configuration

::: bw.bl.set_animation_parameters

### Set the Background Color for the Animation

::: bw.bl.set_background_color

### Set the Camera Orientation (Location and Direction)

::: bw.bl.set_camera_location_orientation

### Set the Output File for the Animation

::: bw.bl.set_output_file

### Set the Camera and World Render Settings

::: bw.bl.set_render_settings

## Coloring APIs

Colors are disabled when rendering models with greater than 2000 faces.

### Assign Colors based off Quantile Ranges

::: bw.bl.get_quantile_colors

### Color Map

::: bw.bl.colors

## Export Scene to Other Formats

### Save as STL

Note: GitHub can automatically show small STL files.

```bash
export STL=./blender/example-model.stl
```

::: bw.bl.save_as_stl

### Save as glTF

```bash
export GLTF=./blender/example-model-gltf
```

::: bw.bl.save_as_gltf
