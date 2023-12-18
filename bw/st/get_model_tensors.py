import logging
import safetensors
import numpy as np


log = logging.getLogger(__name__)


def get_model_tensors(
    model_path: str,
    layer_names: list,
    device: str = "cpu",
):
    # Use SafeTensors to read a model's tensor array and store it as a dictionary
    """
    get_model_tensors

    extract the model tensors using safetensors
    rust mmap

    :param model_path: path to the model.safetensors file
    :param layer_names: optional - prefix layer names to
        include in the returned model_tensors dictionary
    :param device: "cpu" or "gpu"

    :return: dictionary with layer name as the key
    """
    model_tensors = {}
    with safetensors.safe_open(
        model_path,
        framework="pt",
        device="cpu",
    ) as f:
        """
        keys = f.keys()
        num_keys = len(keys)
        print(num_keys)
        """
        for key in f.keys():
            include_tensor = True
            for skip_key in [
                "bias",
                "ln_1",
                "ln_2",
                "ln_f",
            ]:
                if skip_key in key:
                    include_tensor = True
            if not include_tensor:
                log.debug(f"skipping tensor={key}")
                continue
            for layer_test_name in layer_names:
                if layer_test_name in key:
                    include_tensor = True
            if include_tensor:
                tensor_data = f.get_tensor(key)
                """
                print(tensor_data)
                print(key)
                print(tensor_data.shape)
                """
                rows = None
                cols = None
                try:
                    (rows, cols) = tensor_data.shape
                except Exception:
                    try:
                        # https://github.com/pytorch/pytorch/issues/110285
                        # is there anything worth our time?
                        numpy_check = tensor_data.numpy(
                            force=True
                        )
                        data_min = np.min(numpy_check)
                        data_max = np.max(numpy_check)
                        if (
                            data_min == 0.0
                            and data_max == 0.0
                        ):
                            log.debug(
                                f"ignoring empty tensor={key}"
                            )
                            continue
                        if data_min == data_max:
                            log.debug(
                                f"ignoring mirror tensor={key}"
                            )
                            continue
                        tensor_size = numpy_check.shape[0]
                        # divide by 2 for rows
                        num_rows = int(tensor_size / 64)
                        if num_rows == 0:
                            num_rows = int(tensor_size / 4)
                            if num_rows == 0:
                                continue
                        num_cols = int(
                            tensor_size / num_rows
                        )
                        # convert 1d to 2d
                        tensor_data = np.reshape(
                            tensor_data,
                            (
                                num_rows,
                                num_cols,
                            ),
                        )
                        (rows, cols) = tensor_data.shape
                    except Exception as e:
                        err_msg = str(e)
                        # BFloat16 support
                        # https://github.com/pytorch/pytorch/issues/110285
                        if err_msg not in [
                            (
                                "Got unsupported "
                                "ScalarType BFloat16"
                            ),
                        ]:
                            log.error(
                                f"failed processing tensor={key} "
                                f"ex={e}"
                            )
                            # for testing new models it's easier
                            # to shutdown blender here
                            # raise SystemExit
                        else:
                            log.debug(
                                f"unsupported tensor={key} "
                                f"datatype with ex={e}"
                            )
                        continue

                model_tensors[key] = {
                    "data": tensor_data,
                    "rows": rows,
                    "cols": cols,
                }
                # print(model_tensors[key])

        # print(f.get_metadata())
    return model_tensors
