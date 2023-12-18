import bpy
import math
import logging


log = logging.getLogger(__name__)


def set_camera_location_orientation(
    name: str = "Camera",
    x_start: int = -300,
    y_start: int = 100,
    z_start: int = 200,
    x_end: int = -300,
    y_end: int = 500,
    z_end: int = 200,
    x_rotation: int = 90,
    y_rotation: int = 0,
    z_rotation: int = 0,
):
    """
    set_camera_location_orientation

    set up a named camera for navigating
    a path through blender by
    setting the start position (x, y, z) and
    end position (x, y, z) with an initial
    viewing angle (in radians for (x, y, z))

    :param name: camera name in
        bpy.data.objects[name]
    :param x_start: camera start x position
    :param y_start: camera start y position
    :param z_start: camera start z position
    :param x_end: camera end x position
    :param y_end: camera end y position
    :param z_end: camera end z position
    :param x_rotation: camera rotation angle
        for viewing in math.radians(x_rotation)
    :param y_rotation: camera rotation angle
        for viewing in math.radians(y_rotation)
    :param z_rotation: camera rotation angle
        for viewing in math.radians(z_rotation)
    """

    # Create a look at target
    bpy.data.objects[name].location = (
        x_start,
        y_start,
        z_start,
    )
    look_at_target = bpy.data.objects.new(
        "LookAtTarget", None
    )
    bpy.context.collection.objects.link(look_at_target)
    look_at_target.location = (x_end, y_end, z_end)

    # Set up the camera constraints
    log.debug(
        f"setting camera={name} "
        f"start=({x_start}, {y_start}, {z_start}) "
        f"look_at=({x_end}, {y_end}, {z_end}) "
        f"end=({x_end}, {y_end}, {z_end}) "
        f"angle=({x_rotation}, {y_rotation}, {z_rotation})"
    )
    bpy.context.scene.camera = bpy.data.objects[name]
    track_constraint = bpy.data.objects[
        name
    ].constraints.new("TRACK_TO")
    track_constraint.target = look_at_target
    track_constraint.track_axis = "TRACK_NEGATIVE_Z"
    track_constraint.up_axis = "UP_Y"
    bpy.data.objects[name].rotation_euler = (
        math.radians(x_rotation),
        math.radians(y_rotation),
        math.radians(z_rotation),
    )
