from math import comb, factorial

# 조합 함수 정의
def nCr(n, r):
    return comb(n, r)

# 경우의 수 계산
ways_150_30 = (nCr(150, 30) * nCr(120, 30) * nCr(90, 30) * nCr(60, 30)) // factorial(5)
print(ways_150_30)