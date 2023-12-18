import bpy


def set_background_color(
    use_alpha: bool = False,
    world_r: float = 0.0,
    world_g: float = 0.0,
    world_b: float = 0.0,
):
    """
    set_background_color

    set the background color for easier animations

    :param use_alpha: flag to set the animations
        as transparent
    :param world_r: world decimal red value
    :param world_g: world decimal green value
    :param world_b: world decimal blue value
    """
    bpy.context.scene.render.film_transparent = use_alpha
    bpy.context.scene.view_settings.view_transform = (
        "Standard"
    )
    bpy.context.scene.view_settings.look = "None"
    bpy.context.scene.view_settings.exposure = 0.0
    bpy.context.scene.view_settings.gamma = 0.1
    bpy.context.scene.view_settings.view_transform = (
        "Standard"
    )
    bpy.context.scene.world.use_nodes = False
    """
    # does not work on 4.0, works on 3.0
    bpy.context.scene.world.light_settings.use_ambient_occlusion = (
        True
    )
    """
    # Set color in world
    bpy.context.scene.world.color = (
        world_r,
        world_g,
        world_b,
    )
