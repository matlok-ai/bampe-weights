import bpy


def set_render_settings(
    file_format: str = "PNG",
    color_mode: str = "RGB",
    color_depth: str = "8",
    use_zbuffer: bool = False,
    color_alpha: bool = False,
):
    """
    set_render_settings

    set common animation rendering properties
    like file format, color mode, color depth,
    and to use the z buffer

    :param file_format: type of animation image
    :param color_mode: RBG vs RBGA
    :param color_depth: '8' or '16' ('32' not
        supported)
    :param use_zbuffer: flag to use the z buffer
    :param color_alpha: flag to use alphaa
    """
    bpy.context.scene.render.image_settings.file_format = (
        file_format
    )
    bpy.context.scene.render.image_settings.color_mode = (
        color_mode
    )
    bpy.context.scene.render.image_settings.color_depth = (
        color_depth
    )
    # supported on 3.0, not 4.0
    """
    bpy.context.scene.render.image_settings.use_zbuffer = (
        use_zbuffer
    )
    """
    # bpy.context.scene.render.image_settings.color_alpha = 'RGBA' if color_alpha else 'RGB'
