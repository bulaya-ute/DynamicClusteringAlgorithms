import json


def travel_towards(point1, point2, ratio):
    """
    Compute the coordinates of the destination point after traveling a specified
    ratio of the distance from point1 to point2.

    Parameters:
    - point1: List or tuple representing the coordinates of the first point.
    - point2: List or tuple representing the coordinates of the second point.
    - ratio: Fraction of the distance to travel from point1 to point2 (0 <= ratio <= 1).

    Returns:
    - List representing the coordinates of the destination point.
    """
    # Check if point1 and point2 have the same dimensions
    if len(point1) != len(point2):
        raise ValueError("Both points must have the same number of dimensions.")

    # Compute the coordinates of the destination point
    destination = [(1 - ratio) * p1 + ratio * p2 for p1, p2 in zip(point1, point2)]

    return destination


def load_dataset(path: str):
    with open(path, "r") as file_obj:
        data = json.load(file_obj)
        return data
