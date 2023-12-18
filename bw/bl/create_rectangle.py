import bpy
import logging


log = logging.getLogger(__name__)


def create_rectangle(
    height: int,
    width: int,
    depth: int,
    hex_color: str,
    opacity: float,
    x_position: int,
    y_position: int,
    z_position: int,
):
    """
    create_rectangle

    create a 3d rectangle by x, y, z with
    rgba support

    :param height: height of the object
    :param width: width of the object
    :param depth: depth of the object
    :param hex_color: hex color string
    :param opacity: transparency
    :param x_position: x location
    :param y_position: y location
    :param z_position: z location
    """
    color = tuple(
        int(hex_color[i : i + 2], 16) / 255.0
        for i in (1, 3, 5)
    )
    log.debug(
        "creating rectangle("
        f"x={x_position}, "
        f"y={y_position}, "
        f"z={z_position}, "
        f"dep={depth}"
    )

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(x_position, y_position, z_position),
    )
    rectangle = bpy.context.active_object
    rectangle.dimensions = (width, height, depth)

    material = bpy.data.materials.new(
        name="Rectangle_Material"
    )
    rectangle.data.materials.append(material)
    material.use_nodes = False

    material.diffuse_color = color + (opacity,)

    log.debug("done")
