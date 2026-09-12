"""lcs.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lcs import LCS


def brute_lcs(S, T):
    n, m = len(S), len(T)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if S[i - 1] == T[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


class TestLCS(unittest.TestCase):
    def test_example_from_docstring(self):
        self.assertEqual(LCS("AABBABCCCABC", "ABC"), 3)

    def test_identical_strings(self):
        self.assertEqual(LCS("abcde", "abcde"), 5)

    def test_no_common_subsequence(self):
        self.assertEqual(LCS("aaa", "bbb"), 0)

    def test_matches_brute_force_randomized(self):
        """独自DP実装(dp[i][j]+=方式)の誤り回帰テスト。標準的な動的計画法と突き合わせる"""
        random.seed(5)
        for _ in range(200):
            s = "".join(random.choice("ab") for _ in range(random.randint(0, 8)))
            t = "".join(random.choice("ab") for _ in range(random.randint(0, 8)))
            self.assertEqual(LCS(s, t), brute_lcs(s, t), (s, t))


if __name__ == "__main__":
    unittest.main()
