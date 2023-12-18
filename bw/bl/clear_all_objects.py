import logging
import bpy


log = logging.getLogger(__name__)


def clear_all_objects():
    """
    clear_all_objects

    clear all objects in the blender env
    """
    log.debug("start")
    # clear all mesh objects from the scene
    bpy.ops.object.select_all(action="DESELECT")
    # iterate through all objects in the scene
    for obj in bpy.context.scene.objects:
        # optional filtering by names
        # if obj.type == 'MESH' or (obj.type == 'MESH' and obj.name == 'Cube'):
        if obj.type == "MESH":
            obj.select_set(True)

    # delete selected objects
    bpy.ops.object.delete()
