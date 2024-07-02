# Dynamic Clustering Algorithm

This repository implements a dynamic clustering algorithm based on the online k-means algorithm. It features real-time data point assignment to clusters and centroid position updates.

## Algorithm Description

### 1. Initialization

- **Centroids**: User specifies the number of centroids. There as many centroids as there are clusters.
- **Bounds**: User provides the bounds for each data input dimension. Upper and lower limits for expected values in the dataset
- **Outlier Threshold**: User defines a threshold to determine outliers.
- **Cluster Memory**: User defines this value. It determines the maximum number of outliers that a cluster should keep track of.

Centroids are randomly placed within the specified bounds.

### 2. Data Point Entry

- Data points enter the space one at a time.

### 3. Data Point Assignment

- For each data point:
  1. Calculate the distance to each centroid.
  2. Focus on the closest centroid.
  3. Determine if the centroid is 'willing' to accept the data point:
     - **Empty Cluster**: Centroid always accepts (always willing).
     - **Non-Empty Cluster**: Acceptance depends on the distance:
       - **Distance ≤ Outlier Threshold**: Accept.
       - **Distance > Outlier Threshold**: Reject (data point is an outlier).
  4. If the centroid accepts the new data point, the data point is added to the cluster, and the centroid position updated.
  5. If the centroid rejects the new data point, it is flagged as an outlier. The outlier then updates the memory of the cluster that just rejected it, as well as all the empty clusters.

### 4. Memory update

- Cluster memory is updated based on free space and priority. This allows a cluster to remember a relevant outlier, and possibly add the outlying data point to itself in the future.
- If there is enough memory available, a data point that was just rejected will always be 'remembered' (added to memory).
- Memory is 'full' when the number of outliers a cluster has in its memory is equal to the user-specified `cluster_memory`.
- If memory

### 5. Centroid Update

- When a centroid accepts a data point:
  1. Update its position towards the new data point.
  2. The update distance is calculated as `d * learning_rate`, where:
     - `d` is the distance to the new data point.
     - `learning_rate` is the inverse of the number of data points in the cluster.

## Example Usage

```python
# To be documented soon...

```

