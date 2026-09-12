def cross(o, a, b):
    """ベクトルOA, OBの外積 (OA x OB) を返す。

    正: OからみてBがAより反時計回り側、負: 時計回り側、0: 一直線上。

    https://github.com/yasyasyu/local-lib/blob/master/geometry.py
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def ccw(a, b, c):
    """3点a, b, cの向きを判定する。1: 反時計回り, -1: 時計回り, 0: 一直線上。

    https://github.com/yasyasyu/local-lib/blob/master/geometry.py
    """
    val = cross(a, b, c)
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


def convex_hull(points):
    """点集合の凸包を、反時計回りの頂点列として返す（Andrewのモノトーンチェーン法）。
    convex_hull([(0, 0), (1, 1), (1, 0), (0, 1), (0.5, 0.5)])
    # -> [(0, 0), (1, 0), (1, 1), (0, 1)]（反時計回り、内部の点は除かれる）

    3点以上が一直線上に並ぶ辺は、両端点だけを残し中間の点は含めない。
    点が1個以下の場合はそのまま返す。

    https://github.com/yasyasyu/local-lib/blob/master/geometry.py
    """
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def on_segment(a, b, p):
    """点a, b, pが一直線上にある前提で、pが線分ab上（端点含む）にあるかを返す。

    https://github.com/yasyasyu/local-lib/blob/master/geometry.py
    """
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_intersect(p1, p2, p3, p4):
    """線分p1p2と線分p3p4が交差する（端点や一直線上での接触も含む）かを返す。
    segments_intersect((0, 0), (2, 2), (0, 2), (2, 0))  # True（交差する）

    https://github.com/yasyasyu/local-lib/blob/master/geometry.py
    """
    d1 = ccw(p3, p4, p1)
    d2 = ccw(p3, p4, p2)
    d3 = ccw(p1, p2, p3)
    d4 = ccw(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and (
        (d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)
    ):
        return True

    if d1 == 0 and on_segment(p3, p4, p1):
        return True
    if d2 == 0 and on_segment(p3, p4, p2):
        return True
    if d3 == 0 and on_segment(p1, p2, p3):
        return True
    if d4 == 0 and on_segment(p1, p2, p4):
        return True

    return False


def point_in_polygon(point, polygon):
    """点と多角形（頂点列、時計回り/反時計回りどちらでも可）の位置関係を判定する。
    point_in_polygon((1, 1), [(0, 0), (2, 0), (2, 2), (0, 2)])
    # 1: 内部, 0: 辺上, -1: 外部

    戻り値: 1 = 内部, 0 = 辺上（頂点含む）, -1 = 外部。

    https://github.com/yasyasyu/local-lib/blob/master/geometry.py
    """
    x, y = point
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]

        if ccw((x1, y1), (x2, y2), point) == 0 and on_segment((x1, y1), (x2, y2), point):
            return 0

        if (y1 > y) != (y2 > y):
            x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_intersect:
                inside = not inside

    return 1 if inside else -1
