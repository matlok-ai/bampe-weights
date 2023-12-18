import bpy
import logging


log = logging.getLogger(__name__)


def save_as_gltf(
    output_path: str,
    export_format: str = "GLB",
):
    """
    save_as_gltf

    save the scene as a gltf file

    https://docs.blender.org/api/current/bpy.ops.
    export_scene.html#bpy.ops.export_scene.gltf

    **Output Format**

    - **GLB** - glTF Binary (.glb)

      Exports as a single file, with all data packed
      in binary form. Most efficient and portable, but
      more difficult to edit later.

    - **GLTF_SEPARATE** - glTF separate files (.gltf + .bin + textures)

      Exports multiple files, with separate JSON,
      binary and texture data. Easiest to edit later.


    :param output_path: save the scene
        as a gltf file at this local file path
    :param export_format: use a single file
        with GLB and multiple files with
        GLTF_SEPARATE
    """
    log.info(
        f"saving gltf={output_path} "
        f"format={export_format}"
    )
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format=export_format,
        export_animations=True,
    )
