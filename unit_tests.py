import unittest
from dynamic_algorithm import *


class TestDatatypes(unittest.TestCase):
    def test_point_plus_point(self):
        p1 = DataPoint((0, 0))
        p2 = DataPoint((0, 0))
        self.assertTrue(isinstance((p1 + p2), Cluster),
                        msg="'Point' + 'Point' should return a 'Cluster'.")

    def test_point_plus_cluster(self):
        p1 = DataPoint((0, 0))
        cluster1 = Cluster()
        self.assertTrue(isinstance((p1 + cluster1), Cluster),
                        msg="'Point' + 'Cluster' should return a 'Cluster'")

    def test_cluster_plus_point(self):
        p1 = DataPoint((0, 0))
        cluster1 = Cluster((0, 0), 1)
        self.assertTrue(isinstance((cluster1 + p1), Cluster),
                        msg="'Cluster' + 'Point' should return a 'Cluster'")


class TestPointOperations(unittest.TestCase):
    def test_distance_calculation_point_to_point(self):
        # coordinate1, coordinate2, expected_distance
        test_values = [((0, 0), (0, 0), 0),
                       ((0, 0), (1, 1), 1.4142135623730951),
                       ((10, 10), (11, 11), 1.4142135623730951),
                       ((0, 0, 0), (0, 0, 0), 0),
                       ((5, 5, 5), (5, 5, 5), 0),
                       ((3, 4, 5, 6), (3, 4, 5, 6), 0),
                       ((1, 2, 3, 4), (5, 6, 7, 8), 8),
                       ((1, 2, 3, 4), (8, 7, 6, 5), 9.16515138991168)]

        for coord1, coord2, expected_distance in test_values:
            with self.subTest(coord1=coord1, coord2=coord2, expected_distance=expected_distance):
                p1 = DataPoint(coord1)
                p2 = DataPoint(coord2)
                self.assertEqual(expected_distance, p1.distance_with(p2))
                self.assertEqual(expected_distance, p2.distance_with(p1))
                self.assertEqual(p1.distance_with(p2), p2.distance_with(p1))


if __name__ == '__main__':
    unittest.main()
