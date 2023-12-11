def is_ok(mid):
    if mid > 0:
        return True
    else:
        return False


def binary_search(ng, ok):
    """
    (ng : ok)
    """
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if is_ok(mid):
            ok = mid
        else:
            ng = mid
    return ok
