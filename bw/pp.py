"""
helper for pretty printing a dictionary
"""
import json


def pp(json_data: dict):
    """
    pp

    :param json_data: dictionary to print

    :returns: string for the dictionary
    :rtype: str
    """
    return str(
        json.dumps(
            json_data,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )
    )
