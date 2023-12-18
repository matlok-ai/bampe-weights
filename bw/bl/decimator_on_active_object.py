import logging
import bpy


log = logging.getLogger(__name__)


def apply_decimator_to_object(
    active_object,
    reduce_percentage: float = 0.5,
):
    """
    apply_decimator_to_object

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

    :param active_object: set this
        to the blender active object to decimate (reduce)
        active_object=bpy.context.active_object
    :param reduce_percentage: set the target
        reduction percentage as a value between 0.0 and 1.0
    """
    log.info("start reduce={reduce_percentage}")
    modifier = active_object.modifiers.new(
        name="Decimate", type="DECIMATE"
    )

    # Adjust the ratio based on your decimation requirements
    modifier.ratio = reduce_percentage

    # Apply the modifier to permanently modify the mesh
    bpy.ops.object.modifier_apply(
        {"object": active_object}, modifier="Decimate"
    )
    log.info("done reduce={reduce_percentage}")
