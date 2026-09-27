from collections import defaultdict
import heapq


class DeletableHeap:
    """要素の削除が可能なヒープ（多重集合として扱える最小値取得ヒープ）

    使い方:
        h = DeletableHeap()
        h.push(3)
        h.push(1)
        h.get()          # 1 (最小値を参照)
        h.discard(1)     # 1を1個削除してTrueを返す
        h.pop()          # 最小値を削除して返す

    削除は遅延削除（ヒープ先頭に来た時点で捨てる）で実装している。以下のnは内部のヒープの大きさ。

    https://github.com/yasyasyu/local-lib/blob/master/deletable_heap.py
    """

    def __init__(self, is_unique=False):
        """空のヒープを作る。is_unique=Trueなら同じ値を重複して持たない。O(1)"""
        self.heap = []
        self.d = dict()
        self.size = 0
        self.total = 0
        self.is_unique = is_unique

    def __str__(self):
        """要素を並べた文字列を返す。O(n)"""
        result = []
        cnt = defaultdict(int)
        for a in self.heap:
            if not a in self.d.keys():
                continue

            if cnt[a] < self.d[a]:
                cnt[a] += 1
                result.append(str(a))

        return f"[{', '.join(result)}]"

    def push(self, x):
        """xを追加する。O(log n)"""
        if x not in self.d:
            self.d[x] = 1
        elif self.is_unique:
            return
        else:
            self.d[x] += 1

        self.size += 1
        self.total += x
        heapq.heappush(self.heap, x)

    def get(self):
        """最小値を返す（削除しない）。O(1)"""
        return self.heap[0]

    def pop(self):
        """最小値を削除して返す。ならしO(log n)"""
        n = self.get()
        self.discard(n)
        return n

    def discard(self, x):
        """xを1個削除する。xが無ければFalseを返す。ならしO(log n)"""
        if not self.is_exist(x):
            return False

        self.size -= 1
        self.total -= x
        self.d[x] -= 1
        if self.d[x] == 0:
            del self.d[x]

        while len(self.heap) != 0 and self.heap[0] not in self.d:
            heapq.heappop(self.heap)
        return True

    def erase(self, x, n=10**18):
        """xを最大n個削除し、削除した個数を返す。ならしO(log n)"""
        if not self.is_exist(x):
            return 0

        if self.d[x] < n:
            n = self.d[x]
        self.size -= n
        self.total -= x * n
        self.d[x] -= n
        if self.d[x] == 0:
            del self.d[x]

        while len(self.heap) != 0 and self.heap[0] not in self.d:
            heapq.heappop(self.heap)
        return n

    def is_exist(self, x):
        """xが含まれるかを返す。O(1)"""
        return x in self.d

    def __len__(self):
        """要素数（重複込み）を返す。O(1)"""
        return self.size

    def types(self):
        """値の種類数を返す。O(1)"""
        return len(self.d)

    def sum(self):
        """要素の総和を返す。O(1)"""
        return self.total

    def count(self, x):
        """xの個数を返す。O(1)"""
        return self.d[x] if self.is_exist(x) else 0
