import os
import datetime
import logging
import bw.bl.draw_model_layers as draw_layers
import bpy


log = logging.getLogger(__name__)


def run_ai_training_visualizer(
    model_file: str = None,
    num_gen: int = None,
    target_faces: int = None,
    target_rows: int = None,
    target_cols: int = None,
    layer_names: str = None,
    max_layers: int = None,
    save_gif: str = None,
    save_gltf: str = None,
    save_stl: str = None,
    num_frames: int = None,
    output_dir: str = None,
    decimation_ratio: float = None,
    shutdown: bool = None,
):
    """
    run_ai_training_visualizer

    extract a model.safetensors file with mmap (fast)
    then perform matrix transformations to convert all
    the 2d array (model weights) to a 3d array
    for showing in blender using skimage.meaure.marching_cubes

    supports saving an animation of flying through the
    3d model weights as a gif (note: thie takes a lot of
    cpu/ram tested on 12 cpu, 23 gb ram)

    :param model_file: path to model.safetensors file
        and uses the MODEL
        environment variable
        (e.g. export MODEL="./model.safetensors")
    :param num_gen: number of generations to run
        the training visualization through
        and uses the NUM_GEN
        environment variable
        (e.g. export NUM_GEN=5)
    :param target_faces: number of polygon faces
        to extract and draw per tensor weight
        and uses the FACES
        environment variable
        (e.g. export FACES=20000)
    :param target_rows: number of rows (width) for
        the 3d array in blender and the gif
        and uses the ROWS
        environment variable
        (e.g. export ROWS=256)
    :param target_cols: number of columns (height) for
        the 3d array in blender and the gif
        and uses the COLS
        environment variable
        (e.g. export COLS=256)
    :param layer_names: comma-delimited list of layers
        in the model weights to include in blender
        and the gif
        and uses the LAYER_NAMES
        environment variable
        (e.g. export LAYER_NAMES="h.2.,h.3.")
    :param max_layers: number of layers to display
        in blnder and the gif
        and uses the MAX_LAYERS
        environment variable
        (e.g. export MAX_LAYERS=5)
    :param save_gif: set to a file path and each
        visualization loop will save the camera's
        flying animation as a gif
        and uses the GIF
        environment variable
        (e.g. export GIF="./blender/view-model")
    :param save_gltf: optional - path to save
        the blender scene as a
        glTF file
    :param save_stl: optional - path to save
        the blender scene as an
        STL file
    :param num_frames: number of frames for the
        animation
        and uses the FRAMES
        environment variable
        (e.g. export FRAMES=5)
    :param output_dir: output directory for temporary
        animation image files (PNG or TIFF 16 bit)
        and uses the OUTPUT_DIR
        environment variable
        (e.g. export OUTPUT_DIR="./.tmp")
    :param decimation_ratio: reduce each
        layer this percentage with supported values between
        0.0 and 1.0
    :param shutdown: flag to automatically shutdown
        blender after each visualization loop
        and uses the SHUTDOWN_ENABLED
        environment variable
        (e.g. export SHUTDOWN_ENABLED="1")
    :raises SystemExit: thrown to shutdown blender
        without using the mouse
    """
    # https://blender.stackexchange.com/questions/5208/prevent-splash-screen-from-being-shown-when-using-a-script
    bpy.context.preferences.view.show_splash = False
    timeseries_training_data = []
    use_layer_names = []
    total_gens = "inf"
    if model_file is None:
        model_file = os.getenv(
            "MODEL", "./model.safetensors"
        )
        if model_file == "":
            log.error(
                f"missing required model_file={model_file}"
            )
    if not os.path.exists(model_file):
        log.error(f"failed to find model_file={model_file}")
        return None
    if num_gen is None:
        num_gen = int(os.getenv("NUM_GEN", "1"))
    if target_rows is None:
        # set a target row/column for compressing very large
        # tensor weights to a common resolution for viewing in 3d
        # note: camera/animation untested under 50x50 for now
        target_rows = int(os.getenv("ROWS", "256"))
    if target_cols is None:
        target_cols = int(os.getenv("COLS", "256"))
    if layer_names is None:
        # comma-delimited prefix (with wildcard) layer names to include
        test_layer = os.getenv("LAYER_NAMES", None)
        if test_layer:
            layer_names = test_layer.split(",")
        # by default 0/None will show all model layers
    else:
        use_layer_names = layer_names.split(",")
    if max_layers is None:
        max_layers_org = os.getenv("MAX_LAYERS", None)
        if max_layers_org and len(max_layers_org) > 0:
            max_layers = int(max_layers_org)
    if target_faces is None:
        # more faces/shapes uses more cpu + ram
        target_faces = int(os.getenv("FACES", "20000"))
    if num_frames is None:
        # more faces/shapes uses more cpu + ram
        # ~3 min to save a gif of 60 frames with 12 cpu 24GB ram
        num_frames = int(os.getenv("FRAMES", "5"))
    if save_gif is None:
        # more faces/shapes uses more cpu + ram
        # save the animation gif to this path
        save_gif = os.getenv("GIF", None)
    if save_stl is None:
        save_stl = os.getenv("STL", None)
    if save_gltf is None:
        save_gltf = os.getenv("GLTF", None)
    if output_dir is None:
        # more faces/shapes uses more cpu + ram
        # save animation temp images in this directory
        output_dir = os.getenv("OUTPUT_DIR", "./.tmp")
    if decimation_ratio is None:
        # decimation will remove a lot of shape granularity
        # but it will hopefully? work on more diverse hardware
        decimation_ratio_val = os.getenv("DECIMATION", None)
        if (decimation_ratio_val is not None) and (
            decimation_ratio_val != ""
        ):
            decimation_ratio = float(decimation_ratio_val)

    # shutdown the blender ui if set to 1 (for automating gifs)
    if shutdown is None:
        if os.getenv("SHUTDOWN_ENABLED", "0") == "1":
            shutdown = True

    cur_idx = 0
    raise_ex = False
    not_done = True
    while not_done:
        # python 3.12 utc dates
        utc_now = datetime.datetime.now(
            datetime.timezone.utc
        )
        utc_str = utc_now.strftime("%Y-%m-%dT%H:%M:%S")
        try:
            # support for many versions
            # over time with the same file prefix
            use_gif = None
            use_stl = None
            use_gltf = None
            # requires more hardware to do gifs
            if save_gif:
                if num_gen == 1:
                    use_gif = save_gif
                else:
                    use_gif = f"{save_gif}.{cur_idx}.gif"
            if save_stl:
                if num_gen == 1:
                    use_stl = save_stl
                else:
                    use_stl = f"{save_stl}.{cur_idx}.stl"
            if save_gltf:
                if num_gen == 1:
                    use_gltf = save_gltf
                else:
                    use_gltf = f"{save_gltf}.{cur_idx}"

            log.info(
                "start "
                f"gen={cur_idx}/{total_gens} "
                f"model={model_file} "
                f"faces={target_faces} "
                f"target=({target_rows}, {target_cols}) "
                f"layers={','.join(use_layer_names)} "
                f"max_layers={max_layers} "
                f"gif={use_gif} "
                f"gltf={use_gltf} "
                f"stl={use_stl} "
                f"frames={num_frames} "
                f"output_dir={output_dir} "
                f"decimation={decimation_ratio} "
                f"shutdown={shutdown} "
                ""
            )

            # visualize and create shapes report for training
            # and export artifacts for timeseries animations
            training_report = draw_layers.draw_model_layers(
                input_file=model_file,
                layer_names=use_layer_names,
                target_rows=target_rows,
                target_cols=target_cols,
                target_faces=target_faces,
                max_layers=max_layers,
                num_frames=num_frames,
                output_dir=output_dir,
                save_gif=use_gif,
                save_stl=use_stl,
                save_gltf=use_gltf,
                decimation_ratio=decimation_ratio,
                shutdown_after_animation=False,
            )
            data_row = {
                "date": utc_str,
                "report": training_report,
            }
            timeseries_training_data.append(data_row)
            if cur_idx >= num_gen:
                log.info(
                    f"hit iteration {cur_idx}/{num_gen}"
                )
                if shutdown:
                    # shutdown blender
                    log.info("shutting down blender")
                    raise SystemExit
                log.info("shutting down blender")
                break
            if shutdown:
                # shutdown blender
                log.info("shutting down blender")
                raise SystemExit
        # send shutdown
        except SystemExit as f:
            # force shut down
            if raise_ex:
                log.info(
                    "draw_model_shapes catching SystemExit - "
                    "shutting down"
                )
                not_done = False
            else:
                log.info(f"detected shut down ex={f}")
                raise f
        except Exception as e:
            log.error(
                f"draw_model_shapes not handling ex={e}"
            )
            raise e
        # coming soon - visualize model in a training/learning loop
        # train ai
        # export to gltf/stl
        not_done = False
    # end of while loop

    # review detected shapes through training generations
    for pidx, parent_node_org in enumerate(
        timeseries_training_data
    ):
        report_node = parent_node_org["report"]
        num_training_data = len(timeseries_training_data)
        for idx, row in enumerate(report_node["data_3d"]):
            profiled_mc_report = parent_node_org["report"][
                "mc"
            ][idx]
            layer_name = row["name"]
            mc_status = profiled_mc_report["status"]
            if mc_status == 1:
                log.info(
                    "skipped training data "
                    f"gen={idx}/{num_training_data} "
                    f"layer={layer_name}"
                )
                continue
            row_data = row["data"]
            mesh_name = profiled_mc_report["name"]
            mesh_idx = profiled_mc_report["idx"]
            mc_report = profiled_mc_report["closest"]
            mc_size_mb = mc_report["size"]
            mc_level = mc_report["level"]
            mc_step_size = mc_report["step_size"]

            # store these in a database and use
            # bampe-attention to extract/synthesize
            # additional training data
            mc_vertices = mc_report["vertices"]
            mc_faces = mc_report["faces"]
            mc_normals = mc_report["normals"]

            # decoder ring - v1
            # can we extract the weight's knowledge
            # this is the shape meaning/knowledge
            mc_data_values = mc_report["z_values"]

            # exploring passing attention matrix mask
            # this is how models scan for knowledge today
            mc_mask = mc_report["mask"]

            num_mc_verts = len(mc_vertices)
            num_mc_faces = len(mc_faces)
            num_mc_normals = len(mc_normals)
            num_mc_data_values = len(mc_data_values)
            layer_x = row["x"]
            layer_y = row["y"]
            layer_z = row["z"]
            # layer_desc = row['desc']
            log.info(
                "processing training data "
                f"gen={idx}/{num_training_data} "
                f"layer={layer_name} "
                f"size={row_data.shape} "
                f"pos=({layer_x}, "
                f"{layer_y}, "
                f"{layer_z}) "
                ""
                f"mesh {mesh_idx}={mesh_name} "
                f"size={mc_size_mb} "
                f"cubes level={mc_level} "
                f"step_size={mc_step_size} "
                ""
                f"shapes vertices={num_mc_verts} "
                f"faces={num_mc_faces} "
                f"normals={num_mc_normals} "
                f"values={num_mc_data_values} "
                f"mask={mc_mask} "
                ""
            )
        # end of reviewing marching cubes
    # end of building the training report
    log.info("done")
    return timeseries_training_data
