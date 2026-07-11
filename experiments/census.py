#!/usr/bin/env python3
"""Census of twin pairs of Friedlander-Iwaniec form below 10^7.

Regenerates every figure quoted in paper/primefold-note.pdf:
  1. counts of FI primes (p = a^2 + b^4) and FI twins (p, p+2 both prime)
  2. the mod-8 split of both populations
  3. the x = a family decode: p = a^2 + 16, p+2 = a^2 + 2*3^2
  4. the quartic Pell check y^2 = 8c^4 + 1 (no solutions 1 < c <= 10^6)
  5. Hardy-Littlewood prediction for the family vs. actual count
  6. wrong-partner correlation controls on the bi-norm parameterizations

Runtime: ~2 minutes on a laptop. No dependencies beyond the stdlib.
"""
import math

N = 10**7
LIM = N + 2

# ---------------------------------------------------------------- sieve
comp = bytearray(LIM + 1)
comp[0] = comp[1] = 1
i = 2
while i * i <= LIM:
    if not comp[i]:
        comp[i*i::i] = b'\x01' * len(comp[i*i::i])
    i += 1
is_prime = lambda n: not comp[n]

# ------------------------------------------- FI primes and FI twins
reps = {}          # p -> (a, b) with smallest b
fi_all = set()
b = 1
while b**4 <= N - 1:
    b4 = b**4
    for a in range(1, int((N - b4)**0.5) + 1):
        v = a*a + b4
        if is_prime(v):
            fi_all.add(v)
            if is_prime(v + 2) and v not in reps:
                reps[v] = (a, b)
    b += 1
twins = sorted(reps)
print(f"FI primes p = a^2+b^4 <= {N:,}:            {len(fi_all):,}")
print(f"FI twins (p and p+2 prime):                {len(twins):,}")

m8_all = {1: 0, 5: 0}
for p in fi_all:
    if p > 2:
        m8_all[p % 8] += 1
m8_tw = {1: 0, 5: 0}
for p in twins:
    m8_tw[p % 8] += 1
print(f"FI primes mod 8   ->  1: {m8_all[1]:,}   5: {m8_all[5]:,}"
      f"   (ratio {m8_all[1]/m8_all[5]:.2f})")
print(f"FI twins  mod 8   ->  1: {m8_tw[1]:,}   5: {m8_tw[5]:,}"
      f"   (ratio {m8_tw[1]/m8_tw[5]:.2f})")

# ------------------------------------------------ the x = a family
# p = a^2+16, p+2 = a^2+18 = a^2 + 2*3^2, counted directly over a
family = [a for a in range(1, math.isqrt(N - 16) + 1)
          if is_prime(a*a + 16) and is_prime(a*a + 18)]
print(f"\nfamily a^2+16, a^2+18 both prime, a^2+16 <= {N:,}: {len(family)}")
print(f"first members a = {family[:8]}")

# quartic Pell: y^2 = 8c^4 + 1 -> only c = 1 (y = 3) below 10^6
pell_hits = [c for c in range(1, 10**6 + 1)
             if math.isqrt(8*c**4 + 1)**2 == 8*c**4 + 1]
print(f"solutions of y^2 = 8c^4+1 with 1 <= c <= 10^6: c = {pell_hits}")

# ------------------------------ Hardy-Littlewood prediction for family
def legendre(t, ell):
    t %= ell
    if t == 0:
        return 0
    return 1 if pow(t, (ell - 1)//2, ell) == 1 else -1

S = 2.0                                     # ell = 2 factor: (1-1/2)/(1-1/2)^2
ell = 3
while ell < 10**5:
    if is_prime(ell):
        if ell <= 19:                       # small primes: count directly
            omega = sum(1 for a in range(ell)
                        if (a*a + 16) % ell == 0 or (a*a + 18) % ell == 0)
        else:
            omega = (1 + legendre(-16, ell)) + (1 + legendre(-18, ell))
        S *= (1 - omega/ell) / (1 - 1/ell)**2
    ell += 2
A = math.isqrt(N - 16)
pred = S * sum(1 / (math.log(a*a + 16) * math.log(a*a + 18))
               for a in range(2, A + 1))
print(f"Hardy-Littlewood: singular series S = {S:.4f}, "
      f"predicted count = {pred:.1f}, actual = {len(family)}")

# ----------------------- bi-norm parameterizations and correlations
def sqrt_if_square(n):
    r = math.isqrt(n)
    return r if r*r == n else None

raw = []                                    # (p, a, b^2, x, y) for p = 1 mod 8
for p in twins:
    if p % 8 != 1:
        continue
    a, b = reps[p]
    q = p + 2
    for y in range(1, math.isqrt(q // 2) + 1):
        x = sqrt_if_square(q - 2*y*y)
        if x is not None:
            raw.append((p, a, b*b, x, y))
            break

def corr(u, v):
    n = len(u)
    mu, mv = sum(u)/n, sum(v)/n
    su = math.sqrt(sum((t - mu)**2 for t in u))
    sv = math.sqrt(sum((t - mv)**2 for t in v))
    return sum((u[i]-mu)*(v[i]-mv) for i in range(n)) / (su*sv)

n = len(raw)
sp  = [math.sqrt(p) for (p, *_) in raw]
an  = [raw[i][1]/sp[i] for i in range(n)]
b2n = [raw[i][2]/sp[i] for i in range(n)]
xn  = [raw[i][3]/sp[i] for i in range(n)]
yn  = [raw[i][4]/sp[i] for i in range(n)]
print(f"\nbi-norm pairs (p = 1 mod 8): {n}   null s.e. = {1/math.sqrt(n):.4f}")
print(f"true pairing:      corr(a~,x~) = {corr(an, xn):+.4f}"
      f"   corr(b2~,y~) = {corr(b2n, yn):+.4f}")
for shift in (1, 7, 50):
    xs = xn[shift:] + xn[:shift]
    ys = yn[shift:] + yn[:shift]
    print(f"shifted by {shift:3d}:    corr(a~,x~) = {corr(an, xs):+.4f}"
          f"   corr(b2~,y~) = {corr(b2n, ys):+.4f}")
idx = [i for i in range(n) if raw[i][2] != 4]
print(f"b = 2 family removed (n = {len(idx)}): "
      f"corr(a~,x~) = {corr([an[i] for i in idx], [xn[i] for i in idx]):+.4f}"
      f"   corr(b2~,y~) = {corr([b2n[i] for i in idx], [yn[i] for i in idx]):+.4f}")

xa = [r for r in raw if r[3] == r[1]]
print(f"pairs with x = a exactly: {len(xa)} "
      f"(all with b = 2, y = 3: {all(r[2] == 4 and r[4] == 3 for r in xa)})")
