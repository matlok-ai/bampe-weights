import os
import bpy


def hex_to_rgb(hex_color: str):
    """
    hex_to_rgb

    convert hex to floats returned in a tuple (r,b,g)

    :param hex_color: hexidecimal color string
    """
    return tuple(
        int(hex_color[i : i + 2], 16) / 255.0
        for i in (1, 3, 5)
    )


def add_text(
    text: str,
    position: tuple = (0, 0, 0),
    font_size: int = 8,
    font_style: str = None,
    font_family_path: str = None,
    color: str = "#FFFFFF",
    opacity: float = 1.0,
    extrude: float = 0.1,
    bevel_depth: float = 0.05,
):
    """
    add_text

    add a text string at x, y, z with opacity

    :param text: message to show in blender
    :param position: (x, y, z) integer location
        for the text
    :param font_size: size of the font
    :param font_style: style for the font
        like BOLD
    :param font_family_path: optional path to the
        font family file to use
    :param color: hex color string for the text
    :param opacity: alpha color for the text
    :param extrude: amount to extend the text
    :param bevel_depth: amount to curve the text
        edges
    """
    bpy.ops.object.text_add(
        enter_editmode=False,
        align="WORLD",
        location=position,
    )
    text_obj = bpy.context.active_object
    text_obj.data.body = text
    text_obj.data.size = font_size
    if font_family_path and os.path.exists(
        font_family_path
    ):
        text_obj.data.font = bpy.data.fonts.load(
            font_family_path
        )
    if font_style:
        # font_sytyle = 'BOLD'
        text_obj.data.style = font_style

    rgb_tuple = hex_to_rgb(color)
    rgba_color = (
        rgb_tuple[0],
        rgb_tuple[1],
        rgb_tuple[2],
        opacity,
    )
    """
    # for debugging
    print(rgba_color)
    """
    text_obj.color = rgba_color

    text_obj.data.extrude = (
        extrude  # Adjust extrude value as needed
    )

    bpy.ops.object.convert(target="MESH")

    # Select the newly created mesh object
    bpy.context.view_layer.objects.active = (
        bpy.context.scene.objects[text_obj.data.name]
    )

    # Set material properties
    mat = bpy.data.materials.new(name="TextMaterial")
    mat.use_nodes = False
    mat.diffuse_color = rgba_color

    text_obj.data.materials.append(mat)
