def LCS(S, T):
    """Longest Common Subsequence

    >>> LCS("AABBABCCCABC", "ABC")
    3

    https://github.com/yasyasyu/local-lib/blob/master/lcs.py
    """
    n, m = len(S), len(T)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if S[i - 1] == T[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]
