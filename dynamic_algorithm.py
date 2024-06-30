from typing import Union


class Point:
    """
    Base class representing a data point
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Union["Point", "Cluster"]):
        if isinstance(other, Point):
            return Cluster([other])
        elif isinstance(other, Cluster):
            return other + self
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")


class Cluster:
    """
    Base class representing a cluster of data points
    """

    def __init__(self, points=None):
        if points is not None:
            self.points = [p for p in points]
        else:
            self.points = []

    def __add__(self, other: Union["Cluster", "Point"]) -> "Cluster":
        if isinstance(other, Cluster):
            self.points += other.points
            return self
        elif isinstance(other, Point):
            for p in self.points:
                if p is other:
                    break
            else:
                self.points.append(other)
            return self
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")
