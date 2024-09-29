def binary_search(ng, ok):
    """
    (ng : ok)
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
