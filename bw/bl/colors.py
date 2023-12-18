def get_color_tuples(
    opacity: float = 0.5,
):
    """
    get_color_tuples

    build common colorization tuples
    for dynamic shapes and return
    the colors and a dictionary
    for reference later.

    colors are implemented as rgb decimals

    :param opacity: apply a consistent opacity
        for all colors to start
        with default set to 0.5
    """
    color_map = {
        "red": (1.0, 0.0, 0.0, opacity),  # color = red
        "light red": (
            1.0,
            0.5,
            0.5,
            opacity,
        ),  # color = light red
        "dark brown": (
            0.37,
            0.18,
            0.00,
            opacity,
        ),  # color = dark brown
        "brown": (
            0.64,
            0.32,
            0.00,
            opacity,
        ),  # color = brown
        "orange": (
            1.00,
            0.50,
            0.00,
            opacity,
        ),  # color = orange
        "light orange": (
            1.00,
            0.74,
            0.03,
            opacity,
        ),  # color = light orange
        "light green": (
            0.71,
            1.00,
            0.04,
            opacity,
        ),  # color = light green
        "green": (
            0.00,
            1.00,
            0.00,
            opacity,
        ),  # color = green
        "dark green": (
            0.32,
            0.37,
            0.00,
            opacity,
        ),  # color = dark green
        "neon green": (
            0.20,
            0.37,
            0.01,
            opacity,
        ),  # color = neon green
        "myrtle": (
            0.12,
            0.22,
            0.00,
            opacity,
        ),  # color = myrtle
        "lincoln green": (
            0.20,
            0.37,
            0.01,
            opacity,
        ),  # color = lincoln green
        "darker green": (
            0.01,
            0.22,
            0.04,
            opacity,
        ),  # color = darker green
        "dark green-blue": (
            0.01,
            0.22,
            0.13,
            opacity,
        ),  # color = dark green-blue
        "blue": (0.01, 0.16, 0.22, opacity),  # color = blue
        "light blue": (
            0.02,
            0.28,
            0.39,
            opacity,
        ),  # color = light blue
        "dark blue": (
            0.01,
            0.14,
            0.39,
            opacity,
        ),  # color = dark blue
        "light purple": (
            0.11,
            0.02,
            0.36,
            opacity,
        ),  # color = light purple
        "purple": (
            0.31,
            0.03,
            0.37,
            opacity,
        ),  # color = purple
        "yellow": (
            1.0,
            1.0,
            0.0,
            opacity,
        ),  # color = yellow
    }
    return color_map
