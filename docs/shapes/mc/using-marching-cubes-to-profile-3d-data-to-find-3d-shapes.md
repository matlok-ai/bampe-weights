# 3D Shape Detection Techniques

For v1, instead of using a traditional decimator-only approach for shape reduction, the current tool uses [skimage.measure.marching_cubes](https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.marching_cubes) to find a targeted number of shapes in the 3d data (nearest without going over) before coloring and rendering (preprocessing).

## Marching Cubes

::: bw.sk.profile_data_with_cubes
