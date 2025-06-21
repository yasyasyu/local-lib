from sorted_set import SortedSet


class Pairset:
    def __init__(self, N) -> None:
        # self.interval = SortedList()
        self.data = SortedSet()
        self.data.add((-(10**6), -(10**6)))
        self.data.add((10**6, 10**6))

    def contains(self, x):
        idx = self.data.index((x, 10**18)) - 1
        L_start, L_end = self.data[idx]
        return x < L_end

    def add(self, x):
        idx = self.data.index((x, 10**18)) - 1
        L_start, L_end = self.data[idx]
        R_start, R_end = self.data[idx + 1]
        if x < L_end:
            return False
        if L_end < x and x + 1 < R_start:
            self.data.add((x, x + 1))
        elif L_end == x and x + 1 < R_start:
            self.data.pop(idx)
            # self.interval.discard(L_end - L_start)
            self.data.add((L_start, x + 1))
        elif L_end < x and x + 1 == R_start:
            self.data.pop(idx + 1)
            # self.interval.discard(R_end - R_start)
            self.data.add((x, R_end))
        else:
            self.data.pop(idx + 1)
            self.data.pop(idx)
            # self.interval.discard(L_end - L_start)
            # self.interval.discard(R_end - R_start)

            self.data.add((L_start, R_end))
        l, r = self.expand(x)
        # self.interval.add(r - l)
        return True

    def mex(self, x):
        idx = self.data.index((x, 10**18)) - 1
        L_start, L_end = self.data[idx]
        if L_end <= x:
            return x
        else:
            return L_end

    def expand(self, x):
        idx = self.data.index((x, 10**18)) - 1
        L_start, L_end = self.data[idx]
        if L_end <= x:
            return x, x
        else:
            return L_start, L_end

    def remove(self, x):
        idx = self.data.index((x, 10**18)) - 1
        L_start, L_end = self.data[idx]
        if L_end <= x:
            return False
        self.data.pop(idx)
        # self.interval.discard(L_end - L_start)
        if L_start < x:
            self.data.add((L_start, x))
            # self.interval.add(x - L_start)
        if x + 1 < L_end:
            self.data.add((x + 1, L_end))
            # self.interval.add(L_end - x + 1)
        return True
