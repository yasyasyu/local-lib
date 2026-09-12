class Parser:
    """四則演算(+ - * /)と括弧を含む数式を評価するパーサー。

    使い方:
        Parser().expr("2+3*4")     # 14
        Parser().expr("(2+3)*4")   # 20
        Parser().expr("2(3+4)")    # 14（括弧の前の掛け算記号は省略可）

    https://github.com/yasyasyu/local-lib/blob/master/_parser.py
    """

    def __init__(self) -> None:
        self.i = 0
        return None
    
    def _count_up(self):
        self.i += 1
    
    def expr(self, s) -> int:
        """expr    = term, {("+", term) | ("-", term)}"""
        res = self.term(s)
        while self.i < len(s):
            if s[self.i] == '+':
                self._count_up()
                res += self.term(s)
                continue
            elif s[self.i] == '-':
                self._count_up()
                res -= self.term(s)
                continue
            return res
        return res
    
    def term(self, s):
        """term    = factor, {("*", factor) | ("/", factor) | ("(", factor)}"""
        res = self.factor(s)
        while self.i < len(s):
            if s[self.i] == '*':
                self._count_up()
                res *= self.factor(s)
                continue
            elif s[self.i] == '/':
                self._count_up()
                if res < 0:
                    res *= -1
                    res //= self.factor(s)
                    res *= -1
                else:
                    res //= self.factor(s)
                continue
            elif s[self.i] == '(' and str(res).isdigit():
                res *= self.factor(s)
                continue
            else:
                break
        return res
    
    def factor(self, s):
        """factor  = ("(", expr, ")") | number"""
        if s[self.i] == '(':
            self._count_up()
            res = self.expr(s)
            if s[self.i] == ')':
                self._count_up()
            return res
        return self.number(s)

    def number(self, s):
        """number  = 1つ以上の数字"""
        res = ''
        while self.i < len(s) and s[self.i].isdigit():
            res += s[self.i]
            self._count_up()

        return int(res)
