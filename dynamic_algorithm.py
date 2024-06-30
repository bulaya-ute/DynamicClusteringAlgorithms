from typing import Union
import numpy as np


class Point:
    """
    Base class representing a data point
    """

    def __init__(self, position: tuple[float, ...]):
        self.position = position

    def distance_with(self, other: Union["Point", "Cluster"]) -> float:
        """
        Return the straight-line distance between two points or the distance
        between the caller object and the point in a cluster that is closest to it.
        """
        if isinstance(other, Point):
            coords1 = self.position
            coords2 = other.position
            distance = np.sqrt(sum([(c1 - c2) ** 2 for c1, c2 in zip(coords1, coords2)]))
            return distance
        elif isinstance(other, Cluster):
            shortest_distance = float("inf")
            for point in other.points:
                distance = point.distance_with(self)
                if distance < shortest_distance:
                    shortest_distance = distance
            return shortest_distance
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")

    def is_close_to(self, other: Union["Point", "Cluster"], threshold: float):
        if isinstance(other, Point):
            if self.distance_with(other) <= threshold:
                return True
            return False

        elif isinstance(other, Cluster):
            return other.is_close_to(self)
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")

    def __add__(self, other: Union["Point", "Cluster"]) -> "Cluster":
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

    def __add__(self, other: Union["Cluster", Point]) -> "Cluster":
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

    def is_close_to(self, other: Union["Cluster", Point], threshold: float):
        if isinstance(other, Cluster):
            for p1 in self.points:
                for p2 in other.points:
                    if p1.is_close_to(p2, threshold):
                        return True
            return False
        elif isinstance(other, Point):
            for p in self.points:
                if p.is_close_to(other, threshold):
                    return True
            return False
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")


if __name__ == "__main__":
    point1 = Point((0, 0))
    point2 = Point((1, 1))
    c = point1 + point2

    print(point1.distance_with(point2))
