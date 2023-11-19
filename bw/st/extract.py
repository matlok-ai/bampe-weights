import os
import logging
import numpy as np
import safetensors


log = logging.getLogger(__name__)


def extract_safetensor_data_to_numpy_files(
    weight_dir: str,
    st_file: str,
    device: str = "cpu",
):
    """
    extract_safetensor_data_to_numpy_files
    use rust bindings to iterate over
    the mmap-ed, in-memory gtpq tensors
    and save them as numpy npy files for

    after running you can use numpy to open
    any of the weights for editing/changing

    ```python
    >>> import numpy as np
    >>> d = np.load('path/tdata__model.norm.weight.npy')
    >>> print(d)
    [0.8203 0.824  0.8086 ... 0.789  0.496  0.879 ]
    >>>
    ```

    :param weight_dir: directory to save the
        all tensor files as npy
    :param st_file: safetensors file (gptq)
    :param device: cpu by default
    """
    tensors = {}
    npy_dir_path = f"{weight_dir}"
    if not os.path.exists(npy_dir_path):
        os.mkdir(npy_dir_path)
    log.info(f"loading st_file={st_file}")
    with safetensors.safe_open(
        st_file,
        framework="pt",
        device=device,
    ) as f:
        num_keys = len(f.keys())
        for i, key in enumerate(f.keys()):
            tensors[key] = f.get_tensor(key)
            npy_file_path = (
                f"{npy_dir_path}/" f"tdata__{key}.npy"
            )
            log.info(
                f"extracting tensor {i}/{num_keys}={key} "
                f"to {npy_file_path}"
            )
            np.save(npy_file_path, tensors[key])
    return tensors
