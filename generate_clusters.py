# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def generate_clusters(num_clusters, points_per_cluster, width, height, min_distance):
#     np.random.seed(57984687)  # For reproducibility
#     clusters = []
#     points = []
#
#     # Rectangle bounds
#     x_min, x_max = -width / 2, width / 2
#     y_min, y_max = -height / 2, height / 2
#
#     for _ in range(num_clusters):
#         # Ensure the cluster center is within the bounds with padding for point generation
#         cx = np.random.uniform(x_min + min_distance, x_max - min_distance)
#         cy = np.random.uniform(y_min + min_distance, y_max - min_distance)
#         clusters.append((cx, cy))
#
#         for _ in range(points_per_cluster):
#             valid = False
#             while not valid:
#                 angle = np.random.uniform(0, 2 * np.pi)
#                 distance = np.random.uniform(min_distance, min_distance * 2)
#                 px = cx + distance * np.cos(angle)
#                 py = cy + distance * np.sin(angle)
#
#                 # Check bounds
#                 if x_min + min_distance <= px <= x_max - min_distance and \
#                         y_min + min_distance <= py <= y_max - min_distance:
#                     # Check distance to other points
#                     if all(np.sqrt((px - ox) ** 2 + (py - oy) ** 2) >= min_distance for ox, oy in points):
#                         points.append((px, py))
#                         valid = True
#
#     return points
#
#
# # Parameters
# width = 10
# height = 6
# num_clusters = 5
# points_per_cluster = 1
# min_distance = 0.35
#
# # Generate points
# points = generate_clusters(num_clusters, points_per_cluster, width, height, min_distance)
#
# # Print points
# print("Generated Points:", points)
#
# # Visualization
# plt.figure(figsize=(10, 6))
#
# # Unzip points for plotting
# x, y = zip(*points)
#
# # Create rectangle centered at origin
# rectangle = plt.Rectangle(
#     (-width / 2, -height / 2), width, height,
#     linewidth=2, edgecolor='green', facecolor='none', label='Enclosing Rectangle'
# )
#
# # Plot points
# plt.scatter(x, y, color='red', label='Generated Points')
#
# # Add rectangle to plot
# plt.gca().add_patch(rectangle)
#
# # Plot configurations
# plt.axhline(0, color='gray', linestyle='--')
# plt.axvline(0, color='gray', linestyle='--')
# plt.legend()
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Generated Points with Enclosing Rectangle')
# plt.grid(True)
# plt.xlim(-width / 2 - 1, width / 2 + 1)  # Extend x-axis slightly to fit rectangle
# plt.ylim(-height / 2 - 1, height / 2 + 1)  # Extend y-axis slightly to fit rectangle
# plt.show()
