from time import sleep
from typing import Union, Optional, Sequence, Iterable
from utils import load_dataset, travel_towards
import numpy as np
from matplotlib import pyplot as plt


class DataPoint:
    """
    Base class representing a data point
    """

    def __init__(self, position: tuple[float, ...]):
        self.position = position
        self.other_attributes = {}

    def distance_with(self, other: Union["DataPoint", "Cluster"]) -> float:
        """
        Return the straight-line distance between two points or the distance
        between the caller object and the point in a cluster that is closest to it.
        """
        if isinstance(other, DataPoint) or isinstance(other, Cluster):
            coords1 = self.position
            coords2 = other.position
            distance = sum([(c1 - c2) ** 2 for c1, c2 in zip(coords1, coords2)]) ** 0.5
            return distance
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")

    def is_close_to(self, other: Union["DataPoint", "Cluster"], threshold: float):
        if isinstance(other, DataPoint):
            if self.distance_with(other) <= threshold:
                return True
            return False

        elif isinstance(other, Cluster):
            return other.is_close_to(self, threshold)
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")

    def __add__(self, other: Union["DataPoint", "Cluster"]) -> "Cluster":
        if isinstance(other, DataPoint):
            return Cluster([other], 1)
        elif isinstance(other, Cluster):
            return other + self
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")


class Cluster:
    """
    Base class representing a cluster of data points
    """

    def __init__(self, centroid_pos: Sequence[float] = (0, 0), acceptance_radius: float = 1, memory_limit: int = 1,
                 points=None):
        self.acceptance_radius = acceptance_radius
        self.memory_limit = memory_limit
        self.position = centroid_pos
        if points is not None:
            self.points: Sequence[DataPoint] = [p for p in points]
        else:
            self.points: Sequence[DataPoint] = []
        self.memory: list[DataPoint] = []
        self.other_attributes = {}

    def __add__(self, other: Union["Cluster", DataPoint]) -> "Cluster":
        if isinstance(other, Cluster):
            self.points += other.points
            return self
        elif isinstance(other, DataPoint):
            for p in self.points:
                if p is other:
                    break
            else:
                self.points.append(other)
            return self
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")

    def is_close_to(self, other: Union["Cluster", DataPoint], threshold: float) -> bool:
        if isinstance(other, Cluster):
            for p1 in self.points:
                for p2 in other.points:
                    if p1.is_close_to(p2, threshold):
                        return True
            return False
        elif isinstance(other, DataPoint):
            for p in self.points:
                if p.is_close_to(other, threshold):
                    return True
            return False
        else:
            raise TypeError(f"Invalid operand supplied. Expected 'Point' or 'Cluster', got {type(other)}.")

    def add_point(self, point: "DataPoint") -> None:
        self + point

    def update_memory(self, point: DataPoint):
        new_memory = self.memory + [point]
        new_memory.sort(key=lambda x: x.distance_with(self), reverse=True)
        self.memory = new_memory[:self.memory_limit]

    def is_empty(self) -> bool:
        return not bool(self.points)

    def set_position(self, new_pos: Sequence[float]):
        """Set the coordinates of the cluster's centroid"""
        self.position = new_pos

    @property
    def learning_rate(self):
        if self.points:
            return 1 / len(self.points)
        return 1


class Space:
    """Base class for sample space in which sample points will be added and clusters made"""

    colors = ["blue", "green", "red", "purple", "orange", "yellow"]

    def __init__(
            self, dataset_path: str = None, acceptance_radius=1, cluster_memory=3
    ):
        self._bounds = None

        # This will contain all the data points present
        self.contents: list[Union[Cluster, DataPoint]] = []

        self._clusters = self.contents[:]
        self._empty_clusters = self.contents[:]
        self.other_attributes = {}

        if dataset_path:
            data = load_dataset(dataset_path)

            for i, cp in enumerate(data["centroid_points"]):
                _cluster = self.add_cluster(cp, acceptance_radius, cluster_memory)
                _cluster.other_attributes["name"] = f"cluster{i}"

            for sp in data["sample_points"]:
                self.add_data_point(DataPoint(sp))

            self._bounds = data["bounds"]

    def add_cluster(self, pos, acceptance_radius, memory_limit):
        # A centroid is basically an empty cluster here
        _cluster = Cluster(pos, acceptance_radius, memory_limit)
        self.contents.append(_cluster)
        self._clusters.append(_cluster)
        return _cluster

    def add_data_point(self, point: DataPoint):
        distances = []
        for _cluster in self._clusters:
            distances.append(point.distance_with(_cluster))
        shortest_distance = min(distances)
        nearest_index = distances.index(shortest_distance)
        nearest_cluster = self._clusters[nearest_index]

        # Not an outlier.
        if shortest_distance <= nearest_cluster.acceptance_radius or nearest_cluster.is_empty():
            # Add it to the nearest cluster
            nearest_cluster.add_point(point)

            # Update the position of the centroid
            new_pos = travel_towards(nearest_cluster.position, point.position, nearest_cluster.learning_rate)
            nearest_cluster.set_position(new_pos)

            # Update the empty clusters
            while nearest_cluster in self._empty_clusters:
                self._empty_clusters.remove(nearest_cluster)

            # Check the memory of the cluster for any nearby outliers
            i = 0
            while i < len(nearest_cluster.memory):
                outlier = nearest_cluster.memory[i]

                # Check if the outlier is close enough
                if outlier.distance_with(nearest_cluster) <= nearest_cluster.acceptance_radius:
                    # Update the position of the centroid
                    new_pos = travel_towards(nearest_cluster.position, outlier.position, nearest_cluster.learning_rate)
                    nearest_cluster.set_position(new_pos)

                    # Remove the outlier from the memory of all clusters
                    for _cluster in self.clusters:
                        while outlier in _cluster.memory:
                            _cluster.memory.remove(outlier)

                    continue

                i += 1

        else:
            # It is an outlier
            self.contents.append(point)

            # Update the memory of all the clusters
            for _cluster in self.clusters:
                _cluster.update_memory(point)

    def visualise(self) -> None:
        if not self._bounds:
            print("Bounds not initialized. Visualisation cancelled.")
            return

        # Parameters
        width = self.bounds[0][1] - self.bounds[0][0]
        height = self.bounds[1][1] - self.bounds[1][0]

        # Visualization
        plt.figure(figsize=(width, height))

        # Create rectangle centered at origin
        rectangle = plt.Rectangle((-width / 2, -height / 2), width, height,
                                  linewidth=2, edgecolor='green', facecolor='none')
        # Add rectangle to plot
        plt.gca().add_patch(rectangle)

        # Plot configurations
        plt.axhline(0, color='gray', linestyle='--')
        plt.axvline(0, color='gray', linestyle='--')
        # plt.legend()

        abs_color_index = 0

        # Extract and plot points
        for thing in self.contents:
            color_index = abs_color_index % len(self.colors)
            if isinstance(thing, Cluster):
                plt.scatter(*thing.position, color=self.colors[color_index], marker="x", s=100)
                if thing.points and thing.acceptance_radius != float("inf"):
                    circle = plt.Circle((thing.position[0], thing.position[1]), radius=thing.acceptance_radius,
                                        color=self.colors[color_index], fill=False)
                    plt.gca().add_patch(circle)
                for x, y in [sample.position for sample in thing.points]:
                    plt.scatter(x, y, color=self.colors[color_index])
                abs_color_index += 1
            elif isinstance(thing, DataPoint):
                plt.scatter(*thing.position, color='black')
            else:
                raise TypeError

        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Clustering Visualisation')
        plt.grid(True)
        plt.xlim(-width / 2 - 1, width / 2 + 1)  # Extend x-axis slightly to fit rectangle
        plt.ylim(-height / 2 - 1, height / 2 + 1)  # Extend y-axis slightly to fit rectangle
        plt.show()

    @property
    def clusters(self):
        clusters = []
        for thing in self.contents:
            if isinstance(thing, Cluster):
                clusters.append(thing)
        return clusters

    @property
    def bounds(self):
        if self._bounds:
            return self._bounds
        raise RuntimeError("Bounds have not been set")

    def export(self, output_path):
        data = []
        for thing in self.contents:
            if isinstance(thing, Cluster):
                for data_point in thing:


if __name__ == "__main__":
    # dataset = load_dataset("datasets/dataset20240708-042931.json")
    sample_space = Space("datasets/dataset20240708-042931.json")
    sample_space.visualise()

    # # Generate random centroid coordinates
    # centroid_points = [[np.random.uniform(*dataset["bounds"][i]) for i in range(len(dataset["bounds"]))]
    #                    for _ in range(len(dataset["centroid_points"]))]
    #
    # # # Use the actual coordinates of centroids
    # # centroid_points = dataset["centroid_points"]
    #
    # for i, centroid_point in enumerate(centroid_points):
    #     cluster = sample_space.add_cluster(centroid_point, 1, 3)
    #     cluster.other_attributes["name"] = i
    #
    # for sample_point in dataset["sample_points"]:
    #     sample_space.add_data_point(DataPoint(sample_point))
    #
    # sample_space.visualise()
    # sleep(2)
