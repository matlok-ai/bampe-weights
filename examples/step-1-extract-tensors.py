#!/usr/bin/env python3

import os
import logging
import bw.st.extract as extract

level = logging.INFO
log_level = os.getenv("LOG", "info")
if log_level == "debug":
    level = logging.DEBUG

logging.basicConfig(
    level=level,
    format=(
        "%(asctime)s.%(msecs)03d %(levelname)s "
        "%(module)s - %(funcName)s - %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

log = logging.getLogger(__name__)


if __name__ == "__main__":
    # add support for targeting a file with argparse

    st_file = "./model.safetensors"
    dir_name = os.getenv("MODEL_ALIAS", "weights")
    weight_dir = os.getenv(
        "WEIGHT_DIR", f"./npy/{dir_name}"
    )
    device = os.getenv("DEVICE", "cpu")
    tensors = (
        extract.extract_safetensor_data_to_numpy_files(
            weight_dir=weight_dir,
            st_file=st_file,
            device=device,
        )
    )
