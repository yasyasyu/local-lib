from typing import Sequence


class AhoCorasick:
    """Aho-Corasick 法。複数のパターンを、テキストの中から同時に探す。構築 O(パターンの長さの合計)

    状態は Trie の頂点番号（根が 0）。テキストを1文字ずつ step で進めると、
    今の状態は「テキストのここまでの接尾辞のうち、どれかのパターンの接頭辞である最長のもの」になる。
    パターンを含まない文字列を数える DP などでは、状態を DP の添字に使う（end_count を参照）。

    使い方:
        ac = AhoCorasick(["he", "she", "his", "hers"])
        ac.match_counts("ushers")   # [1, 1, 0, 1]（パターンごとの出現回数）
        ac.find_all("ushers")       # [(1, 1), (2, 0), (2, 3)]（(開始位置, パターン番号)）

        # パターンを1つも含まない長さ L の文字列の個数（文字は "abc"）
        dp = {0: 1}
        for _ in range(L):
            ndp = {}
            for state, cnt in dp.items():
                for c in "abc":
                    nxt = ac.step(state, c)
                    if ac.end_count[nxt] == 0:
                        ndp[nxt] = ndp.get(nxt, 0) + cnt
            dp = ndp
        sum(dp.values())

    https://github.com/yasyasyu/local-lib/blob/master/aho_corasick.py
    """

    def __init__(self, patterns: Sequence[str]) -> None:
        """パターンのリスト（どれも空でないこと）から構築する。O(パターンの長さの合計)"""
        self.lengths = [len(p) for p in patterns]
        self.children: list[dict[str, int]] = [{}]
        self.ends: list[list[int]] = [[]]  # ends[v]: v でちょうど終わるパターンの番号
        self.terminal: list[int] = []  # terminal[i]: パターン i が終わる頂点
        for i, pat in enumerate(patterns):
            v = 0
            for c in pat:
                nxt = self.children[v].get(c)
                if nxt is None:
                    nxt = len(self.children)
                    self.children[v][c] = nxt
                    self.children.append({})
                    self.ends.append([])
                v = nxt
            self.ends[v].append(i)
            self.terminal.append(v)

        size = len(self.children)
        # fail[v]: v が表す文字列の真の接尾辞のうち、Trie にある最長のもの
        self.fail = [0] * size
        # dict_link[v]: fail をたどった先で、最初にパターンが終わる頂点（無ければ -1）
        self.dict_link = [-1] * size
        # end_count[v]: v の状態で終わるパターンの個数（fail をたどった先の分も含む）
        self.end_count = [0] * size
        self.order = [0]  # BFS 順
        for v in self.order:
            self.end_count[v] = len(self.ends[v]) + (self.end_count[self.fail[v]] if v else 0)
            for c, u in self.children[v].items():
                if v == 0:
                    f = 0
                else:
                    f = self.step(self.fail[v], c)
                self.fail[u] = f
                self.dict_link[u] = f if self.ends[f] else self.dict_link[f]
                self.order.append(u)

    def step(self, state: int, c: str) -> int:
        """状態 state から文字 c を読んだ次の状態を返す。ならし O(1)（1回だけなら O(パターンの長さ)）"""
        children = self.children
        fail = self.fail
        while state and c not in children[state]:
            state = fail[state]
        return children[state].get(c, 0)

    def match_counts(self, text: str) -> list[int]:
        """パターンごとに、text の中での出現回数（重なりも含む）を返す。O(|text| + パターンの長さの合計)"""
        visit = [0] * len(self.children)
        state = 0
        for c in text:
            state = self.step(state, c)
            visit[state] += 1
        # 頂点 v を訪れたら、fail をたどった先の頂点が表す文字列も、そこで現れている
        for v in reversed(self.order):
            if v:
                visit[self.fail[v]] += visit[v]
        return [visit[t] for t in self.terminal]

    def find_all(self, text: str) -> list[tuple[int, int]]:
        """text の中のすべての出現を (開始位置, パターン番号) のリストで返す。O(|text| + 出現の個数)

        終わる位置の順に並ぶ。出現の個数が非常に多くなりうるときは match_counts を使う。
        """
        res = []
        state = 0
        for i, c in enumerate(text):
            state = self.step(state, c)
            v = state if self.ends[state] else self.dict_link[state]
            while v != -1:
                for pid in self.ends[v]:
                    res.append((i - self.lengths[pid] + 1, pid))
                v = self.dict_link[v]
        return res
