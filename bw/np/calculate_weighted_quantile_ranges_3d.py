import logging
import numpy as np
import bw.bl.colors as bwcl


log = logging.getLogger(__name__)


def calculate_weighted_quantile_ranges_3d(
    array_3d: np.ndarray,
    num_ranges: int,
):
    """
    calculate_weighted_quantile_ranges_3d

    build a quantile range based off the 3d array
    z-axis values and the number of ranges. assign
    colors based off an ordered list from
    bw.bl.colors.get_color_tuples()

    :param array_3d: 3d array data to process
    :param num_ranges: number of np.quantile ranges
        to calculate min/max lower/upper bounds
        for quickly assigning colors to a z-value
        in the array_3d
    """
    # Calculate the minimum and maximum values for all z values
    min_z = np.min(array_3d[:, :, 2])
    max_z = np.max(array_3d[:, :, 2])

    # Calculate quantile ranges for z values
    quantile_ranges = np.linspace(
        min_z, max_z, num_ranges + 1
    )

    # Create a dictionary to store colors for each quantile range
    colors_dict = {}

    # Apply seaborn color gradient with opacity 1.0
    # cmap = sns.color_palette("viridis", num_ranges)
    # cmap = sns.color_palette("bright", num_ranges)
    # colors = sns.color_palette(cmap, n_colors=num_ranges)

    colors_tuples_map = bwcl.get_color_tuples()
    colors_names = [
        color_name for color_name in colors_tuples_map
    ]
    colors_list = [
        colors_tuples_map[color_name]
        for color_name in colors_names
    ]

    # Assign colors to the dictionary based on quantile ranges
    num_colors = len(colors_list)
    cidx = 0
    for i in range(num_ranges):
        min_range_org = quantile_ranges[i]
        max_range_org = quantile_ranges[i + 1]
        min_range = float(f"{min_range_org:.2f}")
        max_range = float(f"{max_range_org:.2f}")
        color_key = f"{min_range}_{max_range}"
        color_node = colors_list[cidx]
        color_name = colors_names[cidx]
        """
        log.debug(
            f'{i}/{num_ranges} '
            f'quantile=[{min_range},{max_range}]'
            f'color={color_name} {color_key}')
        """
        colors_dict[color_key] = {
            "name": colors_names[cidx],
            "r": color_node[0],
            "b": color_node[1],
            "g": color_node[2],
            "a": color_node[3],
            "q": i,
            "min": min_range,
            "max": max_range,
        }
        cidx += 1
        if cidx >= num_colors:
            cidx = 0

    for idx, color_range in enumerate(colors_dict):
        color_node = colors_dict[color_range]
        color_name = color_node["name"]
        min_range_val = color_node["min"]
        max_range_val = color_node["max"]
        log.debug(
            f"{idx} = [{min_range_val}, {max_range_val}] "
            f"{color_name}"
        )
    return colors_dict
