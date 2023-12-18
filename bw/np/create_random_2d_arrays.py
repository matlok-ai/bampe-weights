import logging
import numpy as np


log = logging.getLogger(__name__)


def create_random_2d_arrays(
    num_arrays: int,
    min_rows: int,
    max_rows: int,
    min_cols: int,
    max_cols: int,
):
    """
    create testing 2d arrays

    Create x number of random-sized 2D arrays.

    :param num_arrays: number of 2d arrays
        to create
    :param min_rows: min rows
    :param max_rows: max rows
    :param min_cols: min columns
    :param max_cols: max columns

    :return: list of 2d numpy ndarrays of float32 data
    """
    arrays = []
    for i in range(num_arrays):
        rows = np.random.randint(min_rows, max_rows + 1)
        cols = np.random.randint(min_cols, max_cols + 1)
        array = np.random.rand(rows, cols).astype(
            np.float32
        )
        mb_size = (
            float(array.shape[0] * array.shape[1] * 4)
            / 1024.0
            / 1024.0
        )
        log.info(
            f"created {i + 1}/{num_arrays} {array.shape} "
            f"{mb_size:.2f}mb"
        )
        arrays.append(array)
    return arrays
