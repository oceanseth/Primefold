"""Bilinear ("type II") statistics on the parity decoy.

`decoy_filter.py` splits the primes p in (x, 51x/50) into

    E = {p : Omega(p+2) even}   (contains no twin prime pair)
    O = {p : Omega(p+2) odd}    (contains every twin prime pair)

and finds that size and residue classes cannot tell E from O.  Sieve theory's
known way past this "parity barrier" is bilinear information: sums over
factorisations

    T(S; alpha, beta) = sum over p in S, over m | p+2 with M < m <= 2M,
                        of alpha(m) * beta((p+2)/m).

This script evaluates T on E and on O for several coefficient choices and
three ranges of m, and reports z = (T(E) - T(O)) / sqrt(sum of squares), i.e.
how many standard deviations apart the halves are compared with a random
split of the primes into two halves.

It also evaluates, on ALL the primes, the one bilinear sum a proof would need
to bound:  sum_p lambda(p+2) * #{m | p+2, M < m <= 2M}  (lambda = Liouville).

Usage:  python type2_filter.py [x]        (default x = 10**8)
"""
import sys
import numpy as np
from decoy_filter import sieve, big_omega, KAPPA, H

X = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0e8
rng = np.random.default_rng(20261121)


def main():
    x = X
    lo, hi = x, KAPPA * x
    P = sieve(lo, hi)
    base = int(lo) + 1
    om = big_omega(lo, hi + 4)
    A = P + H                                   # the shifted primes p + 2
    lamA = 1 - 2 * (om[A - base] % 2)           # lambda(p+2)
    inE = lamA == 1
    nE, nO = int(inE.sum()), int((~inE).sum())
    twins = int((om[A - base] == 1).sum())
    print(f"primes in ({lo:.0f}, {hi:.0f}): {len(P)};  E: {nE} (no twins);  O: {nO} ({twins} twin primes p)")

    # position of each shifted prime, for divisor enumeration
    span = int(np.ceil(hi)) + H + 2 - base
    pos = -np.ones(span, dtype=np.int64)
    pos[A - base] = np.arange(len(A))

    small = big_omega(0, int(hi) // 100 + 10)   # Omega(k) for k up to x/100, index k-1
    lam_small = 1 - 2 * (small % 2)

    def lam(k):
        return lam_small[np.asarray(k) - 1]

    def factor_pairs(M):
        """All (index of a in A, m, n) with a = m*n, M < m <= 2M."""
        ia, ms, ns = [], [], []
        for m in range(M + 1, 2 * M + 1):
            first = ((base + m - 1) // m) * m
            mult = np.arange(first, base + span, m)
            j = pos[mult - base]
            k = j >= 0
            if k.any():
                ia.append(j[k])
                ms.append(np.full(int(k.sum()), m, dtype=np.int64))
                ns.append(mult[k] // m)
        return np.concatenate(ia), np.concatenate(ms), np.concatenate(ns)

    def z_split(c):
        """c[a] = inner sum for each a.  Returns T(E), T(O) and the z-score of
        T(E) - T(O) against a random split."""
        tE, tO = c[inE].sum(), c[~inE].sum()
        return tE, tO, (tE - tO) / np.sqrt((c**2).sum())

    for M in (100, 1000, 10000):
        ia, ms, ns = factor_pairs(M)
        print(f"\nm in ({M}, {2 * M}], n = (p+2)/m about {x / (1.5 * M):.0f};  {len(ia)} factorisations")
        print(f"   {'coefficients alpha(m), beta(n)':40s} {'T(E)':>12s} {'T(O)':>12s} {'z':>9s}")

        def inner(w):
            return np.bincount(ia, weights=w, minlength=len(A))

        tau = inner(np.ones(len(ia)))
        rows = [
            ("1, 1   (divisor count; type I)", tau),
            ("lambda(m), 1   (type I, signed)", inner(lam(ms).astype(float))),
            ("1, lambda(n)", inner(lam(ns).astype(float))),
            ("lambda(m), lambda(n)   (parity-type)", inner((lam(ms) * lam(ns)).astype(float))),
        ]
        for name, c in rows:
            tE, tO, z = z_split(c)
            print(f"   {name:40s} {tE:12.0f} {tO:12.0f} {z:+9.2f}")
        zs = []
        for _ in range(20):
            al = rng.choice([-1.0, 1.0], size=2 * M + 1)
            be = rng.choice([-1.0, 1.0], size=int(ns.max()) + 1)
            zs.append(z_split(inner(al[ms] * be[ns]))[2])
        zs = np.array(zs)
        print(f"   {'random +-1, random +-1   (20 draws)':40s} {'':12s} {'':12s} "
              f"rms {np.sqrt((zs**2).mean()):.2f}, max {np.abs(zs).max():.2f}")

        # the sum a proof would have to bound, on all the primes
        s = (lamA * tau).sum()
        print(f"   on all primes: sum lambda(p+2) * tau_M(p+2) = {s:+.0f}; "
              f"sum tau_M = {tau.sum():.0f}; z = {s / np.sqrt((tau**2).sum()):+.2f}")


if __name__ == "__main__":
    main()
