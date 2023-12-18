import logging
import numpy as np


log = logging.getLogger(__name__)


def downscale_2d_array(
    array: np.ndarray, target_rows: int, target_cols: int
):
    """
    downscale_2d_array

    downscale a 2D array to the target dimensions by averaging values

    :param array: input 2D NumPy array
    :param target_rows: number of rows
    :param target_cols: number of columns

    :return: downscaled 2D numpy array
    """
    downscale_factor_rows = max(
        1, array.shape[0] // target_rows
    )
    downscale_factor_cols = max(
        1, array.shape[1] // target_cols
    )

    reshaped_array = array[
        : downscale_factor_rows * target_rows,
        : downscale_factor_cols * target_cols,
    ]
    log.debug(
        f"downscaling {array.shape} "
        f"factor_rows={downscale_factor_rows} "
        f"factor_cols={downscale_factor_cols} "
    )
    reshaped_array = reshaped_array.reshape(
        target_rows,
        downscale_factor_rows,
        target_cols,
        downscale_factor_cols,
    )

    downscaled_array = np.mean(reshaped_array, axis=(1, 3))

    return downscaled_array
