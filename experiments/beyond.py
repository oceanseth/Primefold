#!/usr/bin/env python3
"""Second-stage experiments: census to 10^9, complete fold classification,
and gaps between Friedlander-Iwaniec primes.

Regenerates every figure quoted in Sections 7-8 of the note:
  1. FI primes and FI twins to 10^9 (Miller-Rabin, deterministic below 3.2e9)
  2. complete pass-through fold classification: b^4 + s = m*y^2 for
     s <= 100, m in {1,2,3,7}, b <= 300
  3. the two shift-2 families (a^2+1, a^2+3) and (a^2+16, a^2+18) counted to
     10^9 against their Hardy-Littlewood predictions
  4. gap statistics between consecutive FI primes to 10^9: minimum gap,
     histogram of small gaps, count of consecutive pairs within 246

Runtime: ~2-5 minutes. Stdlib only.
"""
import math
from collections import Counter

N = 10**9

# --------------------------- deterministic Miller-Rabin for n < 3,215,031,751
SMALL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)

def is_prime(n):
    if n < 2:
        return False
    for p in SMALL:
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7):          # deterministic for n < 3,215,031,751
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

# ------------------------------------------------- FI primes to 10^9
fi = set()
b = 1
while b**4 < N:
    b4 = b**4
    amax = math.isqrt(N - 1 - b4)
    astart = 1 if b % 2 == 0 else 2      # opposite parity => odd value
    for a in range(astart, amax + 1, 2):
        v = a*a + b4
        if is_prime(v):
            fi.add(v)
    b += 1
fi_sorted = sorted(fi)
print(f"FI primes p = a^2+b^4 <= 10^9:  {len(fi_sorted):,}")

twins = [p for p in fi_sorted if is_prime(p + 2)]
print(f"FI twins (p, p+2 prime) <= 10^9: {len(twins):,}")
for cut in (10**7, 10**8):
    print(f"  ... of which <= {cut:.0e}: FI primes "
          f"{sum(1 for p in fi_sorted if p <= cut):,}, "
          f"twins {sum(1 for p in twins if p <= cut):,}")

# --------------------------- complete pass-through fold classification
# a^2+b^4 prime and a^2+b^4+s prime, with the shifted member equal to
# a^2 + m*y^2: requires b^4 + s = m*y^2.
print("\npass-through folds b^4 + s = m*y^2  (s <= 100 even, m in {1,2,3,7}, b <= 300):")
for s in range(2, 101, 2):
    for m in (1, 2, 3, 7):
        for bb in range(1, 301):
            t = bb**4 + s
            if t % m:
                continue
            y = math.isqrt(t // m)
            if m * y * y == t:
                print(f"  s={s:3d}  m={m}  b={bb:3d}  y={y:5d}   "
                      f"family: a^2+{bb**4}, a^2+{bb**4}+{s} = a^2+{m}*{y}^2")

# --------------------------------- the two shift-2 families, to 10^9
def singular_series(c1, c2, L=10**5):
    """Hardy-Littlewood singular series for a^2+c1, a^2+c2 simultaneously prime."""
    sieve = bytearray(L)
    sieve[0] = sieve[1] = 1
    i = 2
    while i * i < L:
        if not sieve[i]:
            sieve[i*i::i] = b'\x01' * len(sieve[i*i::i])
        i += 1
    S = 1.0
    for ell in range(2, L):
        if sieve[ell]:
            continue
        if ell <= 19:
            omega = sum(1 for a in range(ell)
                        if (a*a + c1) % ell == 0 or (a*a + c2) % ell == 0)
        else:
            omega = 0
            for t in (-c1, -c2):
                tm = t % ell
                if tm == 0:
                    omega += 1
                else:
                    omega += 1 + (1 if pow(tm, (ell-1)//2, ell) == 1 else -1)
        S *= (1 - omega/ell) / (1 - 1/ell)**2
    return S

for (c1, c2, name) in ((1, 3, "a^2+1, a^2+3"), (16, 18, "a^2+16, a^2+18")):
    A = math.isqrt(N - c1)
    actual = sum(1 for a in range(1, A + 1)
                 if is_prime(a*a + c1) and is_prime(a*a + c2))
    S = singular_series(c1, c2)
    pred = S * sum(1 / (math.log(a*a + c1) * math.log(a*a + c2))
                   for a in range(2, A + 1))
    print(f"\nfamily {name}, both prime, first <= 10^9:")
    print(f"  actual = {actual}   HL prediction = {pred:.1f}   (S = {S:.4f})")

# --------------------------------------- gaps between consecutive FI primes
gaps = Counter()
min_gap, min_at = 10**9, None
within246 = 0
for i in range(1, len(fi_sorted)):
    g = fi_sorted[i] - fi_sorted[i-1]
    if g <= 500:
        gaps[g] += 1
    if g <= 246:
        within246 += 1
    if g < min_gap:
        min_gap, min_at = g, fi_sorted[i-1]
print(f"\nconsecutive FI-prime pairs with gap <= 246, below 10^9: {within246:,}")
print(f"minimum gap: {min_gap} (first at p = {min_at:,})")
print("most common gaps <= 500:", gaps.most_common(10))
gap4 = [fi_sorted[i-1] for i in range(1, len(fi_sorted))
        if fi_sorted[i] - fi_sorted[i-1] == 4]
print(f"gap-4 pairs (p, p+4 both FI prime): {len(gap4):,}, "
      f"first: {[(p, p+4) for p in gap4[:5]]}")
# how does the within-246 count grow? cumulative at decades
for cut in (10**7, 10**8, 10**9):
    c = sum(1 for i in range(1, len(fi_sorted))
            if fi_sorted[i] <= cut and fi_sorted[i] - fi_sorted[i-1] <= 246)
    print(f"pairs with gap <= 246 below {cut:.0e}: {c:,}")
