"""trie.pyのテストコード"""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from trie import BinaryTrie, Trie


class TestTrie(unittest.TestCase):
    def test_search_exact_match_only(self):
        trie = Trie()
        trie.insert("abc")
        trie.insert("abd")
        self.assertTrue(trie.search("abc"))
        self.assertTrue(trie.search("abd"))
        self.assertFalse(trie.search("ab"))
        self.assertFalse(trie.search("abcd"))

    def test_starts_with(self):
        trie = Trie()
        trie.insert("abc")
        self.assertTrue(trie.starts_with("a"))
        self.assertTrue(trie.starts_with("ab"))
        self.assertTrue(trie.starts_with("abc"))
        self.assertFalse(trie.starts_with("abcd"))
        self.assertFalse(trie.starts_with("x"))

    def test_count_prefix(self):
        trie = Trie()
        for w in ["abc", "abd", "abcd", "xyz"]:
            trie.insert(w)
        self.assertEqual(trie.count_prefix("ab"), 3)
        self.assertEqual(trie.count_prefix("abc"), 2)
        self.assertEqual(trie.count_prefix("xyz"), 1)
        self.assertEqual(trie.count_prefix("q"), 0)

    def test_empty_string(self):
        trie = Trie()
        trie.insert("")
        self.assertTrue(trie.search(""))
        self.assertEqual(trie.count_prefix(""), 1)

    def test_duplicate_insert(self):
        trie = Trie()
        trie.insert("abc")
        trie.insert("abc")
        self.assertEqual(trie.count_prefix("abc"), 2)
        self.assertTrue(trie.search("abc"))


class TestBinaryTrie(unittest.TestCase):
    def test_insert_and_contains(self):
        trie = BinaryTrie(bit_length=8)
        trie.insert(5)
        trie.insert(12)
        self.assertIn(5, trie)
        self.assertIn(12, trie)
        self.assertNotIn(7, trie)

    def test_len(self):
        trie = BinaryTrie(bit_length=8)
        self.assertEqual(len(trie), 0)
        trie.insert(1)
        trie.insert(1)
        trie.insert(2)
        self.assertEqual(len(trie), 3)

    def test_erase(self):
        trie = BinaryTrie(bit_length=8)
        trie.insert(5)
        trie.insert(5)
        trie.erase(5)
        self.assertIn(5, trie)
        self.assertEqual(len(trie), 1)
        trie.erase(5)
        self.assertNotIn(5, trie)
        self.assertEqual(len(trie), 0)

    def test_max_xor_and_min_xor_small_example(self):
        trie = BinaryTrie(bit_length=4)
        for v in [3, 9, 12]:
            trie.insert(v)
        # 5^3=6, 5^9=12, 5^12=9 -> max=12, min=6
        self.assertEqual(trie.max_xor(5), 12)
        self.assertEqual(trie.min_xor(5), 6)

    def test_empty_trie_returns_none(self):
        trie = BinaryTrie(bit_length=8)
        self.assertIsNone(trie.max_xor(3))
        self.assertIsNone(trie.min_xor(3))

    def test_matches_brute_force_randomized(self):
        random.seed(0)
        bit_length = 10
        limit = 1 << bit_length
        trie = BinaryTrie(bit_length=bit_length)
        multiset = []

        for _ in range(200):
            op = random.random()
            if op < 0.6 or not multiset:
                v = random.randint(0, limit - 1)
                trie.insert(v)
                multiset.append(v)
            else:
                v = random.choice(multiset)
                trie.erase(v)
                multiset.remove(v)

            self.assertEqual(len(trie), len(multiset))

            if multiset:
                x = random.randint(0, limit - 1)
                expected_max = max(x ^ y for y in multiset)
                expected_min = min(x ^ y for y in multiset)
                self.assertEqual(trie.max_xor(x), expected_max, (x, multiset))
                self.assertEqual(trie.min_xor(x), expected_min, (x, multiset))


if __name__ == "__main__":
    unittest.main()
