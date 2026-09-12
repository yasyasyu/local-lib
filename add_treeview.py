def add_tree_view(target_class):
    """セグメント木のクラス(要素数を持つ self._size、内部配列を持つ self._d)にツリー状に整形した __str__ を追加するデコレータ。

    使い方:
        class Segtree:
            def __init__(self, n):
                self._size = n
                self._d = [0] * (2 * n)

        add_tree_view(Segtree)
        print(Segtree(4))  # ツリー状に整形されて表示される

    target_classを返すので、自分で定義するクラスには通常のデコレータ構文が使える:

        @add_tree_view
        class Segtree:
            def __init__(self, n):
                self._size = n
                self._d = [0] * (2 * n)

    ac-library-pythonの`atcoder.segtree.SegTree`・`atcoder.lazysegtree.LazySegTree`のように
    既に定義済みの外部クラスは、クラス定義文の直後にしか書けない`@`構文をその場で使えないため、
    代わりに関数として後付けする（戻り値を返すので代入形でも書ける）:

        from atcoder.segtree import SegTree
        add_tree_view(SegTree)  # SegTree自体が書き換わる
        # SegTree = add_tree_view(SegTree)  と書いても同じ
        seg = SegTree(op=lambda x, y: x + y, e=0, v=[1, 2, 3, 4, 5])
        print(seg)

    値の桁数（負号込み）はノードごとにバラバラでもよく、木全体で一番長い表示幅に自動的に揃える。

    https://github.com/yasyasyu/local-lib/blob/master/add_treeview.py
    """

    def format_level(values, group_size, cell, total_width, z):
        """1段分の行を組み立てる。

        group_size: この段の1ノードがまとめている葉の数
        cell: 葉1個分の表示幅（値の桁数z + 区切りの"|" 1文字）
        total_width: 木全体（葉の段）の行の文字数。全ての段でこの幅に揃える
        """
        row = [" "] * total_width
        for j in range(len(values) + 1):
            row[j * group_size * cell] = "|"

        region_len = group_size * cell - 1  # 両端の"|"を除いた、値を置ける幅
        for j, value in enumerate(values):
            s = str(value).zfill(z)
            start = j * group_size * cell + 1 + (region_len - z) // 2
            row[start : start + z] = list(s)

        return "".join(row)

    def view(self):
        n_leaves = self._size
        z = max((len(str(x)) for x in self._d[1 : n_leaves * 2]), default=1)
        cell = z + 1
        total_width = n_leaves * cell + 1

        ret = ""
        k = 1
        i = 1
        while i < n_leaves * 2:
            arr = self._d[i : i + k]
            ret += format_level(arr, n_leaves // k, cell, total_width, z) + "\n"
            i += k
            k *= 2

        return ret

    setattr(target_class, "__str__", view)
    return target_class
