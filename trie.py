class Trie:
    """文字列の集合を管理するTrie木（挿入・完全一致検索・前置一致個数）

    使い方:
        trie = Trie()
        trie.insert("abc")
        trie.insert("abd")
        trie.search("abc")       # True（完全一致で存在する）
        trie.search("ab")        # False（挿入されたのは"abc","abd"のみ）
        trie.starts_with("ab")   # True（"ab"を接頭辞に持つ単語がある）
        trie.count_prefix("ab")  # 2（"ab"を接頭辞に持つ単語の数）

    https://github.com/yasyasyu/local-lib/blob/master/trie.py
    """

    class _Node:
        __slots__ = ("children", "is_end", "count")

        def __init__(self):
            self.children = {}
            self.is_end = False
            self.count = 0  # このノードを通過する（接頭辞に持つ）単語の数

    def __init__(self) -> None:
        self.root = self._Node()

    def insert(self, s: str) -> None:
        """文字列sを挿入する。"""
        node = self.root
        node.count += 1
        for c in s:
            if c not in node.children:
                node.children[c] = self._Node()
            node = node.children[c]
            node.count += 1
        node.is_end = True

    def _find(self, s: str):
        node = self.root
        for c in s:
            if c not in node.children:
                return None
            node = node.children[c]
        return node

    def search(self, s: str) -> bool:
        """文字列sが完全一致で挿入済みかを返す。"""
        node = self._find(s)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """prefixを接頭辞に持つ単語が1つ以上挿入済みかを返す。"""
        return self._find(prefix) is not None

    def count_prefix(self, prefix: str) -> int:
        """prefixを接頭辞に持つ単語の個数を返す。"""
        node = self._find(prefix)
        return node.count if node else 0


class BinaryTrie:
    """非負整数の多重集合を管理し、XORに関するクエリを高速に処理するTrie木

    使い方:
        trie = BinaryTrie(bit_length=30)
        trie.insert(5)
        trie.insert(12)
        trie.max_xor(3)   # 集合内の要素yについて 3^y の最大値
        trie.min_xor(3)   # 同様に最小値
        3 in trie         # True（要素として含まれているか）
        len(trie)         # 現在の要素数（多重度込み）
        trie.erase(5)     # 挿入済みの値のみeraseできる（未挿入の値をeraseすると壊れる）

    https://github.com/yasyasyu/local-lib/blob/master/trie.py
    """

    def __init__(self, bit_length: int = 30) -> None:
        self.bit_length = bit_length
        self.children = [[-1, -1]]  # children[node] = [0側の子, 1側の子]
        self.count = [0]  # count[node] = このノードを通過する要素数

    def _new_node(self) -> int:
        self.children.append([-1, -1])
        self.count.append(0)
        return len(self.children) - 1

    def __len__(self) -> int:
        return self.count[0]

    def insert(self, x: int) -> None:
        """xを挿入する。"""
        node = 0
        self.count[node] += 1
        for i in range(self.bit_length - 1, -1, -1):
            b = (x >> i) & 1
            if self.children[node][b] == -1:
                self.children[node][b] = self._new_node()
            node = self.children[node][b]
            self.count[node] += 1

    def erase(self, x: int) -> None:
        """xを1つ削除する。xが挿入済みであることが前提（未挿入の値を渡すと状態が壊れる）。"""
        node = 0
        self.count[node] -= 1
        for i in range(self.bit_length - 1, -1, -1):
            b = (x >> i) & 1
            node = self.children[node][b]
            self.count[node] -= 1

    def __contains__(self, x: int) -> bool:
        node = 0
        for i in range(self.bit_length - 1, -1, -1):
            b = (x >> i) & 1
            nxt = self.children[node][b]
            if nxt == -1 or self.count[nxt] == 0:
                return False
            node = nxt
        return True

    def max_xor(self, x: int):
        """集合内の要素yについて x^y の最大値を返す。集合が空ならNone。"""
        if self.count[0] == 0:
            return None
        node = 0
        res = 0
        for i in range(self.bit_length - 1, -1, -1):
            b = (x >> i) & 1
            want = 1 - b
            nxt = self.children[node][want]
            if nxt != -1 and self.count[nxt] > 0:
                res |= 1 << i
                node = nxt
            else:
                node = self.children[node][b]
        return res

    def min_xor(self, x: int):
        """集合内の要素yについて x^y の最小値を返す。集合が空ならNone。"""
        if self.count[0] == 0:
            return None
        node = 0
        res = 0
        for i in range(self.bit_length - 1, -1, -1):
            b = (x >> i) & 1
            nxt = self.children[node][b]
            if nxt != -1 and self.count[nxt] > 0:
                node = nxt
            else:
                res |= 1 << i
                node = self.children[node][1 - b]
        return res
