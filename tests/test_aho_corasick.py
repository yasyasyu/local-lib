"""aho_corasick.pyのテストコード"""

import itertools
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from aho_corasick import AhoCorasick


def brute_find_all(text, patterns):
    res = []
    for end in range(len(text)):
        for pid, p in sorted(enumerate(patterns), key=lambda t: -len(t[1])):
            start = end - len(p) + 1
            if start >= 0 and text[start : end + 1] == p:
                res.append((start, pid))
    return res


class TestAhoCorasick(unittest.TestCase):
    def test_docstring_examples(self):
        ac = AhoCorasick(["he", "she", "his", "hers"])
        self.assertEqual(ac.match_counts("ushers"), [1, 1, 0, 1])
        self.assertEqual(ac.find_all("ushers"), [(1, 1), (2, 0), (2, 3)])

    def test_dp_example(self):
        patterns = ["ab", "ca"]
        ac = AhoCorasick(patterns)
        for L in range(0, 7):
            dp = {0: 1}
            for _ in range(L):
                ndp = {}
                for state, cnt in dp.items():
                    for c in "abc":
                        nxt = ac.step(state, c)
                        if ac.end_count[nxt] == 0:
                            ndp[nxt] = ndp.get(nxt, 0) + cnt
                dp = ndp
            want = sum(
                1 for t in itertools.product("abc", repeat=L) if not any(p in "".join(t) for p in patterns)
            )
            self.assertEqual(sum(dp.values()), want)

    def test_random_matches_brute_force(self):
        rng = random.Random(0)
        for _ in range(300):
            patterns = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 6))]
            text = "".join(rng.choice("ab") for _ in range(rng.randint(0, 20)))
            ac = AhoCorasick(patterns)
            found = ac.find_all(text)
            self.assertEqual(sorted(found), sorted(brute_find_all(text, patterns)))
            counts = [sum(1 for i in range(len(text)) if text.startswith(p, i)) for p in patterns]
            self.assertEqual(ac.match_counts(text), counts)
            # 終わる位置の順に並んでいる
            ends = [s + len(patterns[pid]) - 1 for s, pid in found]
            self.assertEqual(ends, sorted(ends))

    def test_duplicate_patterns(self):
        ac = AhoCorasick(["a", "a", "aa"])
        self.assertEqual(ac.match_counts("aaa"), [3, 3, 2])
        self.assertEqual(len(ac.find_all("aaa")), 8)

    def test_end_count(self):
        ac = AhoCorasick(["a", "ba"])
        state = 0
        for c in "ba":
            state = ac.step(state, c)
        self.assertEqual(ac.end_count[state], 2)  # "ba" と "a" の両方がここで終わる


if __name__ == "__main__":
    unittest.main()
