import itertools
import random
import subprocess
from typing import Any

from manimlib import *
import math
import numpy as np
import json

from utils import travel_towards

with open("datasets/dataset20240708-034937.json", "r") as file_obj:
    data = json.load(file_obj)
    sample_points = data["sample_points"]
    centroid_points = data["centroid_points"]
    bounds = data["bounds"]
np.random.seed(123445848)
np.random.shuffle(sample_points)
print(f"sample points: {sample_points}")
# print(f"centroid points: {centroid_points}")

colors = [BLUE, GREEN, RED, PURPLE, ORANGE, YELLOW, GREY]

num_clusters = 4
cluster_memory = 10
outlier_threshold = 1.0

# centroid_points = [[np.random.uniform(*bounds["x"]), np.random.uniform(*bounds["y"])] for _ in range(num_clusters)]


class KMeans(Scene):
    def construct(self):

        # Generate samples and centroids within the rectangle
        samples = VGroup()
        centroids = VGroup()

        # Create a rectangle
        rectangle = Rectangle(width=10, height=6, color=WHITE)

        rect_half_width = rectangle.width / 2
        rect_half_height = rectangle.height / 2

        # Add the rectangle to the scene
        self.play(FadeIn(rectangle))
        self.wait(1)

        # Initialize the centroids
        for i, (x, y) in enumerate(centroid_points):
            dot = Text(text="X", color=colors[i], font_size=30)
            dot.move_to((x, y, 0))
            dot.set_color(colors[i])
            centroids.add(dot)

        # Add the centroid to the scene
        self.play(FadeIn(centroids))
        self.wait(1)

        # Initialize the samples
        for x, y in sample_points:
            dot = Dot(point=(x, y, 0), color=WHITE, radius=0.1)
            samples.add(dot)

            # --------------------------------------------- tabbed here!

            # Add the samples to the scene
            # self.play(FadeIn(samples))
            self.play(FadeIn(dot))
            # self.wait(1)

            for iteration in itertools.count():
                centroids_moved = False

                # A cluster will be a group of dots in this case. The first item in the group
                # will be the centroid dot
                clusters = [VGroup(centroid) for centroid in centroids]

                change_color_animations = []
                connect_lines_animations = []
                fade_out_lines_animations = []

                for sample in samples:
                    distances = []

                    # Variable to store the lines
                    # lines = VGroup()
                    for centroid in centroids:
                        # line = Line(start=sample.get_center(), end=centroid.get_center())
                        # lines.add(line)
                        distances.append(math.sqrt(
                            (centroid.get_center()[0] - sample.get_center()[0]) ** 2 +
                            (centroid.get_center()[1] - sample.get_center()[1]) ** 2))

                    # Show lines connecting the sample to the centroids
                    # connect_lines_animations += [Create(line) for line in lines]

                    shortest_index = distances.index(min(distances))

                    line = Line(color=centroids[shortest_index].get_color(), start=sample.get_center(),
                                end=centroids[shortest_index].get_center())
                    connect_lines_animations.append(ShowCreation(line))
                    change_color_animations.append(sample.animate.set_color(centroids[shortest_index].get_color()))

                    # Add dot to the cluster
                    for cluster in clusters:
                        if cluster[0] is centroids[shortest_index]:
                            cluster.add(sample)

                    fade_out_lines_animations.append(FadeOut(line))
                    # self.wait(0.5)

                self.play(*(connect_lines_animations + change_color_animations))
                # self.wait(0.5)
                self.play(*fade_out_lines_animations)

                # Calculate the means of the clusters and check if the existing centroid changes position
                cluster_means = [(np.mean([sample.get_x() for sample in cluster[1:]]),
                                  np.mean([sample.get_y() for sample in cluster[1:]])) for cluster in clusters]

                centroid_adjust_animations = []
                # Check if cluster centroids are already located at the cluster means
                for i, (cluster, mean_pos) in enumerate(zip(clusters, cluster_means)):
                    if np.isnan(mean_pos[0]) or np.isnan(mean_pos[1]):
                        continue
                    centroid_pos = cluster[0].get_center()[0:2]
                    if abs(mean_pos[0] - centroid_pos[0]) > 0.05 or abs(mean_pos[1] - centroid_pos[1]) > 0.05:
                        centroids_moved = True
                        centroid_adjust_animations.append(centroids[i].animate.move_to((mean_pos[0], mean_pos[1], 0)))

                if centroid_adjust_animations:
                    self.play(*centroid_adjust_animations)

                if centroids_moved:  # or interation_num < 10:
                    # Remove the existing lines
                    # self.play(*fade_out_lines_animations, run_time=1)

                    # Make all the sample dots white again
                    self.play(*[dot.animate.set_color(WHITE) for dot in samples])
                else:
                    break

                break

        # # Fade out all elements
        self.wait(5)
        # self.play(FadeOut(rectangle), FadeOut(samples), FadeOut(centroids), FadeOut(assigned_lines))


class DynamicClustering(Scene):
    def construct(self):
        # Remove these two lines later. It's solely for testing
        # centroid_points = [[random.uniform(*bounds["x"]), random.uniform(*bounds["y"])] for _ in range(num_clusters)]
        # sample_points = [[random.uniform(*bounds["x"]), random.uniform(*bounds["y"])] for _ in range(50)]

        points_on_scene = []
        centroids_on_scene = []
        acceptance_regions = []
        cluster_memories = [[] for _ in centroid_points]

        rect_width = bounds["x"][1] - bounds["x"][0]
        rect_height = bounds["y"][1] - bounds["y"][0]
        rect = Rectangle(width=rect_width, height=rect_height)

        new_center = np.array([np.mean(bounds["x"]), np.mean(bounds["y"]), 0])
        rect.move_to(new_center)
        self.camera.frame.move_to(new_center)
        self.play(FadeIn(rect))

        for i, point in enumerate(centroid_points):
            centroid = Text("X", color=colors[i])
            centroid.set_fill(opacity=0.5)
            centroid.move_to(point + [0.0, ])

            centroids_on_scene.append(centroid)
            region_radius = outlier_threshold
            circle = Circle(radius=region_radius)
            circle.move_to(centroid.get_center())
            circle.set_stroke(color=colors[i], opacity=0.5)
            acceptance_regions.append(circle)

        clusters: list[list[Union[Text, Dot]]] = [[cen] for cen in centroids_on_scene]

        # self.play(FadeIn(*centroids_on_scene))
        self.add(*centroids_on_scene)
        self.add(*acceptance_regions)

        for sample_count_index, point in enumerate(sample_points):
            dot = Dot(point + [0, ], radius=0.1)
            points_on_scene.append(dot)
            self.play(FadeIn(dot))

            # Calculate distances with the centroids
            distances = []
            for centroid in centroids_on_scene:
                distance = sum([(p1 - p2) ** 2 for p1, p2 in zip(dot.get_center(), centroid.get_center())]) ** 0.5
                distances.append(distance)

            shortest_index = distances.index(min(distances))
            shortest_distance = distances[shortest_index]
            nearest_cluster = clusters[shortest_index]

            # Determine if it's an outlier

            if shortest_distance > outlier_threshold and nearest_cluster[1:]:
                # It is an outlier

                self.play(dot.animate.set_color(GREY_BROWN))

                animations = []

                def distance_key(dp):
                    return sum([(p1 - p2) ** 2 for p1, p2 in zip(dp.get_center(),
                                                                 nearest_cluster[0].get_center())]) ** 0.5

                # Update the memory of all the clusters
                for i, cluster in enumerate(clusters):

                    # First check that the data point doesn't already exist in the memory of this cluster
                    if dot not in cluster_memories[i]:
                        new_memory = cluster_memories[i] + [dot]
                    else:
                        new_memory = cluster_memories[i]

                    # Update the order of the memory and ensure the correct amount is available
                    new_memory.sort(key=distance_key)

                    cluster_memories[i].clear()
                    cluster_memories[i] += new_memory[:cluster_memory]

                    line = Line(start=dot.get_center(),
                                end=centroids_on_scene[i].get_center())
                    animations.append(ShowCreationThenDestruction(line))

                if animations:
                    self.play(*animations)

                # # Nudge the nearest centroid towards the outlier.
                # # It is guaranteed that the number of sample points are >= 1
                #
                # learning_rate =  1 / max(len(nearest_cluster[1:]), 1) / max((shortest_distance - outlier_threshold), 1)
                # dest_pos = travel_towards(nearest_cluster[0].get_center(), dot.get_center(), learning_rate)
                #
                # self.play(nearest_cluster[0].animate.move_to(dest_pos),
                #           acceptance_regions[shortest_index].animate.move_to(dest_pos))

            else:
                # If the code below this point executes, it is not an outlier

                # Assign point to nearest cluster
                assigned_centroid = centroids_on_scene[shortest_index]

                # Add point to cluster
                cluster_of_choice = clusters[shortest_index]
                cluster_of_choice.append(dot)

                self.play(dot.animate.set_color(assigned_centroid.get_color()))

                learning_rate = 1 / max(len(cluster_of_choice[1:]), 1)
                dest_pos = travel_towards(cluster_of_choice[0].get_center(), cluster_of_choice[-1].get_center(),
                                          learning_rate)

                self.play(cluster_of_choice[0].animate.move_to(dest_pos),
                          acceptance_regions[shortest_index].animate.move_to(dest_pos))

                # Check if any previously rejected data points are now worth adding to the
                # cluster, now that the centroid is in an updated position
                i = 0
                while i < len(cluster_memories[shortest_index]):
                    data_point = cluster_memories[shortest_index][i]
                    distance = sum([(p1 - p2) ** 2 for p1, p2 in zip(data_point.get_center(),
                                                                     assigned_centroid.get_center())]) ** 0.5

                    if distance <= outlier_threshold:

                        # Assign the data point to the cluster
                        cluster_of_choice.append(data_point)
                        self.play(data_point.animate.set_color(assigned_centroid.color))

                        # Update the position of the centroid
                        learning_rate = 1 / max(len(cluster_of_choice[1:]), 1)
                        dest_pos = travel_towards(cluster_of_choice[0].get_center(), cluster_of_choice[-1].get_center(),
                                                  learning_rate)

                        self.play(cluster_of_choice[0].animate.move_to(dest_pos),
                                  acceptance_regions[shortest_index].animate.move_to(dest_pos),
                                  # Transform(acceptance_regions[shortest_index], new_circle),
                                  acceptance_regions[shortest_index].animate.move_to(dest_pos))

                        # Remove the redeemed data point from the memories of all clusters
                        for memory in cluster_memories:
                            while data_point in memory:
                                memory.remove(data_point)

                    else:
                        i += 1


if __name__ == "__main__":
    # subprocess.run("manim -pql animation_main.py DynamicClustering".split())

    # To render in medium quality
    # subprocess.run("manimgl animation_main.py DynamicClustering -o -w -m".split())

    # To simply play animation without rendering
    subprocess.run("manimgl animation_main.py DynamicClustering".split())
