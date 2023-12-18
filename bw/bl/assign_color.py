import logging


log = logging.getLogger(__name__)


def assign_color(
    percentile: float,
    color_dictionary: dict,
):
    """
    assign_color

    assign a color based off the percentile
    value based off the lower/upper min/max values
    in the color_dictionary

    returns the color_tuple for blender in decimal
    format (1.0, 1.0, 1.0, 1.0) where (R, G, B, A)

    :param percentile: percentile that needs
        a color
    :param color_dictionary: source of truth for
        how to colorize percentiles based off
        pre-existing setup
        (for more refer to bw.bl.get_percentile_colors)
    """
    min_value = None
    max_value = None
    color = None
    for range_key, perc_node in color_dictionary.items():
        min_value = perc_node["min"]
        max_value = perc_node["max"]
        """
        log.debug(
            f"{min_value} <= {percentile} "
            f"<= {max_value}"
        )
        """
        color = (
            perc_node["r"],
            perc_node["b"],
            perc_node["g"],
            perc_node["a"],
        )
        if min_value <= percentile <= max_value:
            """
            name = perc_node["name"]
            log.debug(
                f"{min_value} <= {percentile} "
                f"<= {max_value} => "
                f"{name} = {color}"
            )
            """
            return color
    """
    log.error(
        "unsupported percentile detected "
        f"{min_value} <= {percentile} "
        f"<= {max_value} => "
        f"{color}"
    )
    """
    return color
