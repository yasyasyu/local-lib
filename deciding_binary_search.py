def binary_search(ng, ok):
    """めぐる式二分探索のテンプレート。

    ng: is_ok が False になる値、ok: is_ok が True になる値(順は逆でもよい)。
    is_ok の中身は問題に応じて書き換えて使う。

    使い方:
        # is_okを書き換えた上で
        binary_search(-1, 10)  # is_ok(mid) = mid > 0 の場合、境界の1を返す

    https://github.com/yasyasyu/local-lib/blob/master/deciding_binary_search.py
    """

    def is_ok(mid):
        if mid > 0:
            return True
        else:
            return False

    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok
