def add_tree_view(target_class):
    """セグメント木風のクラス(要素数を持つ self._size、内部配列を持つ self._d)に
    ツリー状に整形した __str__ を追加するデコレータ。

    使い方:
        class Segtree:
            def __init__(self, n):
                self._size = n
                self._d = [0] * (2 * n)

        add_tree_view(Segtree)
        print(Segtree(4))  # ツリー状に整形されて表示される

    https://github.com/yasyasyu/local-lib/blob/master/add_treeview.py
    """
    bit_length = lambda x: x.bit_length() - 1

    def format_tree(arr, k, z):
        rank = bit_length(len(arr))
        max_rank = bit_length(k)
        edge_offset = ""
        for i in range(int(2 ** (max_rank - rank - 1))):
            if i == 0:
                edge_offset += "|" + " " * (z // 2)
            else:
                edge_offset += "|" + " " * z

        edge_offset += "|"
        middle_offset = ("|" + " " * z) * (2 * (max_rank - rank) - 1)
        middle_offset += "|"

        return (
            edge_offset
            + middle_offset.join(map(lambda x: str(x).zfill(z), arr))
            + edge_offset[::-1]
        )

    def view(self):
        k = 1
        i = 1

        ret = ""
        while i < self._size * 2:
            arr = self._d[i : i + k]
            ret += format_tree(arr, self._size, 3) + "\n"
            i += k
            k *= 2

        return ret

    setattr(target_class, "__str__", view)
