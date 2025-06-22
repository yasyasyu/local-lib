def LCS(S, T):
    """Longest Common Sequence"""

    """print(LCS("AABBABCCCABC", "ABC"))"""

    dp = [[0] * len(S) for _ in range(len(T))]

    for i in range(len(S)):
        if i != 0:
            dp[0][i] = dp[0][i - 1]
        if S[i] == T[0]:
            dp[0][i] += 1

    for i in range(1, len(T)):
        for j in range(1, len(S)):
            dp[i][j] = dp[i][j - 1]
            if T[i] == S[j]:
                dp[i][j] += dp[i - 1][j - 1]
    print(*dp, sep="\n")

    return dp[-1][-1]
