import random


class RollingHash:
    """ローリングハッシュ（部分文字列の一致判定・LCPを高速に求める）

    使い方:
        rh = RollingHash("abcabc")
        rh.get(0, 3)                  # "abc" のハッシュ値
        rh.get(0, 3) == rh.get(3, 6)  # True（どちらも"abc"）
        rh.lcp(0, 3)                  # 位置0と3から始まる最長共通接頭辞の長さ -> 3

    https://github.com/yasyasyu/local-lib/blob/master/rolling_hash.py
    """

    MOD = (1 << 61) - 1

    def __init__(self, s: str, base: int | None = None) -> None:
        n = len(s)
        if base is None:
            base = random.randint(37, self.MOD - 1)
        self.base = base
        self.n = n
        self.hash = [0] * (n + 1)
        self.pw = [1] * (n + 1)
        for i, c in enumerate(s):
            self.hash[i + 1] = (self.hash[i] * base + ord(c)) % self.MOD
            self.pw[i + 1] = self.pw[i] * base % self.MOD

    def get(self, l: int, r: int) -> int:
        """区間[l, r)のハッシュ値を返す。"""
        return (self.hash[r] - self.hash[l] * self.pw[r - l]) % self.MOD

    def lcp(self, a: int, b: int) -> int:
        """位置a, bからそれぞれ始まる最長共通接頭辞の長さを返す。"""
        length = min(self.n - a, self.n - b)
        ok, ng = 0, length + 1
        while ng - ok > 1:
            mid = (ok + ng) // 2
            if self.get(a, a + mid) == self.get(b, b + mid):
                ok = mid
            else:
                ng = mid
        return ok
