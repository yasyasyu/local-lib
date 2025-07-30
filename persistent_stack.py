from typing import Generic, Optional, Iterable, TypeVar, Union

T = TypeVar("T")


class PersistentStack(Generic[T]):
    """
    永続スタック（Persistent Stack）を実装したクラス。

    スタックの各操作（push, pop）は新しいスタックを返し、元のスタックは変更されません。
    これにより、過去の状態を保持したまま操作を行うことができます。

    Attributes:
        value: スタックの先頭要素
        prv: 直前のスタック（前の状態）

    Methods:
        push(value): 新しい値を積んだ新しいスタックを返す
        pop(): 1つ前の状態のスタックを返す
        peek(): 先頭要素を返す（空ならNone）
        from_iterable(iterable): イテラブルからスタックを生成
        __iter__(): 下から上へスタックをイテレート
        __str__(): スタック内容を文字列で返す
        __repr__(): デバッグ用表現

    使い方例:
        >>> A = PersistentStack()
        >>> A = A.push(1)
        >>> A = A.push(2)
        >>> print(A)  # [1, 2]
        >>> A = A.pop()
        >>> print(A)  # [1]
        >>> print(A.peek())  # 1

    状態の保存・復元例:
        >>> from collections import defaultdict
        >>> notebook = defaultdict(lambda: PersistentStack())
        >>> A = PersistentStack()
        >>> A = A.push("a")
        >>> notebook["save1"] = A
        >>> A = A.push("b")
        >>> print(A)  # [a, b]
        >>> A = notebook["save1"]
        >>> print(A)  # [a]
    """

    def __init__(
        self,
        value: Optional[Union[T, Iterable[T]]] = None,
        prev: Optional["PersistentStack"] = None,
    ):
        """
        スタックの初期化。

        Args:
            value: スタックに積む値、またはイテラブル
            prev: 直前のスタック
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

    def push(self, value) -> "PersistentStack":
        """
        新しい値を積んだ新しいスタックを返します。

        Args:
            value: 積む値

        Returns:
            PersistentStack: 新しいスタック
        """
        return PersistentStack(value=value, prev=self)

    def pop(self) -> "PersistentStack":
        """
        1つ前の状態のスタックを返します。

        Returns:
            PersistentStack: 1つ前のスタック
        """
        return self.prv if self.prv else self

    def peek(self) -> Optional[T]:
        """
        先頭要素を返します。

        Returns:
            Optional[T]: 先頭要素（空ならNone）
        """
        return self.value

    @staticmethod
    def from_iterable(iterable: Iterable[T]) -> "PersistentStack":
        """
        イテラブルからスタックを生成します。

        Args:
            iterable: イテラブル

        Returns:
            PersistentStack: 生成されたスタック
        """
        cur = PersistentStack()
        for v in iterable:
            cur = cur.push(v)
        return cur

    def __repr__(self) -> str:
        """
        デバッグ用にクラス名付きでスタック内容を返します。

        Returns:
            str: スタックのデバッグ用表現
        """
        return f"PersistentStack({(self)})"

    def __iter__(self) -> T:
        """
        スタックを下から上へイテレートします。

        Yields:
            T: スタックの各要素
        """
        val = []
        cur = self
        while cur.value:
            val.append(cur.value)
            cur = cur.prv

        for v in val[::-1]:
            yield v

    def __str__(self) -> str:
        """
        スタック内容を文字列で返します。

        Returns:
            str: スタックの内容
        """
        return "[" + ", ".join(str(v) for v in self) + "]"
