import itertools
import subprocess
from manim import *
import random
import math

import numpy as np

sample_points = [(2.4658305992895144, 1.6172972798007168), (2.7596883152421237, 1.3832868707980224),
                 (2.3523028009278337, 1.0820019383433914), (2.7021758597018573, 1.1850205974819472),
                 (-0.7671196580991739, -0.39206211416293274), (-0.9948567521489593, -0.921956021666712),
                 (-1.0108145504092583, -0.47519652634637427), (-0.5336671402932296, -1.0046440809079267),
                 (-4.37750392790103, 0.6931394400258767), (-4.7321888181741105, 0.4804369727514282),
                 (-4.581582028848124, 1.0047889242161654), (-4.706804872911479, 0.26919433910581525)]

centroid_points = [(-1.4071639815436434, -2.7868225797427524), (-1.2579876499736493, 0.3097631351116471),
                   (0.6507108202087171, 2.5291621624495493)]


class KMeans(Scene):
    def construct(self):
        colors = [BLUE, GREEN, RED, PURPLE, ORANGE, YELLOW, GREY]

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

        # Initialize the samples
        for x, y in sample_points:
            dot = Dot(point=(x, y, 0), color=WHITE, radius=0.1)
            samples.add(dot)

        # Initialize the centroids
        for i, (x, y) in enumerate(centroid_points):
            # # Generate random coordinates within the rectangle
            # x = random.uniform(-rect_half_width + dot_radius, rect_half_width - dot_radius)  # Rectangle width / 2
            # y = random.uniform(-rect_half_height + dot_radius, rect_half_height - dot_radius)  # Rectangle height / 2

            dot = Dot(point=(x, y, 0), color=colors[i], radius=0.15)
            centroids.add(dot)

        # Add the samples to the scene
        self.play(FadeIn(samples))
        self.wait(2)

        # Add the centroid to the scene
        self.play(FadeIn(centroids))
        self.wait(2)

        for interation_num in itertools.count():
            centroids_moved = False

            # A cluster will be a group of dots in this case. The first item in the group
            # will be the centroid dot
            clusters = [VGroup(centroid) for centroid in centroids]
            assigned_lines = VGroup()

            if interation_num < 0:
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
            else:
                connect_lines_animations = []
                change_line_color_animations = []
                fade_out_lines_animations = []
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
                    connect_lines_animations += [Create(line) for line in lines]
                    # self.play(*[Create(line) for line in lines], run_time=0.5)
                    # self.wait(0.5)

                    # Change the color of the shortest line and its sample to suit its associated centroid
                    shortest_index = distances.index(min(distances))
                    # self.play(lines[shortest_index].animate.set_color(centroids[shortest_index].get_color()),
                    #           sample.animate.set_color(centroids[shortest_index].get_color()), run_time=0.5)
                    change_line_color_animations += [
                        lines[shortest_index].animate.set_color(centroids[shortest_index].get_color()),
                        sample.animate.set_color(centroids[shortest_index].get_color())
                    ]
                    assigned_lines.add(lines[shortest_index])
                    lines.remove(lines[shortest_index])

                    # Add dot to the cluster
                    for cluster in clusters:
                        if cluster[0] is centroids[shortest_index]:
                            cluster.add(sample)

                    # Animate the removal of other lines
                    # self.play(FadeOut(lines))
                    fade_out_lines_animations.append(FadeOut(lines))
                    # self.wait(0.5)

                # if interation_num < 0:
                #     print(f"DEBUG: connect animations: {len(connect_lines_animations)}")
                #     print(f"DEBUG: fade-line animations: {len(fade_out_lines_animations)}")
                #     print(f"DEBUG: change color animations: {len(change_line_color_animations)}")
                #     for i in range(0, len(connect_lines_animations), 3):
                #         self.play(*connect_lines_animations[i: i + 3], run_time=1)
                #         # l1 = int(i / 1.5)
                #         # l2 = l1 + 2
                #         # self.play(*fade_out_lines_animations[l1:l2], run_time=1)
                #         # c1 = int(i / 3)
                #         # c2 = c1 + 1
                #         # self.play(*change_line_color_animations[c1:c2], run_time=1.0)
                #
                #     # # self.play(*connect_lines_animations, run_time=1.0)
                #     # # [self.play(anim, run_time=0.5) for anim in connect_lines_animations]
                #     # [self.play(*connect_lines_animations[i: i + 3], run_time=0.5) for i in
                #     #  range(0, len(connect_lines_animations), 3)]
                #     # self.wait(0.5)
                #     [self.play(anim, run_time=0.5) for anim in fade_out_lines_animations]
                #     # self.wait(0.5)
                #     [self.play(anim, run_time=0.5) for anim in change_line_color_animations]
                #
                # else:
                self.play(*connect_lines_animations, run_time=1.0)
                self.wait(0.5)
                self.play(*fade_out_lines_animations, run_time=1.0)
                # self.wait(0.5)
                self.play(*change_line_color_animations, run_time=1.5)

                # raise NotImplementedError

            # Calculate the variances of the clusters and check if the existing centroid changes position
            cluster_means = [(np.mean([sample.get_x() for sample in cluster[1:]]),
                              np.mean([sample.get_y() for sample in cluster[1:]])) for cluster in clusters]

            # Check if cluster centroids are already located at the cluster means
            for i, (cluster, mean_pos) in enumerate(zip(clusters, cluster_means)):
                if np.isnan(mean_pos[0]) or np.isnan(mean_pos[1]):
                    continue
                # print(f"DEBUG 0: MEAN POS - {mean_pos}, CENTROID POS - {cluster[0].get_center()[0:2]}")
                centroid_pos = cluster[0].get_center()[0:2]

                if mean_pos[0] != centroid_pos[0] or mean_pos[1] != centroid_pos[1]:
                    # print(f"\tDEBUG 1: MEAN POS - {mean_pos}, CENTROID POS - {centroid_pos}")
                    centroids_moved = True
                    self.play(centroids[i].animate.move_to((mean_pos[0], mean_pos[1], 0)), run_time=0.5)

            if centroids_moved:  # or interation_num < 10:
                # Remove the existing lines
                self.play(FadeOut(*[line for line in assigned_lines]), run_time=1)

                # Make all the sample dots white again
                self.play(*[dot.animate.set_color(WHITE) for dot in samples], run_time=0.5)
            else:
                break

            if interation_num >= 5:
                break

        # # Fade out all elements
        self.wait(5)
        self.play(FadeOut(rectangle), FadeOut(samples), FadeOut(centroids), FadeOut(assigned_lines))


class DynamicClustering(Scene):
    def construct(self):
        points = []
        clusters = []

