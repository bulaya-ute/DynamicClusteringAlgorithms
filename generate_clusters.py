import datetime
import os

import numpy as np
import matplotlib.pyplot as plt
import json


def generate_clusters(_num_clusters, _avg_points_per_cluster, _width, _height, _min_distance,
                      _avg_num_outliers, variance=2):
    np.random.seed(564552)  # For reproducibility

    _points = []

    # Rectangle bounds
    x_min, x_max = -_width / 2, _width / 2
    y_min, y_max = -_height / 2, _height / 2

    centroids = []
    for _ in range(_num_clusters):
        valid = False
        while not valid:
            # valid = False
            cx = np.random.uniform(x_min + _min_distance, x_max - _min_distance)
            cy = np.random.uniform(y_min + _min_distance, y_max - _min_distance)
            for cx2, cy2 in centroids:
                if ((cx - cx2) ** 2 + (cy - cy2) ** 2) ** 0.5 < _min_distance:
                    valid = False
                    break
            else:
                centroids.append((cx, cy))
                valid = True
                break

    for cx, cy in centroids:
        # Randomize the number of points in the cluster
        num_points = np.random.randint(max(1, _avg_points_per_cluster - variance),
                                       _avg_points_per_cluster + variance + 1)

        for _ in range(num_points):
            valid = False
            while not valid:
                angle = np.random.uniform(0, 2 * np.pi)
                distance = np.random.uniform(0, _min_distance)
                px = cx + distance * np.cos(angle)
                py = cy + distance * np.sin(angle)

                # Check bounds
                if x_min + _min_distance <= px <= x_max - _min_distance and \
                        y_min + _min_distance <= py <= y_max - _min_distance:
                    _points.append((px, py))
                    valid = True

    # Generate outliers
    num_outliers = np.random.randint(max(0, _avg_num_outliers - variance), _avg_num_outliers + variance + 1)
    outliers = []
    for _ in range(num_outliers):
        valid = False
        while not valid:
            px = np.random.uniform(x_min, x_max)
            py = np.random.uniform(y_min, y_max)
            # Check distance with centroids and other outliers
            if all(np.sqrt((px - ox) ** 2 + (py - oy) ** 2) >= (_min_distance*2) for ox, oy in centroids + outliers):
                outliers.append((px, py))
                valid = True
    _points += outliers
    return _points


def save_data_to_json(_points, _width, _height, filename, _centroids=None):
    """
    Save the generated points and the rectangle bounds to a JSON file.

    Parameters:
    - points: List of tuples representing the coordinates of the points.
    - width: Width of the enclosing rectangle.
    - height: Height of the enclosing rectangle.
    - filename: The name of the file to save the data to.
    """
    x_min, x_max = -_width / 2, _width / 2
    y_min, y_max = -_height / 2, _height / 2

    data = {
        'sample_points': _points,
        'bounds': {
            'x': [x_min, x_max],
            'y': [y_min, y_max]
        }
    }
    if _centroids:
        data["centroid_points"] = _centroids
    with open(filename, 'w') as f:
        json.dump(data, f)


# Parameters
width = 10
height = 6
num_clusters = 5
avg_points_per_cluster = 30
min_distance = 0.7
avg_num_outliers = 10

# Generate points
points = generate_clusters(num_clusters, avg_points_per_cluster, width, height, min_distance, avg_num_outliers,
                           variance=0)
centroids = generate_clusters(num_clusters, 1, width, height, min_distance, 0,
                              variance=0)

# Save points and rectangle bounds to JSON file
save_data_to_json(points, width, height,
                  f"datasets/dataset{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
                  _centroids=centroids)

# Print points and bounds
print("Generated Points:", points)
print("Bounds:", {
    'x': [-width / 2, width / 2],
    'y': [-height / 2, height / 2]
})

# Visualization
plt.figure(figsize=(10, 6))

# Unzip points for plotting
x_point, y_point = zip(*points)
x_centroid, y_centroid = zip(*centroids)

# Create rectangle centered at origin
rectangle = plt.Rectangle(
    (-width / 2, -height / 2), width, height,
    linewidth=2, edgecolor='green', facecolor='none', label='Enclosing Rectangle'
)

# Plot points
plt.scatter(x_point, y_point, color='red', label='Generated Points')
plt.scatter(x_centroid, y_centroid, color='blue', label='Generated Centroids')

# Add rectangle to plot
plt.gca().add_patch(rectangle)

# Plot configurations
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.legend()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Generated Points with Enclosing Rectangle')
plt.grid(True)
plt.xlim(-width / 2 - 1, width / 2 + 1)  # Extend x-axis slightly to fit rectangle
plt.ylim(-height / 2 - 1, height / 2 + 1)  # Extend y-axis slightly to fit rectangle
plt.show()
