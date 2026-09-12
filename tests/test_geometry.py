"""geometry.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from geometry import (
    ccw,
    convex_hull,
    cross,
    on_segment,
    point_in_polygon,
    segments_intersect,
)


class TestCrossCcw(unittest.TestCase):
    def test_cross_sign(self):
        self.assertGreater(cross((0, 0), (1, 0), (1, 1)), 0)
        self.assertLess(cross((0, 0), (1, 1), (1, 0)), 0)
        self.assertEqual(cross((0, 0), (1, 1), (2, 2)), 0)

    def test_ccw(self):
        self.assertEqual(ccw((0, 0), (1, 0), (1, 1)), 1)
        self.assertEqual(ccw((0, 0), (1, 1), (1, 0)), -1)
        self.assertEqual(ccw((0, 0), (1, 1), (2, 2)), 0)


class TestOnSegment(unittest.TestCase):
    def test_point_between(self):
        self.assertTrue(on_segment((0, 0), (4, 0), (2, 0)))

    def test_point_outside_bounding_box(self):
        self.assertFalse(on_segment((0, 0), (4, 0), (5, 0)))


class TestConvexHull(unittest.TestCase):
    def _assert_valid_hull(self, points, hull):
        n = len(hull)
        for i in range(n):
            p, q = hull[i], hull[(i + 1) % n]
            for r in points:
                self.assertGreaterEqual(cross(p, q, r), 0, (p, q, r, hull))

    def test_square_with_interior_point(self):
        points = [(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)]
        hull = convex_hull(points)
        self.assertEqual(sorted(hull), [(0, 0), (0, 2), (2, 0), (2, 2)])
        self._assert_valid_hull(points, hull)

    def test_collinear_points_excluded(self):
        points = [(0, 0), (1, 0), (2, 0), (2, 2), (0, 2)]
        hull = convex_hull(points)
        self.assertNotIn((1, 0), hull)
        self._assert_valid_hull(points, hull)

    def test_single_point(self):
        self.assertEqual(convex_hull([(1, 1)]), [(1, 1)])

    def test_empty(self):
        self.assertEqual(convex_hull([]), [])

    def test_matches_validity_randomized(self):
        random.seed(0)
        for _ in range(30):
            points = [
                (random.randint(-10, 10), random.randint(-10, 10)) for _ in range(20)
            ]
            hull = convex_hull(points)
            self._assert_valid_hull(points, hull)
            # 凸包の頂点は全て入力点集合に含まれること
            point_set = set(points)
            for p in hull:
                self.assertIn(p, point_set)


class TestSegmentsIntersect(unittest.TestCase):
    def test_crossing_segments(self):
        self.assertTrue(segments_intersect((0, 0), (2, 2), (0, 2), (2, 0)))

    def test_non_intersecting_parallel(self):
        self.assertFalse(segments_intersect((0, 0), (1, 0), (0, 1), (1, 1)))

    def test_touching_at_endpoint(self):
        self.assertTrue(segments_intersect((0, 0), (1, 1), (1, 1), (2, 0)))

    def test_collinear_overlapping(self):
        self.assertTrue(segments_intersect((0, 0), (2, 0), (1, 0), (3, 0)))

    def test_collinear_non_overlapping(self):
        self.assertFalse(segments_intersect((0, 0), (1, 0), (2, 0), (3, 0)))

    def test_disjoint_segments(self):
        self.assertFalse(segments_intersect((0, 0), (1, 1), (5, 5), (6, 6)))


class TestPointInPolygon(unittest.TestCase):
    def setUp(self):
        self.square = [(0, 0), (4, 0), (4, 4), (0, 4)]

    def test_inside(self):
        self.assertEqual(point_in_polygon((2, 2), self.square), 1)

    def test_outside(self):
        self.assertEqual(point_in_polygon((5, 5), self.square), -1)

    def test_on_edge(self):
        self.assertEqual(point_in_polygon((0, 2), self.square), 0)

    def test_on_vertex(self):
        self.assertEqual(point_in_polygon((0, 0), self.square), 0)

    def test_concave_polygon(self):
        # L字型のへこんだ多角形（左上2x2の領域だけ欠けている）
        polygon = [(0, 0), (4, 0), (4, 4), (2, 4), (2, 2), (0, 2)]
        self.assertEqual(point_in_polygon((1, 1), polygon), 1)  # 下側の領域内
        self.assertEqual(point_in_polygon((3, 3), polygon), 1)  # 右上の領域内
        self.assertEqual(point_in_polygon((1, 3), polygon), -1)  # 欠けている左上の領域


if __name__ == "__main__":
    unittest.main()
