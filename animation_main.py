from manim import *
import random
import math

import numpy as np


class KMeans(Scene):
    def construct(self):
        colors = [BLUE, GREEN, RED, PURPLE, ORANGE, YELLOW, GREY]

        # Create a rectangle
        rectangle = Rectangle(width=10, height=6, color=WHITE)

        rect_half_width = rectangle.width / 2
        rect_half_height = rectangle.height / 2

        # Add the rectangle to the scene
        self.play(Create(rectangle))
        self.wait(1)

        # Define number of samples and centroids
        num_dots = 12
        num_centroids = 3

        # Generate random samples within the rectangle
        samples = VGroup()
        centroids = VGroup()

        # Initialize the samples
        for _ in range(num_dots):
            dot_radius = 0.1

            # Generate random coordinates within the rectangle
            x = random.uniform(-rect_half_width + dot_radius, rect_half_width - dot_radius)  # Rectangle width / 2
            y = random.uniform(-rect_half_height + dot_radius, rect_half_height - dot_radius)  # Rectangle height / 2

            dot = Dot(point=(x, y, 0), color=WHITE, radius=dot_radius)
            samples.add(dot)

        # Initialize the centroids
        for i in range(num_centroids):
            dot_radius = 0.2

            # Generate random coordinates within the rectangle
            x = random.uniform(-rect_half_width + dot_radius, rect_half_width - dot_radius)  # Rectangle width / 2
            y = random.uniform(-rect_half_height + dot_radius, rect_half_height - dot_radius)  # Rectangle height / 2

            dot = Dot(point=(x, y, 0), color=colors[i], radius=dot_radius)
            centroids.add(dot)

        # Add the samples to the scene
        self.play(FadeIn(samples))
        self.wait(2)

        # Add the centroid to the scene
        self.play(FadeIn(centroids))
        self.wait(2)

        centroids_moved = True
        # while centroids_moved:
        for _ in range(3):
            centroids_moved = False

            # A cluster will be a group of dots in this case. The first item in the group
            # will be the centroid dot
            clusters = [VGroup(centroid) for centroid in centroids]
            assigned_lines = VGroup()

            # Begin assigning samples to centroids
            for sample in samples:
                distances = []

                # Variable to store the lines
                lines = VGroup()
                for centroid in centroids:
                    line = Line(start=sample.get_center(), end=centroid.get_center())
                    lines.add(line)
                    distances.append(math.sqrt(
                        (centroid.get_center()[0] - sample.get_center()[0]) ** 2 +
                        (centroid.get_center()[1] - sample.get_center()[1]) ** 2))

                # Show lines connecting the sample to the centroids
                self.play(*[Create(line) for line in lines], run_time=0.5)
                self.wait(0.5)

                # Change the color of the shortest line and its sample to suit its associated centroid
                shortest_index = distances.index(min(distances))
                self.play(lines[shortest_index].animate.set_color(centroids[shortest_index].get_color()),
                          sample.animate.set_color(centroids[shortest_index].get_color()), run_time=0.5)
                assigned_lines.add(lines[shortest_index])
                lines.remove(lines[shortest_index])

                # Add dot to the cluster
                for cluster in clusters:
                    if cluster[0] is centroids[shortest_index]:
                        cluster.add(sample)

                # Animate the removal of other lines
                self.play(FadeOut(lines))
                self.wait(0.5)

            # Calculate the variances of the clusters and check if the existing centroid changes position
            cluster_means = [(np.mean([sample.get_x() for sample in cluster[1:]]),
                              np.mean([sample.get_y() for sample in cluster[1:]])) for cluster in clusters]

            # Check if cluster centroids are already located at the cluster means
            for i, (cluster, mean_pos) in enumerate(zip(clusters, cluster_means)):
                print(f"DEBUG 0: MEAN POS - {mean_pos}, CENTROID POS - {cluster[0].get_center()[0:2]}")
                centroid_pos = np.round(tuple(cluster[0].get_center()[0:2]), decimals=1)
                mean_pos = np.round(mean_pos, decimals=1)

                if (centroid_pos != mean_pos).any():
                    print(f"\tDEBUG 1: MEAN POS - {mean_pos}, CENTROID POS - {centroid_pos}")
                    centroids_moved = True

                    # # Show a dot at the mean
                    # x_mark = Text("X", font_size=48, color=RED)
                    #
                    # # Position the 'X'
                    # x_mark.move_to((mean_pos[0], mean_pos[1], 0))
                    #
                    # # Add 'X' to the scene
                    # # self.add(x_mark)
                    # self.play(FadeIn(x_mark))

                    # Relocate the centroid
                    self.play(centroids[i].animate.move_to((mean_pos[0], mean_pos[1], 0)), run_time=0.5)

            if centroids_moved:
                # Remove the existing lines
                self.play(FadeOut(*[line for line in assigned_lines]), run_time=1)

                # Make all the sample dots white again
                self.play(*[dot.animate.set_color(WHITE) for dot in samples], run_time=0.5)

            # break

        # # Fade out all elements
        # self.play(FadeOut(rectangle), FadeOut(samples), FadeOut(centroids))
        self.wait(5)
