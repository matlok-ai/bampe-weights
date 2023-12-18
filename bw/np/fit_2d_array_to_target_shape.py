import logging
import numpy as np
import bw.np.downscale_2d_array as downscaler
import bw.np.upscale_2d_array as upscaler


log = logging.getLogger(__name__)


def fit_2d_arrays_to_target_shape(
    arrays: list[np.ndarray],
    target_rows: int,
    target_cols: int,
):
    """
    fit_2d_arrays_to_target_shape

    fit a list of 2D arrays into a target 3D array with specified dimensions.

    :param arrays: List of 2D NumPy arrays.
    :param target_rows: number of
        resample target rows before
        drawing
    :param target_cols: number of
        resample target cols before
        drawing

    :return: 3d np.ndarray with the resized 2d arrays stacked on
        the z-axis
    """
    num_arrays = len(arrays)
    fitted_arrays = []
    for idx, array in enumerate(arrays):
        op_performed = None
        if (array.shape[0] < target_rows) or (
            array.shape[1] < target_cols
        ):
            op_performed = "upscaled"
            log.debug(
                f"fit {idx}/{num_arrays} "
                f"upscaled {array.shape}"
            )
            fitted_array = upscaler.upscale_2d_array(
                array, target_rows, target_cols
            )
        elif (array.shape[0] > target_rows) or (
            array.shape[1] > target_cols
        ):
            op_performed = "downscale"
            log.debug(
                f"fit {idx}/{num_arrays} "
                f"downscaled {array.shape}"
            )
            fitted_array = downscaler.downscale_2d_array(
                array, target_rows, target_cols
            )
        else:
            op_performed = "ignored"
            log.debug(
                f"fit {idx}/{num_arrays} "
                f"ignored {array.shape}"
            )
            fitted_array = array

        log.debug(
            f"fit {idx}/{num_arrays} "
            f"{op_performed} "
            f"src={array.shape} "
            f"dst={fitted_array.shape} == "
            f"({target_rows}, {target_cols})"
        )
        fitted_arrays.append(fitted_array)

    return np.stack(fitted_arrays, axis=2)
