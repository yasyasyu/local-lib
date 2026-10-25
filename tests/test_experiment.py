"""experiment.pyのテストコード"""

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from experiment import arrays, bfs_states, graphs, permutations, show, strings, stress, table, trees


def connected(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    return len({find(v) for v in range(n)}) == 1


class TestGenerators(unittest.TestCase):
    def test_docstring_examples(self):
        self.assertEqual(list(arrays(2, 0, 1)), [(0, 0), (0, 1), (1, 0), (1, 1)])
        self.assertEqual(list(strings(2, "ab")), ["aa", "ab", "ba", "bb"])
        self.assertEqual(len(list(permutations(3))), 6)
        self.assertEqual(len(list(trees(4))), 16)
        self.assertEqual(len(list(graphs(3))), 8)
        self.assertEqual(len(list(graphs(3, connected=True))), 4)

    def test_trees_are_distinct_spanning_trees(self):
        for n in range(1, 7):
            all_trees = list(trees(n))
            self.assertEqual(len(all_trees), n ** (n - 2) if n >= 2 else 1)
            keys = set()
            for edges in all_trees:
                self.assertEqual(len(edges), n - 1)
                self.assertTrue(connected(n, edges))
                keys.add(frozenset(frozenset(e) for e in edges))
            self.assertEqual(len(keys), len(all_trees))

    def test_connected_graph_counts(self):
        # 頂点数 1〜5 のラベル付き連結グラフの個数
        self.assertEqual([len(list(graphs(n, connected=True))) for n in range(1, 6)], [1, 1, 4, 38, 728])


class TestBfsStates(unittest.TestCase):
    def test_docstring_example(self):
        def moves(p):
            for i in range(len(p) - 1):
                q = list(p)
                q[i], q[i + 1] = q[i + 1], q[i]
                yield tuple(q)

        dist = bfs_states((2, 0, 1), moves)
        self.assertEqual(dist[(0, 1, 2)], 2)
        self.assertIn((1, 0, 2), dist)
        self.assertEqual(len(dist), 6)

    def test_unreachable(self):
        dist = bfs_states(0, lambda x: [x + 2] if x < 10 else [])
        self.assertEqual(dist, {0: 0, 2: 1, 4: 2, 6: 3, 8: 4, 10: 5})
        self.assertNotIn(1, dist)


class TestOutput(unittest.TestCase):
    def test_show(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            show(sum, [(1, 2), (3,)])
        self.assertEqual(buf.getvalue(), "(1, 2) -> 3\n(3,) -> 3\n")

    def test_table_docstring_example(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            table(lambda n, k: n * k, range(1, 4), range(0, 3))
        self.assertEqual(buf.getvalue(), "  | 0 1 2\n---------\n1 | 0 1 2\n2 | 0 2 4\n3 | 0 3 6\n")

    def test_stress_finds_counterexample(self):
        brute = lambda a: max(a)
        wrong = lambda a: a[-1]
        gen = lambda rng: tuple(rng.randint(0, 3) for _ in range(rng.randint(1, 4)))
        buf = io.StringIO()
        with redirect_stdout(buf):
            x = stress(wrong, brute, gen)
        self.assertIsNotNone(x)
        self.assertNotEqual(wrong(x), brute(x))
        self.assertIn("反例", buf.getvalue())

    def test_stress_all_match(self):
        gen = lambda rng: tuple(rng.randint(0, 3) for _ in range(rng.randint(1, 4)))
        buf = io.StringIO()
        with redirect_stdout(buf):
            x = stress(lambda a: max(a), lambda a: sorted(a)[-1], gen, trials=100)
        self.assertIsNone(x)
        self.assertEqual(buf.getvalue(), "100 件すべて一致\n")


if __name__ == "__main__":
    unittest.main()
