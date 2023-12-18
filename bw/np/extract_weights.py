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
    start_x: int = 0,
    start_y: int = 0,
    start_z: int = 1,
    max_depth: int = 2,
    pad_per: int = 20,
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
        layers to fit
    :param device: cpu vs gpu
    :param target_faces: min faces to
        hopefully fit if there is
        enough data
    :param target_rows: number of
        resample target rows before
        drawing
    :param target_cols: number of
        resample target cols before
        drawing
    :param max_depth: stack each layer
        on itself this many times
        to convert it to a 3d ndarray
    :param pad_per: number to pad
        per object
        on the y-axis
    """
    tensors = {}
    tensor_keys = []
    num_tensors = 0

    log.info(
        f"extracting tensors from model={input_file} "
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

    # set some depth for shape rendering with smaller renders
    if max_layers is not None and max_layers < 5:
        max_depth = 3

    all_data_3d = []
    tensor_2d_arrays = []
    num_fit = 0
    for idx, key in enumerate(tensors):
        tensor_node = tensors[key]
        # https://github.com/pytorch/pytorch/issues/110285
        try:
            tensor_data = tensor_node["data"].numpy()
        except Exception as e:
            log.debug(
                f"ignored tensor={idx} {key} with ex={e}"
            )
            continue
        # refresh to make this faster
        tensor_2d_arrays = []
        tensor_2d_arrays.append(tensor_data)
        tensor_2d_arrays.append(tensor_data)
        tensor_num_rows = tensor_data.shape[0]
        tensor_num_cols = tensor_data.shape[1]
        for i in range(0, max_depth):
            stacked_arr = np.tile(
                tensor_data[:, :, np.newaxis], (1, 1, 3)
            )
        if len(stacked_arr) > 1:
            mb_size_org = float(stacked_arr.nbytes) / (
                1024.0 * 1024.0
            )
            layer_name = f"{key[0:128]}"
            label_layer_name = f"Layer: {layer_name}"
            desc = (
                f"src dimensions=({tensor_num_rows}, "
                f"{tensor_num_cols}) "
                f"size={mb_size_org:.2f}mb compressed to "
                f"({target_rows},{target_cols}) "
                f"{target_size_mb:.2f}mb"
            )
            if (num_tensors < 50) or (idx % 500 == 0):
                log.info(
                    f"fitting {num_fit + 1}/{num_tensors} "
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
                    "layer_name": label_layer_name,
                    "desc": desc,
                    "data": fitted_3d_array,
                    "target_faces": target_faces,
                    "target_rows": target_rows,
                    "target_cols": target_cols,
                    "x": start_x,
                    "y": start_y + (num_fit * pad_per),
                    "z": start_z,
                }
            )
            num_fit += 1
            if max_layers:
                if num_fit >= max_layers:
                    break
    # for key in tensors

    if max_layers:
        log.info(
            f"done fitting {num_fit}/{max_layers} "
            f"out of {num_tensors} "
            f"into ~{target_faces} polygon faces "
            "per tensor in "
            f"shape({target_rows}, {target_cols})"
        )
    else:
        log.info(
            f"done fitting {num_fit}/{num_tensors} "
            f"into ~{target_faces} polygon faces "
            "per tensor in "
            f"shape({target_rows}, {target_cols})"
        )
    return all_data_3d
