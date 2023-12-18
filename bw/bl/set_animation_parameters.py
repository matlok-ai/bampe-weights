import bpy


def set_animation_parameters(
    name: str = "Camera",
    frame_start: int = 1,
    frame_end: int = 10,
    x_start: int = -300,
    y_start: int = 100,
    z_start: int = 200,
    x_move_speed: int = 0,
    y_move_speed: int = -100,
    z_move_speed: int = 0,
):
    """
    set_animation_parameters

    set the animation configuration

    :param name: name of the camera
        bpy.data.objects[name]
    :param frame_start: start frame index
    :param frame_end: end frame index
    :param x_start: camera start x
    :param y_start: camera start y
    :param z_start: camera start z
    :param x_move_speed: camera x move speed
    :param y_move_speed: camera x move speed
    :param z_move_speed: camera x move speed
    """
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    # Create a new animation data block
    animation = bpy.data.actions.new(name="CameraAnimation")
    bpy.data.objects[name].animation_data_create()
    bpy.data.objects[name].animation_data.action = animation

    # Adjust the camera clipping distance
    bpy.data.objects[
        name
    ].data.clip_start = 0.1  # Set the near clipping distance (adjust as needed)
    # < 64x64 the clipping distance will show more
    bpy.data.objects[
        name
    ].data.clip_end = 600.0  # Set the far clipping distance (adjust as needed)

    # Set other camera properties if necessary
    bpy.data.objects[
        name
    ].data.lens = 25.0  # Adjust the focal length if needed

    bpy.context.scene.frame_set(
        bpy.context.scene.frame_start
    )
    # Move the camera in the x axis
    bpy.data.objects[name].location.x = x_move_speed
    # Move the camera in the y axis
    bpy.data.objects[name].location.y += y_move_speed
    # Move the camera in the z axis
    bpy.data.objects[name].location.z = z_move_speed
    bpy.data.objects[name].keyframe_insert(
        data_path="location", index=1
    )

    # Create a new keyframe for the camera location and rotation
    bpy.context.scene.frame_set(bpy.context.scene.frame_end)
    bpy.data.objects[name].location = (
        x_start,
        y_start,
        z_start,
    )
    bpy.data.objects[name].keyframe_insert(
        data_path="location", index=1
    )
    # Set up rendering parameters
