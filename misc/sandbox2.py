import numpy as np
import matplotlib.pyplot as plt


def generate_radially_distributed_points(x_min, x_max, y_min, y_max, radius, num_points):
    """
    Generates points in a 2D plane such that they are dispersed from the center outwards.

    Parameters:
    - x_min, x_max: The lower and upper limits for the x-axis.
    - y_min, y_max: The lower and upper limits for the y-axis.
    - radius: Radius of the circular region around each point.
    - num_points: Number of points to generate.

    Returns:
    - points: List of (x, y) coordinates of the generated points.
    """

    # Calculate the center of the bounding box
    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2

    # Initialize the list to store points
    points = []

    # Angle increment per point for even distribution around the circle
    angle_increment = 2 * np.pi / num_points

    for i in range(num_points):
        # Calculate the distance from the center, growing outward
        distance = np.sqrt(i + 1) * radius

        # Determine the angle for the current point
        angle = i * angle_increment

        # Calculate the position of the point
        x = center_x + distance * np.cos(angle)
        y = center_y + distance * np.sin(angle)

        # Ensure the point is within bounds
        x = np.clip(x, x_min + radius, x_max - radius)
        y = np.clip(y, y_min + radius, y_max - radius)

        points.append((x, y))

    return points


# Example usage:
x_min, x_max = 0, 10
y_min, y_max = 0, 10
radius = 0.5
num_points = 4

points = generate_radially_distributed_points(x_min, x_max, y_min, y_max, radius, num_points)

# Print generated points
print("Generated Points:", points)

# Plotting
fig, ax = plt.subplots()
x, y = zip(*points)
ax.scatter(x, y, color='red')

# Plot circles around each point
for (px, py) in points:
    circle = plt.Circle((px, py), radius, color='blue', fill=False)
    ax.add_patch(circle)

# Plot configuration
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Radially Distributed Points with Circular Regions')
plt.grid(True)
plt.show()
