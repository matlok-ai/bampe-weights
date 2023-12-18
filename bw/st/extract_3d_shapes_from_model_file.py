import logging
import numpy as np
import bw.st.get_model_tensors as get_model_tensors
import bw.np.fit_2d_arrays_to_target_shape as fit


log = logging.getLogger(__name__)


def extract_3d_shapes_from_model_file(
    input_file: str,
    layer_names: list,
    max_layers: int = None,
    device: str = "cpu",
    target_faces: int = None,
    target_rows: int = 512,
    target_cols: int = 512,
    start_x: int = -500,
    start_y: int = 100,
    start_z: int = -300,
):
    """
    extract_3d_shapes_from_model_file

    extract the weights from a model file
    and build a list of 3d arrays with
    an a marching cubes algorithm that
    finds shapes in high resolution data

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
    """
    tensors = {}
    tensor_keys = []
    num_tensors = 0

    num_extracted = len(tensor_keys)
    log.info(
        f"extracted {num_extracted}/{num_tensors} "
        f"tensors from model={input_file} "
        f"layers={','.join(tensor_keys)}"
    )
    tensors = get_model_tensors.get_model_tensors(
        input_file, layer_names, device=device
    )

    """
    print("Model Tensors:")
    print(tensors)
    print(f"num tensors: {len(tensors)}")
    """
    num_tensors = len(tensors)
    log.info(
        "preprocess - phase 1 - "
        f"reading {num_tensors} tensors "
        f"filtering layers={len(layer_names)}"
    )

    target_size_mb = float(
        f"{float(target_rows * target_cols * 4.0 / 1024.0 / 102.4)}"
    )

    all_data_3d = []
    tensor_2d_arrays = []
    num_rendered = 0
    for idx, key in enumerate(tensors):
        if idx == 61:
            log.info(f"{idx} - skipped tensor key {key}")
            continue
        tensor_node = tensors[key]
        tensor_data = tensor_node["data"].numpy()
        # refresh to make this faster
        tensor_2d_arrays = []
        tensor_2d_arrays.append(tensor_data)
        tensor_2d_arrays.append(tensor_data)
        tensor_num_rows = tensor_data.shape[0]
        tensor_num_cols = tensor_data.shape[1]
        for i in range(0, 3):
            stacked_arr = np.tile(
                tensor_data[:, :, np.newaxis], (1, 1, 3)
            )
        if len(stacked_arr) > 1:
            mb_size_org = float(stacked_arr.nbytes) / (
                1024.0 * 1024.0
            )
            layer_name = f"Layer: {key[0:32]}"
            desc = (
                f"src dimensions=({tensor_num_rows}, "
                f"{tensor_num_cols}) "
                f"size={mb_size_org:.2f}mb compressed to "
                f"({target_rows},{target_cols}) "
                f"{target_size_mb:.2f}mb"
            )
            log.info(
                f"rendering {idx}/{num_tensors} "
                f"{desc} dst=({target_rows}, {target_cols}) "
                f"{target_size_mb:.2f}mb"
                ""
            )
            fitted_3d_array = (
                fit.fit_2d_arrays_to_target_shape(
                    tensor_2d_arrays,
                    target_rows,
                    target_cols,
                )
            )
            all_data_3d.append(
                {
                    "name": layer_name,
                    "desc": desc,
                    "data": fitted_3d_array,
                    "target_faces": target_faces,
                    "target_rows": target_rows,
                    "target_cols": target_cols,
                    "x": start_x,
                    "y": start_y + (num_rendered * 25),
                    "z": start_z,
                }
            )
            num_rendered += 1
            if max_layers:
                if idx > max_layers:
                    break
    # for key in tensors

    if max_layers:
        log.info(
            f"rendered {num_rendered}/{max_layers} "
            f"out of {num_tensors} "
            f"into ~{target_faces} polygon faces "
            "per tensor in "
            f"shape({target_rows}, {target_cols})"
        )
    else:
        log.info(
            f"rendered {num_rendered}/{num_tensors} "
            f"into ~{target_faces} polygon faces "
            "per tensor in "
            f"shape({target_rows}, {target_cols})"
        )
    return all_data_3d
