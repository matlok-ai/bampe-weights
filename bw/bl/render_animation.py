import bpy
import logging


log = logging.getLogger(__name__)


def render_animation(
    save_gif: bool = False, gif_path: str = None
):
    """
    render_animation

    render the animation frames and save as
    a gif if set

    :param save_gif: flag to enable saving
        the animation as a gif
    :param gif_path: path to save the gif
    """
    if save_gif:
        log.debug("saving gif={save_gif}")
        bpy.context.scene.render.filepath = gif_path
        bpy.ops.render.render(animation=True)
        bpy.ops.image.save_as(
            {
                "active_object": bpy.data.images[
                    "Render Result"
                ]
            },
            copy=True,
            filepath=gif_path,
            check_existing=False,
        )
    else:
        log.debug("not saving gif={save_gif}")
        bpy.ops.render.render(animation=True)
