from typing import Callable


class Doubling:
    """ダブリング（写像の高速反復適用）

    使い方:
        N, K = map(int, input().split())
        mapping = list(map(lambda x: int(x) - 1, input().split()))

        doubling = Doubling(N, K, lambda x: mapping[x])
        doubling.get(x, k)  # xにmappingをk回適用した結果
    """

    def __init__(self, N: int, max_K: int, mapping: Callable[[int], int]) -> None:
        """要素数nのダブリングテーブルを作成します。"""
        k_bits = max_K.bit_length()

        # dub[i][j] = 値jを2**i回操作した結果
        self.doubling_table = [[0] * N for _ in range(k_bits)]

        # 1回(2**0回)操作した結果を作成
        for j in range(N):
            self.doubling_table[0][j] = mapping(j)

        # 2**i回操作した結果を順に作成
        # 2**(i-1)回操作を2回すれば2**i回操作したことになる
        for i in range(1, k_bits):
            for j in range(N):
                self.doubling_table[i][j] = self.doubling_table[i - 1][
                    self.doubling_table[i - 1][j]
                ]

    def get(self, x, k):
        """xをk回操作した値を取得します。"""
        # kをビットごとに分解して、2**a + 2**b + 2**c + ... の形で考える。
        # xを2**a回操作した結果を2**b回操作した結果を2**c回操作… のように順に適用する
        current = x
        for i in range(k.bit_length()):
            if k >> i & 1:
                current = self.doubling_table[i][current]

        return current
