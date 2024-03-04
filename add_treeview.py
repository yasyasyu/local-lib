def add_tree_view(target_class):
    from math import log2

    bit_length = lambda x: int(log2(x))

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
