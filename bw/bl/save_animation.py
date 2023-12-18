import os
import logging
import bpy
import bw.bl.set_render_settings as set_render_settings
import bw.bl.set_background_color as set_background_color
import bw.bl.set_output_file as set_output_file
import bw.bl.set_camera_location_orientation as set_cam
import bw.bl.set_animation_parameters as set_animation


log = logging.getLogger(__name__)


def save_animation(
    save_gif: str,
    output_dir: str = None,
    frame_start: int = 1,
    frame_end: int = 2,
    center_camera: bool = True,
    target_rows: int = None,
    target_cols: int = None,
    x_start: int = -300,
    y_start: int = 0,
    z_start: int = 200,
    x_end: int = -300,
    y_end: int = 500,
    z_end: int = 200,
    x_move_speed: int = 0,
    y_move_speed: int = -10,
    z_move_speed: int = 0,
    shutdown_after_animation: bool = True,
    auto_convert: bool = True,
    file_format: str = "PNG",
    color_depth: str = "8",
    color_mode: str = "RGBA",
):
    """
    save_animation

    save the key frame animation to a gif
    after setting up the camera and temporary
    file storage

    :param save_gif: path to save the animation
        as a gif file
    :param center_camera: flag to center
        the camera for animations based off
        the target dimensions
    :param target_rows: number of rows for
        camera centering
    :param target_cols: number of columns for
        camera centering
    :param output_dir: temp directory
        for saving animation images before
        gif compilation
    :param frame_start: start frame idx
        usually 1
    :param frame_end: ending frame idx
    :param x_start: camera start x position
    :param y_start: camera start y position
    :param z_start: camera start z position
    :param x_end: camera end z position
    :param y_end: camera end z position
    :param z_end: camera end z position
    :param x_move_speed: speed the camera
        navigates from the
        x_start to the x_end position
    :param y_move_speed: speed the camera
        navigates from the
        y_start to the y_end position
    :param z_move_speed: speed the camera
        navigates from the
        z_start to the z_end position
    :param shutdown_after_animation: flag to
        shutdown after rendering the animation
        to a gif. helpful to set to
        False if there are no shapes
        in the gif. in blender you can see the
        camera's location and route for debugging.
    :param auto_convert: flag to run ImageMagick
        to convert all temp animation images to
        a gif if set to True
    :param file_format: type of file for temp
        animation images ('PNG' vs 'TIFF' vs 'JPEG')
    :param color_depth: '8' bit vs '16' bit
    :param color_mode: 'RGBA' vs 'RBG'
    :raises SystemExit: if the shutdown_after_animation
        flag is set to True, this will exit blender after
        saving the gif or if the output directory
        failed creation. if blender exits, then it will
        be difficult to debug camera
        location/pathing issues.
    """
    if center_camera:
        cam_start_x = x_start
        cam_start_y = y_start
        cam_start_z = z_start
        cam_end_x = x_end
        cam_end_y = y_end
        cam_end_z = z_end

        if target_rows and target_cols:
            # works for 50x50
            # rows on the x-axis
            center_x = int(target_rows) - 5
            # cols on the z-axis
            center_z = int(target_cols) - 10
            # larger than 128x128 divide in half
            if target_rows > 128:
                center_x = int(int(target_rows) / 2)
            if target_cols > 128:
                center_z = int(int(target_cols) / 2)
            log.info(
                "animation camera centering "
                ""
                f"mesh_pos=({x_start}, "
                f"{y_start}, "
                f"{z_start}) "
                ""
                "cam_pos=("
                f"{cam_start_x + center_x}, "
                f"{cam_start_y}, "
                f"{cam_start_z + center_z}) "
                f"x={cam_start_x} "
                f"x_center={center_x} "
                f"z={cam_start_z} "
                f"z_center={center_z}"
            )
            cam_start_x += center_x
            cam_end_x += center_x
            cam_start_z += center_z
            cam_end_z += center_z
        else:
            log.info("using cam defaults")
        x_start = cam_start_x
        y_start = cam_start_y
        z_start = cam_start_z
        x_end = cam_end_x
        y_end = cam_end_y
        z_end = cam_end_z
    # end center_camera

    log.info(
        f"saving frames=[{frame_start}, {frame_end}] "
        f"gif={save_gif} center={center_camera} "
        f"start camera=({x_start}, {y_start}, {z_start}) "
        f"end camera=({x_end}, {y_end}, {z_end}) "
        f"speed=(x={x_move_speed}, y={y_move_speed}, "
        f"z={z_move_speed}) "
        f"shutdown={shutdown_after_animation} "
        f"output_dir={output_dir} "
        ""
    )
    if not save_gif:
        log.info(f"no gif to save={save_gif}")
        return
    # Set the output directory and file name
    if not output_dir:
        output_dir = os.getenv("GIF_DIR", "./.tmp")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if not os.path.exists(output_dir):
        log.error(
            f"unable to create output dir: {output_dir} - stopping"
        )
        raise SystemExit
    output_file = save_gif
    output_path = output_file

    camera_name = "Camera"
    tmp_output_path = f"{output_dir}/temp_frame_"
    set_render_settings.set_render_settings(
        file_format=file_format,
        color_mode=color_mode,
        color_depth=color_depth,
        use_zbuffer=False,
        color_alpha=False,
    )
    set_background_color.set_background_color(
        use_alpha=False,
        world_r=1.0,
        world_g=1.0,
        world_b=1.0,
    )
    set_output_file.set_output_file(
        filepath=tmp_output_path,
        file_format=file_format,
    )
    set_cam.set_camera_location_orientation(
        name=camera_name,
        x_start=x_start,
        y_start=y_start,
        z_start=z_start,
        x_end=x_end,
        y_end=y_end,
        z_end=z_end,
    )
    set_animation.set_animation_parameters(
        frame_start=frame_start,
        frame_end=frame_end,
        x_start=x_start,
        y_start=y_start,
        z_start=z_start,
        x_move_speed=x_move_speed,
        y_move_speed=y_move_speed,
        z_move_speed=z_move_speed,
    )
    # determine num frames after detection
    sc_frame_start = bpy.context.scene.frame_start
    sc_frame_end = bpy.context.scene.frame_end
    num_frames = sc_frame_end - sc_frame_start
    log.info(f"rendering animation for {num_frames} frames")
    # automated render animation
    bpy.ops.render.render(animation=True)
    # convert frames to gif using an external tool like ImageMagick
    if auto_convert:
        vc = (
            f"convert -delay 2 -loop 0 "
            f"{output_dir}/temp_frame_*.png "
            f"{output_path}"
        )
        if file_format == "TIFF":
            vc = (
                f"convert -delay 2 -loop 0 "
                f"{output_dir}/temp_frame_*.tif "
                f"{output_path}"
            )
        elif file_format == "JPEG":
            vc = (
                f"convert -delay 2 -loop 0 "
                f"{output_dir}/temp_frame_*.jpeg "
                f"{output_path}"
            )
        log.info(
            f"saving frames={num_frames} animation with command: {vc}"
        )
        os.system(vc)
    else:
        log.info("not converting gif")
    # clean up temporary frames
    for item in bpy.data.images:
        log.info(f"cleaning up animation images: {item}")
        if item.name.startswith("temp_frame_"):
            bpy.data.images.remove(item)
    if shutdown_after_animation:
        log.info("animation done - shutting down")
        raise SystemExit
    log.info(f"done saving gif={save_gif}")
    return
