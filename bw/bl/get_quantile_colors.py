import logging
import bw.np.calculate_weighted_quantile_ranges_2d as calc


log = logging.getLogger(__name__)


def get_quantile_colors(
    z_values,
    min_value: float,
    max_value: float,
    num: int = 10,
    opacity: float = 0.5,
    color_map: dict = None,
):
    """
    get_quantile_colors

    PROMPTS

    build a color dictionary for
    quickly mapping weights to a color
    based off quantile ranges in the z_values

    :param z_values: numpy 2d array
    :param min_value: start
        value for dynamic quantile calculations
        using the num argument
    :param max_value: end
        value for dynamic quantile calculations
        using the num argument
    :param num: number of quantiles to
        map to colors (it does not have to
        be all of the colors either)
    :param opacity: transparency
    :param color_map: optional - existing
        color map to use
        with default from the
        bw.bl.colors.get_color_tuples() api
    """
    # Calculate quantile intervals
    color_map = calc.calculate_weighted_quantile_ranges_2d(
        array_2d=z_values, num_ranges=num + 1
    )
    return color_map
