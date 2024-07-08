import math
import matplotlib.pyplot as plt


def compute_particle_positions(n, width, height):
    # Determine the number of rows and columns for grid layout
    rows = int(math.sqrt(n))
    cols = math.ceil(n / rows)

    # Calculate horizontal and vertical spacing between particles
    if cols > 1:
        horizontal_spacing = width / (cols + 1)
    else:
        horizontal_spacing = width / 2

    if rows > 1:
        vertical_spacing = height / (rows + 1)
    else:
        vertical_spacing = height / 2

    # Calculate the starting padding
    x_padding = horizontal_spacing
    y_padding = vertical_spacing

    positions = []
    particle_idx = 0

    for i in range(rows):
        for j in range(cols):
            if particle_idx >= n:
                break
            x = x_padding + j * horizontal_spacing
            y = y_padding + i * vertical_spacing
            positions.append((x, y))
            particle_idx += 1

    return positions


def plot_particles(n, width, height, positions):
    plt.figure(figsize=(8, 4))
    plt.scatter(*zip(*positions), color='blue', marker='o', s=100, label='Particles')

    # Draw the rectangle
    plt.gca().add_patch(plt.Rectangle((0, 0), width, height, fill=None, edgecolor='black', linewidth=2))

    plt.xlim(-10, width + 10)
    plt.ylim(-10, height + 10)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f'{n} Particles in {width}x{height} Rectangle')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.grid(True)
    plt.legend()
    plt.show()


# Example usage
n = 10
width = 100
height = 50

positions = compute_particle_positions(n, width, height)
plot_particles(n, width, height, positions)
