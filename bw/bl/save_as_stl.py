import bpy
import logging


log = logging.getLogger(__name__)


def save_as_stl(
    output_path: str,
):
    """
    save_as_stl

    save the scene as an stl file

    https://docs.blender.org/api/current/bpy.ops.ex
    port_mesh.html#module-bpy.ops.export_mesh

    :param output_path: save the scene
        as an stl file at this local file path
    """
    log.info(f"saving stl={output_path}")
    bpy.ops.export_mesh.stl(
        filepath=output_path,
        # single file
        batch_mode="OFF",
        # use_selection=True
    )
