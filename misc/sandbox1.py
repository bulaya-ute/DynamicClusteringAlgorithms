import numpy as np
import matplotlib.pyplot as plt

# Original sample points
sample_points = [
    (0.2218330988875646, 1.0191359996764715), (0.17658274339163582, 1.3569781605162081),
    (0.7381177331966775, 1.1424361440770663), (0.5478593827167472, 0.9097296795994058),
    (0.8493537798069922, 2.477195312977458), (0.7190494714412317, 2.015176370070864),
    (1.0098171587948328, 2.3351448972444895), (0.3075014089838477, 2.4686912640266794),
    (-3.423018372273402, 1.088392867231354), (-3.944836154687986, 0.7448394700676745),
    (-3.696973014983087, 1.136921499577464), (-3.3432904737337705, 0.8216645962758133)
]

# Dispersal parameters
dispersal_factors = [1, 2.0, 1.5]  # Scaling factors for each cluster
dispersal_offsets = [(0.5, -1.5), (0.5, -0.5), (-0.5, 0.5)]  # Offsets for each cluster

# Apply dispersal to clusters
dispersed_points = []

# Cluster 1
for point in sample_points[:4]:
    dispersed_points.append((
        point[0] * dispersal_factors[0] + dispersal_offsets[0][0],
        point[1] * dispersal_factors[0] + dispersal_offsets[0][1]
    ))

# Cluster 2
for point in sample_points[4:8]:
    dispersed_points.append((
        point[0] * dispersal_factors[1] + dispersal_offsets[1][0],
        point[1] * dispersal_factors[1] + dispersal_offsets[1][1]
    ))

# Cluster 3
for point in sample_points[8:]:
    dispersed_points.append((
        point[0] * dispersal_factors[2] + dispersal_offsets[2][0],
        point[1] * dispersal_factors[2] + dispersal_offsets[2][1]
    ))

# Print new dispersed points
print("Dispersed Points:", dispersed_points)
# for point in dispersed_points:
#     print(point)

# Visualization
plt.figure(figsize=(10, 6))
original_x, original_y = zip(*sample_points)
dispersed_x, dispersed_y = zip(*dispersed_points)

plt.scatter(original_x, original_y, color='blue', label='Original Points')
plt.scatter(dispersed_x, dispersed_y, color='red', label='Dispersed Points')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.legend()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Original vs. Dispersed Points')
plt.grid(True)
plt.show()
