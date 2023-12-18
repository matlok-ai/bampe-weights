import bpy


def set_output_file(
    filepath: str = "./.tmp/temp_frame_",
    file_format: str = "RBGA",
):
    """
    set_output_file

    set the animation temporary file output paths

    :param filepath: path to save the temp files
    :param file_format: format to use when
        saving files during the animation
    """
    bpy.context.scene.render.filepath = filepath
    bpy.context.scene.render.image_settings.file_format = (
        file_format
    )
