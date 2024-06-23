from manim import *
import random
import math


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
        while centroids_moved:
            centroids_moved = False

            # A cluster will be a group of dots in this case. The first item in the group will be the centroid
            # dot
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
                    if cluster[0] is

                # Animate the removal of other lines
                self.play(FadeOut(lines))
                self.wait(0.5)

            # Add the recognised cluster

        # # Fade out all elements
        # self.play(FadeOut(rectangle), FadeOut(samples), FadeOut(centroids))
