"""
{0,1,2,...,n-1}の部分集合の部分集合(空集合除く)の列挙
1011だと1011, 1010, 1001, 1000, 0011 ,0010 ,0001

使い方:
    bit_partial_set(0b1011)  # 標準出力に列挙結果を表示する

https://github.com/yasyasyu/local-lib/blob/master/bit_partial_set.py
"""


def bit_partial_set(n):
    width = n.bit_length()
    k = n
    while k:
        print(bin(k)[2:].zfill(width), k)
        k = (k - 1) & n
