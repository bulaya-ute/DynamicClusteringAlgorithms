import itertools
import subprocess
from manimlib import *
import random
import math
import numpy as np

# sample_points = [(2.4658305992895144, 1.6172972798007168), (2.7596883152421237, 1.3832868707980224),
#                  (2.3523028009278337, 1.0820019383433914), (2.7021758597018573, 1.1850205974819472),
#                  (-0.7671196580991739, -0.39206211416293274), (-0.9948567521489593, -0.921956021666712),
#                  (-1.0108145504092583, -0.47519652634637427), (-0.5336671402932296, -1.0046440809079267),
#                  (-4.37750392790103, 0.6931394400258767), (-4.7321888181741105, 0.4804369727514282),
#                  (-4.581582028848124, 1.0047889242161654), (-4.706804872911479, 0.26919433910581525)]

sample_points = [(-1.691756660979375, -2.0141150341998837), (-1.0774187285187329, -2.022563890994003),
                 (-2.0366042120361323, -2.6020241203543724), (-1.3132545658304284, -1.760959656020698),
                 (-0.75558248055401, -2.408513077765004), (-1.7345994216054779, -2.3944089384951024),
                 (-1.067026399267998, -2.6240423451457344), (3.496285376245024, -1.776621315963331),
                 (4.308636710512622, -2.214716345773818), (3.336020891002123, -2.456652889643928),
                 (4.280653986432277, -1.7946190031668843), (4.259112075134916, -2.647016718485209),
                 (3.8898541770232753, -1.87468306567783), (3.6886900815490433, -2.625908153514662),
                 (-2.4776816285389507, 1.9818185242032567), (-2.9294606463781356, 2.5777598857122226),
                 (-2.0733370613986772, 2.6077351069507415), (-1.7073131738981357, 2.5236597455463396),
                 (-2.1076701953941863, 1.9498461171776327), (-2.7967470001349373, 2.1868859159539658),
                 (-1.768134765065815, 2.0856777241252433), (3.210253984573429, -0.3025572004274236),
                 (2.9874387016120627, 0.6030115904501154), (3.547809841485652, 0.4646284362074433),
                 (2.66969577574225, 0.06224134743094045), (3.454586274478035, 0.8025109027484306),
                 (3.5526623241995328, -0.11037420409349291), (2.7732975063880088, -0.2765187695047199),
                 (-0.7715133604352038, 0.08765813907240644), (-0.3818479689744064, -0.7538097390187852),
                 (-1.0967654394427155, -0.5845115493254527), (-0.6922461268118216, -0.9479573617985608),
                 (0.052549866285714564, -0.6523171565721635), (-0.20084490917942044, 0.07162695633216037),
                 (0.04548958324254937, -0.253497176358515)]

random.shuffle(sample_points)

# centroid_points = [(-1.4071639815436434, -2.7868225797427524), (-1.2579876499736493, 0.3097631351116471),
#                    (0.6507108202087171, 2.5291621624495493)]

centroid_points = [(-0.5284978092425833, 0.18499628922194802), (-0.12365414799156849, -1.0355620876130516),
                   (3.085496820218155, -2.4887500632879194), (3.514191636038472, 0.6806900912421558),
                   (-3.9941593591079694, 1.090299925732625)]

colors = [BLUE, GREEN, RED, PURPLE, ORANGE, YELLOW, GREY]

num_clusters = 5


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


class DynamicClustering(Scene):
    def construct(self):
        points_on_scene = []
        centroids_on_scene = []

        # info = {"Dispersion": 0}
        # info_text = Text(f"Dispersion: {info['Dispersion']}", font_size=30)
        # info_text.to_edge(DOWN)
        # self.play(FadeIn(info_text))

        rect = Rectangle(width=10, height=6)
        self.play(FadeIn(rect))

        # random.shuffle(sample_points)
        for i, point in enumerate(centroid_points):
            # dot = Dot(point + (0,), radius=0.2, stroke_color=GREY, stroke_width=0.04, color=colors[i])
            dot = Text("X", color=colors[i])
            dot.move_to(point + (0,))

            centroids_on_scene.append(dot)
        clusters = [[cen] for cen in centroids_on_scene]

        # self.play(FadeIn(*centroids_on_scene))
        self.add(*centroids_on_scene)

        for point in sample_points:
            dot = Dot(point + (0,), radius=0.1)
            points_on_scene.append(dot)
            self.play(FadeIn(dot))
            dot_pos = dot.get_center()

            # Calculate distances with the centroids
            distances = []
            for centroid in centroids_on_scene:
                centroid_pos = centroid.get_center()
                distance = sum([(p1 - p2) ** 2 for p1, p2 in zip(dot_pos, centroid_pos)])
                distances.append(distance)

            # Assign point to nearest cluster
            shortest_index = distances.index(min(distances))
            assigned_centroid = centroids_on_scene[shortest_index]

            for c in clusters:
                if c[0] is assigned_centroid:
                    c.append(dot)
                    cluster_of_choice = c
                    break
            else:
                raise RuntimeError("Oops!")

            self.play(dot.animate.set_color(assigned_centroid.color))

            # Move centroid to mean position of cluster
            # mean_pos = [np.mean(dim) for dim in list(zip(*[tuple(dot.get_center()) for dot in cluster_of_choice[1:]]))]

            learning_rate = 1 / max(len(cluster_of_choice[1:]), 1)
            dest_pos = travel_towards(cluster_of_choice[0].get_center(), cluster_of_choice[-1].get_center(),
                                      learning_rate)

            self.play(cluster_of_choice[0].animate.move_to(dest_pos))


if __name__ == "__main__":
    # subprocess.run("manim -pql animation_main.py DynamicClustering".split())
    subprocess.run("manimgl animation_main.py DynamicClustering".split())
