import logging
import bpy


log = logging.getLogger(__name__)


def apply_decimator(
    name: str, decimation_ratio: float = 0.5
):
    """
    apply_decimator

    a decimator in blender is beneficial for
    rendering performance because it reduces
    the polygon count of a 3D model. this
    optimization helps decrease the
    computational load during rendering,
    making the process faster and more
    efficient. The decimator simplifies complex
    geometry, maintaining the overall shape
    while reducing the number of vertices,
    edges, and faces. This is especially
    useful when working with intricate
    models or scenes to achieve a balance
    between visual quality and rendering speed.

    :param name: name of the object
        to decimate
    :param decimation_ratio: percent to
        reduce the object between 0.0 and 1.0
    """
    found_it = bpy.data.objects.get(name)
    if found_it is None:
        log.error(f"unable to find bpy object_name={name}")
        return False

    log.debug(
        "start "
        f"decimate=(name={name}, ratio={decimation_ratio})"
    )
    # Select the specified object
    bpy.context.view_layer.objects.active = (
        bpy.data.objects.get(name)
    )
    bpy.context.active_object.select_set(True)

    # Switch to Object mode
    bpy.ops.object.mode_set(mode="OBJECT")

    # Add a Decimate modifier
    bpy.ops.object.modifier_add(type="DECIMATE")
    decimate_modifier = bpy.context.object.modifiers[
        "Decimate"
    ]

    # Set the decimation ratio
    decimate_modifier.ratio = decimation_ratio

    # Apply the modifier to permanently modify the mesh
    bpy.ops.object.modifier_apply(
        {"object": bpy.context.active_object},
        modifier="Decimate",
    )
    log.debug(
        "done "
        f"decimate=(name={name}, "
        f"ratio={decimation_ratio})"
    )
    return True
