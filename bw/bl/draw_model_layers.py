import os
import logging
import bw.np.extract_weights as extract_weights
import bw.bl.generate_3d_from_3d as mesh_gen
import bw.bl.create_rectangle as bwcr
import bw.bl.save_animation as bwan
import bw.bl.clear_all_objects as bwclear
import bw.bl.save_as_stl as export_stl
import bw.bl.save_as_gltf as export_gltf

log = logging.getLogger(__name__)


def draw_model_layers(
    input_file: str,
    layer_names: list = [],
    max_layers: int = 30,
    device: str = "cpu",
    target_faces: int = None,
    target_rows: int = 256,
    target_cols: int = 256,
    x: int = 0,
    y: int = 0,
    z: int = 1,
    rotate_z: float = None,
    max_depth: int = 2,
    pad_per: int = 20,
    save_gif: str = None,
    save_gltf: str = None,
    save_stl: str = None,
    output_dir: str = None,
    num_frames: int = 10,
    decimation_ratio: float = None,
    shutdown_after_animation: bool = False,
    auto_convert: bool = True,
    file_format: str = "PNG",
    color_depth: str = "8",
    color_mode: str = "RGBA",
    center_camera: bool = True,
    animation_y_move_speed: int = -200,
):
    """
    draw_model_layers

    render a model.safetensors file using
    blender by rescaling the model weights
    into polygons/shapes/faces and then
    drawing them in a resolution that
    hopefully can see the shapes (color
    is not supported for weights over
    512x512 in shape dimensions)

    :param input_file: path to model.safetensors
        file
    :param layer_names: filter by layer
        layer colomn names
    :param max_layers: limit the number of
        layers to render
    :param device: cpu vs gpu
    :param target_faces: min faces to
        hopefully render if there is
        enough data
    :param target_rows: number of
        resample target rows before
        drawing
    :param target_cols: number of
        resample target cols before
        drawing
    :param x: starting x axis location
        for all shapes
    :param y: starting y axis location
        for all shapes
    :param z: starting z axis location
        for all shapes
    :param rotate_z: starting z euler rotation
        in radians
    :param max_depth: stack each layer
        on itself this many times
        to convert it to a 3d ndarray
    :param pad_per: number to pad
        per object
    :param save_gif: optional - path to save
        the fly-through camera animation
        as a single gif
    :param save_gltf: optional - path to save
        the blender scene as a
        glTF file
    :param save_stl: optional - path to save
        the blender scene as an
        STL file
    :param output_dir: save outputs
        to this dir
    :param num_frames: number of animation
        key frames to show before saving a gif
    :param decimation_ratio: reduce each
        layer this percentage with supported values between
        0.0 and 1.0
    :param shutdown_after_animation: flag to
        shutdown the blender ui application
        after saving the animation
    :param auto_convert: flag to run ImageMagick
        to convert all temp animation images to
        a gif if set to True
    :param file_format: type of file for temp
        animation images ('PNG' vs 'TIFF' vs 'JPEG')
    :param color_depth: '8' bit vs '16' bit
    :param color_mode: 'RGBA' vs 'RBG'
    :param center_camera: flag to center
        the camera for animations based off
        the target dimensions
    :param animation_y_move_speed: how fast
        does the camera fly during the animation
    """
    obj_x = None
    obj_y = None
    obj_z = None
    mesh_cube_report = []

    log.info(
        f"start - model={input_file} "
        f"target.shape=({target_rows}, {target_cols}) "
        f"faces={target_faces} "
        f"max_layers={max_layers} "
        f"layers={len(layer_names)} "
        f"start pos=({x}, {y}, {z}) "
        f"rotate_z=radians({rotate_z}) "
        f"num_frames={num_frames} "
        f"output_dir={output_dir} "
        f"gif={save_gif} "
        ""
    )
    # extract the data using safetensors rust mmap
    all_data_3d = (
        extract_weights.extract_3d_shapes_from_model_file(
            input_file=input_file,
            layer_names=layer_names,
            max_layers=max_layers,
            device=device,
            target_faces=target_faces,
            target_rows=target_rows,
            target_cols=target_cols,
            start_x=x,
            start_y=y,
            start_z=z,
            max_depth=max_depth,
            pad_per=pad_per,
        )
    )

    # Clear existing mesh objects
    bwclear.clear_all_objects()

    x_max_text_len = 0
    num_datas = len(all_data_3d)
    log.info(f"rendering {num_datas} object shapes")
    for idx, data_3d in enumerate(all_data_3d):
        name = data_3d["name"]
        desc = data_3d["desc"]
        x_max_text_len = len(desc)
        data_to_render = data_3d["data"]
        target_faces = data_3d["target_faces"]
        obj_x = data_3d["x"]
        obj_y = data_3d["y"]
        obj_z = data_3d["z"]
        # shutdown blender for debugging issues
        # raise SystemExit
        log.info(
            f"rendering {idx + 1}/{num_datas} "
            f"{name} "
            f"pos=({obj_x}, {obj_y}, {obj_z})"
        )
        (
            mesh_name,
            mc_report,
        ) = mesh_gen.generate_3d_from_3d(
            name=f"Layer {idx + 1}: {name}",
            desc=desc,
            data=data_to_render,
            x=obj_x,
            y=obj_y,
            z=obj_z,
            target_faces=target_faces,
            mesh_idx=idx,
            decimation_ratio=decimation_ratio,
        )
        # active status
        status = 0
        if mc_report is None:
            log.info(
                f"ignoring {idx + 1}/{num_datas} " f"{name}"
            )
            # inactive status
            status = 1
        else:
            log.info(
                f"adding {idx + 1}/{num_datas} "
                f"{name} "
                f"pos=({obj_x}, {obj_y}, {obj_z}) "
            )
        mesh_cube_report.append(
            {
                "name": mesh_name,
                "status": status,
                "idx": idx,
                "layer_name": name,
                "target_faces": target_faces,
                "closest": mc_report,
                "data_3d": data_3d,
            }
        )
    # end of drawing 3d objects

    # calculate the center for the rectangle
    width_total = target_cols + 50
    width_center = x + int(width_total / 2)
    height_per_layer = pad_per + max_depth + 1
    height_total = len(mesh_cube_report) * height_per_layer
    height_total = (len(mesh_cube_report) * pad_per) + 5
    height_center = y + int(height_total / 2)

    if target_cols < 256:
        width_total = 280
        width_center = x + int(width_total / 2) - 5

    log.debug(
        "centering rectangle "
        f"width_total={width_total} "
        f"width_center={width_center} "
        f"max_desc_len={x_max_text_len} "
        f"height_total={height_total} "
        f"height_center={height_center} "
        f"height_per_layer={height_per_layer} "
        f"src pos=({x}, {y}, {z}) "
        f"dst pos=({x + width_center}, "
        f"{y + height_center - 10}, "
        f"{z})"
    )
    # Create background under the layers
    bwcr.create_rectangle(
        height=height_total,
        width=width_total,
        depth=0.1,
        hex_color="#000000",  # black
        opacity=1.0,
        x_position=x + width_center,
        y_position=y + height_center - 15,
        z_position=z,
    )

    # save the data to various locations
    if save_stl:
        export_stl.save_as_stl(output_path=save_stl)
        if not os.path.exists(save_stl):
            log.error(f"failed to save stl={save_stl}")
    if save_gltf:
        export_gltf.save_as_gltf(
            output_path=save_gltf, export_format="GLB"
        )
        if not os.path.exists(save_stl):
            log.error(f"failed to save gltf={save_gltf}")
    if save_gif:
        bwan.save_animation(
            save_gif=save_gif,
            output_dir=output_dir,
            frame_start=1,
            frame_end=num_frames,
            center_camera=center_camera,
            target_rows=target_rows,
            target_cols=target_cols,
            x_start=obj_x,
            y_start=y,
            z_start=obj_z,
            x_end=obj_x,
            y_end=y + 500,
            z_end=obj_z,
            x_move_speed=0,
            y_move_speed=animation_y_move_speed,
            z_move_speed=0,
            shutdown_after_animation=shutdown_after_animation,
            auto_convert=auto_convert,
            file_format=file_format,
            color_depth=color_depth,
            color_mode=color_mode,
        )
    return {
        "data_3d": all_data_3d,
        "mc": mesh_cube_report,
        "stl": save_stl,
        "gltf": save_gltf,
        "gif": save_gif,
    }


# end of draw_model_layers
