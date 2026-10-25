def sort_by_cmp(a, cmp):
    """比較関数を渡せる安定ソート。ソート済みの新しいリストを返す（aは変更しない）。O(N log N) 回 cmp を呼ぶ

    cmp(x, y): x を y より前に置くとき負、後ろに置くとき正、どちらでもよいとき0を返す
        （functools.cmp_to_key と同じ約束。実際には cmp(x, y) < 0 かどうかだけを見る）。
    sorted(a, key=cmp_to_key(cmp)) と同じ結果になる。PyPyではこちらの方が数倍速い
    （CPythonでは cmp_to_key の方が速い）。

    使い方:
        # 分数 p[0]/p[1] の昇順（分母は正）。浮動小数点を使わずに比較する
        sort_by_cmp([(1, 2), (1, 3), (2, 3)], lambda p, q: p[0] * q[1] - q[0] * p[1])
        # [(1, 3), (1, 2), (2, 3)]

        # 連結したときに辞書順最小になる並べ方
        sort_by_cmp(["3", "30", "34"], lambda x, y: (x + y > y + x) - (x + y < y + x))
        # ["30", "3", "34"]

    https://github.com/yasyasyu/local-lib/blob/master/cmp_sort.py
    """
    # 再帰版のマージソート
    #     def sort(lo, hi):
    #         if hi - lo <= 1: return
    #         mid = (lo + hi) // 2
    #         sort(lo, mid); sort(mid, hi)
    #         merge(lo, mid, hi)
    # は、再帰の一番深いところ（長さ1の区間）から順にマージしていく。
    # ここでは再帰を使わずに、同じことを下から（ボトムアップに）行う。
    #     長さ1の区間を2つずつマージ → 長さ2のソート済み区間ができる
    #     長さ2の区間を2つずつマージ → 長さ4のソート済み区間ができる
    #     ...（width を倍にしていき、width >= n で全体がソート済み）

    def merge(src, dst, lo, mid, hi):
        """ソート済みの src[lo:mid] と src[mid:hi] をマージして dst[lo:hi] に書き込む"""
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            # 右が左より真に前に来るときだけ右を取る（等しいときは左 → 安定）
            if cmp(src[j], src[i]) < 0:
                dst[k] = src[j]
                j += 1
            else:
                dst[k] = src[i]
                i += 1
            k += 1
        # どちらかが尽きたら、残りをそのまま写す
        while i < mid:
            dst[k] = src[i]
            i += 1
            k += 1
        while j < hi:
            dst[k] = src[j]
            j += 1
            k += 1

    n = len(a)
    src = list(a)  # 長さ width ごとの区間がそれぞれソート済みの配列
    dst = [None] * n  # マージ結果の書き込み先（作業用の配列）
    width = 1
    while width < n:
        # 隣り合う2区間 [lo, mid) と [mid, hi) をマージする（末尾の区間は短いことがある）
        for lo in range(0, n, 2 * width):
            mid = min(lo + width, n)
            hi = min(lo + 2 * width, n)
            merge(src, dst, lo, mid, hi)
        # 長さ 2 * width ごとにソート済みになった dst を、次の段の入力にする
        # （毎回新しい配列を作らず、2つの配列を入れ替えて使い回す）
        src, dst = dst, src
        width *= 2
    return src
