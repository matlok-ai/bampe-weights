import logging
import numpy as np


log = logging.getLogger(__name__)


def upscale_2d_array(
    array: np.ndarray,
    target_rows: int,
    target_cols: int,
):
    """
    upscale_2d_array

    upscale a 2D array to the target dimensions by repeating values

    :param array: input 2D NumPy array
    :param target_rows: number of rows
    :param target_cols: number of columns

    :return: upscaled 2D numpy array
    """
    scale_factor_rows = target_rows / array.shape[0]
    scale_factor_cols = target_cols / array.shape[1]
    # use np.tile to repeat the array along each dimension
    upscaled_array = np.tile(
        array,
        (
            int(np.ceil(scale_factor_rows)),
            int(np.ceil(scale_factor_cols)),
        ),
    )

    # crop the upscaled array to match the target dimensions
    upscaled_array = upscaled_array[
        :target_rows, :target_cols
    ]
    return upscaled_array
