# Dynamic Clustering Algorithm

This repository implements a dynamic clustering algorithm based on the online k-means algorithm. It features real-time data point assignment to clusters and centroid position updates.

## Algorithm Description

### 1. Initialization

- **Centroids**: User specifies the number of centroids.
- **Bounds**: User provides the bounds for each data input dimension.
- **Outlier Threshold**: User defines a threshold to determine outliers.
- **Cluster Memory**: User defines this value. It determines the maximum number of rejected data points that the centroid should keep track of.

Centroids are randomly placed within the specified bounds.

### 2. Data Point Entry

- Data points enter the space one at a time.

### 3. Data Point Assignment

- For each data point:
  1. Calculate the distance to each centroid.
  2. Focus on the closest centroid.
  3. Determine if the centroid is willing to accept the data point:
     - **Empty Cluster**: Centroid always accepts.
     - **Non-Empty Cluster**: Acceptance depends on the distance:
       - **Distance ≤ Outlier Threshold**: Accept.
       - **Distance > Outlier Threshold**: Reject (data point is an outlier).

### 4. Centroid Update

- When a centroid accepts a data point:
  1. Update its position towards the new data point.
  2. The update distance is calculated as `d * learning_rate`, where:
     - `d` is the distance to the new data point.
     - `learning_rate` is the inverse of the number of data points in the cluster.

## Example Usage

```python
# Example code here

```

