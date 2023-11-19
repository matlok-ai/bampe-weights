import logging
import numpy as np
import PIL.Image as im

log = logging.getLogger(__name__)


def convert_tiff_from_model_tensor_weight_npy_file(
    input_file: str,
    output_file: str,
):
    """
    convert_tiff_from_model_tensor_weight_npy_file

    convert a local npy file to a tiff file

    :param input_file: input numpy file path
    :param output_file: output tifff file path
    """
    log.info(
        f"converting {input_file} to " f"{output_file}"
    )
    array = np.load(input_file)
    data = im.fromarray(array)
    data.save(output_file)
