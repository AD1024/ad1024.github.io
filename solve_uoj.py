n, k = input().split()
n = int(n)
k = int(k)

a = list(map(int, input().split()))

from functools import lru_cache

@lru_cache
def query_max(l, r):
    if l == r:
        return a[l]
    mid = (l + r) // 2
    return max(query_max(l, mid), query_max(mid + 1, r))

for m in range(1, n + 1):
    b = a[:m]
    i = 0