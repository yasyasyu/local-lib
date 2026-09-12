"""mo.pyのテストコード"""

import random
import sys
import unittest
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mo import Mo


class TestMo(unittest.TestCase):
    def test_no_queries_returns_empty_list(self):
        mo = Mo(5)
        self.assertEqual(mo.solve(lambda i: None, lambda i: None, lambda: 0), [])

    def test_add_query_returns_sequential_index(self):
        mo = Mo(5)
        self.assertEqual(mo.add_query(0, 2), 0)
        self.assertEqual(mo.add_query(1, 3), 1)

    def test_counts_distinct_values_in_range(self):
        a = [1, 2, 1, 3, 2, 1]
        n = len(a)
        mo = Mo(n)
        queries = [(0, 6), (0, 3), (2, 5), (1, 1), (3, 6)]
        for l, r in queries:
            mo.add_query(l, r)

        count = defaultdict(int)
        distinct = [0]

        def add(i):
            if count[a[i]] == 0:
                distinct[0] += 1
            count[a[i]] += 1

        def remove(i):
            count[a[i]] -= 1
            if count[a[i]] == 0:
                distinct[0] -= 1

        def answer():
            return distinct[0]

        result = mo.solve(add, remove, answer)
        expected = [len(set(a[l:r])) for l, r in queries]
        self.assertEqual(result, expected)

    def test_matches_brute_force_randomized(self):
        random.seed(0)
        for _ in range(10):
            n = random.randint(1, 30)
            a = [random.randint(0, 5) for _ in range(n)]
            q = random.randint(1, 20)
            queries = []
            mo = Mo(n)
            for _ in range(q):
                l = random.randint(0, n - 1)
                r = random.randint(l + 1, n)
                queries.append((l, r))
                mo.add_query(l, r)

            count = defaultdict(int)
            distinct = [0]
            total = [0]

            def add(i):
                if count[a[i]] == 0:
                    distinct[0] += 1
                count[a[i]] += 1
                total[0] += a[i]

            def remove(i):
                count[a[i]] -= 1
                if count[a[i]] == 0:
                    distinct[0] -= 1
                total[0] -= a[i]

            def answer():
                return (distinct[0], total[0])

            result = mo.solve(add, remove, answer)
            expected = [
                (len(set(a[l:r])), sum(a[l:r])) for l, r in queries
            ]
            self.assertEqual(result, expected, (a, queries))


if __name__ == "__main__":
    unittest.main()
