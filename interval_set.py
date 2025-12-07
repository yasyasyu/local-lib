from .sorted_multi_set import SortedMultiset


class IntervalSet:
    """区間の集合を管理するデータ構造"""

    def __init__(self) -> None:
        self.data = SortedMultiset()
        self.interval = SortedMultiset()
        self._INF = 10**18
        self.total_count = 0  # 追加された要素の総数
        self.data.add((-(self._INF), -(self._INF)))
        self.data.add((self._INF, self._INF))

    def __len__(self):
        return len(self.data) - 2

    def __str__(self):
        return str([(l, r) for l, r in self.data if -self._INF < r and l < self._INF])

    def _get_interval_index(self, x):
        """xを含むか、xより小さい最大の区間のインデックスを返す"""
        return self.data.index((x, self._INF)) - 1

    def _get_interval(self, x):
        """xを含むか、xより小さい最大の区間を返す"""
        idx = self._get_interval_index(x)
        return self.data[idx]

    def contains(self, x):
        """xが集合に含まれるかチェック"""
        _, end = self._get_interval(x)
        return x < end

    def add(self, x):
        """xを集合に追加。既に含まれる場合はFalseを返す"""
        idx = self._get_interval_index(x)
        left_start, left_end = self.data[idx]

        if x < left_end:
            return False

        right_start, right_end = self.data[idx + 1]

        # 左の区間と結合するか判定
        left_join = left_end == x
        if left_join:
            new_start = left_start
            self.data.pop(idx)
            self.interval.discard(left_end - left_start)
        else:
            new_start = x

        # 右の区間と結合するか判定
        right_join = x + 1 == right_start
        if right_join:
            r_idx = idx if left_join else idx + 1
            self.data.pop(r_idx)
            self.interval.discard(right_end - right_start)
            new_end = right_end
        else:
            new_end = x + 1

        self.data.add((new_start, new_end))
        self.interval.add(new_end - new_start)
        self.total_count += 1  # 要素数を増加
        return True

    def insert(self, left, right):
        """区間[left, right)を集合に追加"""
        if left >= right:
            return

        removed_count = 0  # 既存の要素数をカウント

        # 左端と重なる区間を探す
        idx = self._get_interval_index(left)
        if idx >= 0:
            start, end = self.data[idx]
            if end >= left:
                removed_count += end - start
                left = min(left, start)
                right = max(right, end)
                self.data.pop(idx)
                self.interval.discard(end - start)
            else:
                idx += 1
        else:
            idx = 0

        # 重なる区間をすべてマージ
        while idx < len(self.data):
            start, end = self.data[idx]
            if start > right:
                break
            removed_count += end - start
            right = max(right, end)
            self.data.pop(idx)
            self.interval.discard(end - start)

        self.data.add((left, right))
        self.interval.add(right - left)
        # 追加された新しい要素数 = (新しい区間の長さ) - (削除された要素数)
        self.total_count += (right - left) - removed_count

    def mex(self, x):
        """x以上で集合に含まれない最小の整数を返す"""
        start, end = self._get_interval(x)
        return end if x < end else x

    def expand(self, x):
        """xを含む区間を返す。含まれない場合は(x, x)を返す"""
        start, end = self._get_interval(x)
        return (start, end) if x < end else (x, x)

    def remove(self, x):
        """xを集合から削除。含まれない場合はFalseを返す"""
        idx = self._get_interval_index(x)
        start, end = self.data[idx]

        if end <= x:
            return False

        self.data.pop(idx)
        self.interval.discard(end - start)

        if start < x:
            self.data.add((start, x))
            self.interval.add(x - start)
        if x + 1 < end:
            self.data.add((x + 1, end))
            self.interval.add(end - (x + 1))

        self.total_count -= 1  # 要素数を減少
        return True

    def remove_interval(self, left, right):
        """区間[left, right)を集合から削除"""
        if left >= right:
            return

        removed_count = 0  # 削除される要素数をカウント

        # 左端と重なる区間を処理
        idx = self._get_interval_index(left)
        start, end = self.data[idx]

        if end > left:
            # left を含む区間が存在する
            self.data.pop(idx)
            self.interval.discard(end - start)
            # 削除される部分の長さを計算
            removed_count += min(end, right) - max(start, left)
            if start < left:
                self.data.add((start, left))
                self.interval.add(left - start)
                idx += 1  # 追加した左側の部分の次から処理
            if right < end:
                self.data.add((right, end))
                self.interval.add(end - right)
                self.total_count -= removed_count
                return
            # idx は削除後、次の区間を指す
        else:
            # left を含む区間が存在しない
            idx += 1

        # 完全に含まれる区間を削除
        while idx < len(self.data):
            start, end = self.data[idx]
            if start >= right:
                break
            self.data.pop(idx)
            self.interval.discard(end - start)
            # 削除される部分の長さを計算
            removed_count += min(end, right) - start
            if right < end:
                self.data.add((right, end))
                self.interval.add(end - right)
                break

        self.total_count -= removed_count
