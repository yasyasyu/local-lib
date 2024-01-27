"""
{0,1,2,...,n-1}の部分集合の部分集合(空集合除く)の列挙
1011だと1011, 1010, 1001, 1000, 0011 ,0010 ,0001
"""
from math import log2


def bit_partial_set(k):
    n = k
    print(bin(k)[2:].zfill(int(log2(n)) + 1), k)
    while k:
        k = (k - 1) & n
        print(bin(k)[2:].zfill(int(log2(n)) + 1), k)
