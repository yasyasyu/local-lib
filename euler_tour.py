def euler_tour(G: list[list], root: int):
    """
    G:隣接リスト\\
    root:根\\
    euler tourしてleft idとright idと深さのlistを返す
    """
    N = len(G)
    v = root
    tour = [0] * (2 * N - 1)
    depth_list = []
    depth_v = [-1] * N
    left_id = [-1] * N
    right_id = [-1] * N
    it = [0] * N
    parents = [-1] * N
    visit_id = 0
    left_visit_id = 0
    depth = 0
    while v != -1:
        if left_id[v] == -1:
            left_id[v] = left_visit_id
            if len(depth_list) <= depth:
                depth_list.append([])
            depth_list[depth].append(v)
            depth_v[v] = depth
            left_visit_id += 1

        right_id[v] = left_visit_id
        tour[visit_id] = v
        visit_id += 1
        if it[v] == len(G[v]):
            v = parents[v]
            depth -= 1
            continue
        if G[v][it[v]] == parents[v]:
            it[v] += 1
            if it[v] == len(G[v]):
                v = parents[v]
                depth -= 1
                continue
            else:
                child = G[v][it[v]]
                parents[child] = v
                it[v] += 1
                v = child
                depth += 1
        else:
            child = G[v][it[v]]
            parents[child] = v
            it[v] += 1
            v = child
            depth += 1
    return left_id, right_id, depth_v
