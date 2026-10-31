from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class PersistentStack(Generic[T]):
    """
    永続スタック（Persistent Stack）を実装したクラス。

    スタックの各操作（push, pop）は新しいスタックを返し、元のスタックは変更されません。
    これにより、過去の状態を保持したまま操作を行うことができます。
    push / pop / peekはO(1)、要素を全て辿る__iter__ / __str__ / __repr__はO(N)。

    :var value: スタックの先頭要素
    :var prv: 直前のスタック（前の状態）

    メソッド:

    - ``push(value)``: 新しい値を積んだ新しいスタックを返す
    - ``pop()``: 1つ前の状態のスタックを返す
    - ``peek()``: 先頭要素を返す（空ならNone）
    - ``from_iterable(iterable)``: イテラブルからスタックを生成
    - ``__iter__()``: 下から上へスタックをイテレート
    - ``__str__()``: スタック内容を文字列で返す
    - ``__repr__()``: デバッグ用表現

    使い方例::

        >>> A = PersistentStack()
        >>> A = A.push(1)
        >>> A = A.push(2)
        >>> print(A)  # [1, 2]
        >>> A = A.pop()
        >>> print(A)  # [1]
        >>> print(A.peek())  # 1

    状態の保存・復元例::

        >>> from collections import defaultdict
        >>> notebook = defaultdict(lambda: PersistentStack())
        >>> A = PersistentStack()
        >>> A = A.push("a")
        >>> notebook["save1"] = A
        >>> A = A.push("b")
        >>> print(A)  # [a, b]
        >>> A = notebook["save1"]
        >>> print(A)  # [a]

    https://github.com/yasyasyu/local-lib/blob/master/persistent_stack.py
    """

    def __init__(
        self,
        value: T | Iterable[T] | None = None,
        prev: "PersistentStack[T] | None" = None,
    ) -> None:
        """
        スタックの初期化。O(1)（valueにイテラブルを渡した場合はO(N)）

        :param value: スタックに積む値、またはイテラブル
        :param prev: 直前のスタック
        """
        if (
            value is not None
            and isinstance(value, Iterable)
            and not isinstance(value, (str, bytes))
        ):
            s = PersistentStack.from_iterable(value)
            self.value = s.value
            self.prv = s.prv
        else:
            self.value = value
            self.prv = prev

    def push(self, value: T) -> "PersistentStack[T]":
        """
        新しい値を積んだ新しいスタックを返します。O(1)

        :param value: 積む値
        :return: 新しいスタック
        :rtype: PersistentStack[T]
        """
        return PersistentStack(value=value, prev=self)

    def pop(self) -> "PersistentStack":
        """
        1つ前の状態のスタックを返します。O(1)

        :return: 1つ前のスタック
        :rtype: PersistentStack
        """
        return self.prv if self.prv else self

    def peek(self) -> T | None:
        """
        先頭要素を返します。O(1)

        :return: 先頭要素（空ならNone）
        :rtype: T | None
        """
        return self.value

    @staticmethod
    def from_iterable(iterable: Iterable[T]) -> "PersistentStack":
        """
        イテラブルからスタックを生成します。O(N)

        :param iterable: イテラブル
        :return: 生成されたスタック
        :rtype: PersistentStack
        """
        cur = PersistentStack()
        for v in iterable:
            cur = cur.push(v)
        return cur

    def __repr__(self) -> str:
        """
        デバッグ用にクラス名付きでスタック内容を返します。O(N)

        :return: スタックのデバッグ用表現
        :rtype: str
        """
        return f"PersistentStack({(self)})"

    def __iter__(self) -> Iterator[T]:
        """
        スタックを下から上へイテレートします。O(N)

        :return: スタックの各要素を下から順に返すイテレータ
        :rtype: Iterator[T]
        """
        val = []
        cur = self
        while cur.value is not None:
            val.append(cur.value)
            cur = cur.prv

        for v in val[::-1]:
            yield v

    def __str__(self) -> str:
        """
        スタック内容を文字列で返します。O(N)

        :return: スタックの内容
        :rtype: str
        """
        return "[" + ", ".join(str(v) for v in self) + "]"
