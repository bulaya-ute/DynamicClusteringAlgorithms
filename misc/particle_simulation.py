from manimlib import *
import subprocess
import numpy as np

np.random.seed(852976431)


def calculate_final_position(force, initial_pos, time_):
    # Calculate final position
    xt = initial_pos + 0 * time_ + 0.5 * force * time_ ** 2
    return xt


def repulsion_with_wall(pos: list[float, ...],
                        bounds: list[tuple[float, float]],
                        repulsion_factor: float = 1.0, force_limit: float = None):
    vector = [0 for _ in range(len(pos))]
    for i, val in enumerate(vector):
        force1 = repulsion_factor / (pos[i] - bounds[i][0]) ** 2
        force2 = -repulsion_factor / (pos[i] - bounds[i][1]) ** 2
        resultant = force1 + force2
        if force_limit is not None and abs(resultant) > force_limit and force_limit not in [-float("inf"), float("inf")]:
            force_limit = abs(force_limit)
            if resultant < 0:
                resultant = -force_limit
            else:
                resultant = force_limit
        vector[i] += resultant
    return vector


def repulsion_with_particle(pos: list[float], other_pos: list[float],
                            repulsion_factor: float = 1.0, force_limit: float = None):
    vector = [0 for _ in range(len(pos))]
    for i, val in enumerate(vector):
        sign = (pos[i] - other_pos[i]) / abs(pos[i] - other_pos[i]) if pos[i] != other_pos[i] else 1

        if pos[i] == other_pos[i]:
            force = 0
        else:
            force = (sign * repulsion_factor) / (pos[i] - other_pos[i]) ** 2
        if force_limit is not None and abs(force) > force_limit and force_limit not in [-float("inf"), float("inf")]:
            force_limit = abs(force_limit)
            if force < 0:
                force = -force_limit
            else:
                force = force_limit
        vector[i] += force
    return vector




class RepulsionSimulation(Scene):
    def construct(self) -> None:
        n_particles = 2
        width = 10
        height = 6
        rect = Rectangle(width, height)
        self.play(FadeIn(rect))
        bounds = [(-5.0, 5.0), (-3.0, 3.0)]

        text = Text("Force Vector: []")
        text.next_to(rect, DOWN, buff=0.4)
        self.add(text)

        particles = []
        for _ in range(n_particles):
            radius = 0.1
            pos = [(np.random.uniform((lower + radius), (upper - radius))) for lower, upper in bounds]
            particle = Dot(point=np.array(pos + [0]), radius=radius)
            particles.append(particle)

        self.play(*[FadeIn(p) for p in particles])

        n_frames = 1000000
        frame_time = 0.01
        for _ in range(n_frames):
            animations = []
            for i, particle in enumerate(particles):
                pos = particle.get_center()[:2]

                force_limit = 10000
                repulsion = 10

                wall_vector = repulsion_with_wall(pos, bounds, repulsion_factor=repulsion, force_limit=force_limit)

                # Check if it's not the last one in the list
                if i < len(particles) - 2:
                    other_particles = particles[:i] + particles[i + 1:]
                else:
                    other_particles = particles[:1]

                other_vectors = []
                for other_particle in other_particles:

                    other_pos = other_particle.get_center()[:2]
                    vector = repulsion_with_particle(pos, other_pos, repulsion_factor=repulsion)
                    # print(vector)
                    # exit()
                    other_vectors.append(vector)

                # print(other_vectors)
                other_vectors = [sum(dim_vector) for dim_vector in zip(*other_vectors)]

                # for j, v in enumerate(other_vectors):
                #     if abs(v) > force_limit:
                #         if v < 0:
                #             other_vectors[j] = -force_limit
                #         else:
                #             other_vectors[j] = force_limit

                resultant_vector = [sum(dim_vector) for dim_vector in zip(other_vectors, wall_vector)]

                new_pos = [calculate_final_position(resultant_vector[i], initial, frame_time) for i, initial in enumerate(pos)]
                animations.append(particle.animate.move_to(new_pos + [0]))

            # new_text = Text(f"Vector: {wall_vector}")
            # new_text.move_to(text.get_center())
            # self.remove(text)
            # self.add(new_text)
            # text = new_text
            self.play(*animations, run_time=frame_time)


if __name__ == "__main__":
    subprocess.run("manimgl particle_simulation.py RepulsionSimulation".split())
