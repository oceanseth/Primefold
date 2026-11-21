"""A filter for twin prime "positivity" arguments.

`lean/Primefold/PairIdentity.lean` proves: for a set S of integers in
(x, 51x/50) and positive coefficients a_n,

    J(S) := integral of F[rho](u) * |sum_{n in S} a_n n^(-2 pi i x u)|^2 du
          = sum over m, n in S of a_m a_n rho(x (log n - log m)),

and J(S) > 0 exactly when S contains two elements 2 apart.  The identity holds
for ANY set, so it gives a test: an argument that concludes J > 0 from some
information about the primes must not reach the same conclusion for a decoy
set that carries the same information and has no pairs 2 apart.

This script
  1. checks the identity numerically (integral against pair sum) at small x;
  2. builds the primes in (x, 51x/50) and several decoy sets;
  3. records, for each set, the information a typical argument uses: its size
     and its distribution over residue classes modulo small primes;
  4. runs two candidate "arguments" (prediction rules) on every set and marks
     each as PASS (never claims positivity for a pair-free set) or FAIL.

Usage:  python decoy_filter.py [x]        (default x = 10**8)
"""
import sys
import numpy as np

X = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0e8
KAPPA = 51 / 50
H = 2
R_BUMP = 0.2
SMALL = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
rng = np.random.default_rng(20261121)


def bump(v):
    """Smooth, even, positive on (-R_BUMP, R_BUMP), zero outside."""
    out = np.zeros_like(v, dtype=float)
    k = np.abs(v) < R_BUMP
    out[k] = np.exp(-1.0 / (1.0 - (v[k] / R_BUMP) ** 2))
    return out


def rho(v):
    """A test function for difference 2: a bump at 2 plus its reflection."""
    v = np.asarray(v, dtype=float)
    return bump(v - H) + bump(-v - H)


def pair_sum(S, x):
    """J(S) = sum_{m,n} a_m a_n rho(x (log n - log m)), a_n = log n / sqrt n.
    rho vanishes unless |x (log n - log m)| is within 0.2 of 2, which forces
    |n - m| <= 3 in this range, so only near neighbours are examined."""
    S = np.sort(np.asarray(S, dtype=np.int64))
    a = np.log(S) / np.sqrt(S)
    ln = np.log(S)
    total = 0.0
    for k in range(1, 4):                       # k-th neighbour in the sorted set
        if len(S) <= k:
            break
        close = (S[k:] - S[:-k]) <= 3
        v = x * (ln[k:] - ln[:-k])[close]
        total += 2.0 * np.sum((a[k:] * a[:-k])[close] * rho(v))   # (m, n) and (n, m)
    return total


def pair_integral(S, x, umax=40.0, du=5e-4):
    """The left side of the identity, by direct quadrature.  Only feasible for small x."""
    S = np.asarray(S, dtype=np.int64)
    a = np.log(S) / np.sqrt(S)
    lam = 2 * np.pi * x * np.log(S)
    u = np.arange(-umax, umax + du / 2, du)
    vv = np.linspace(-R_BUMP, R_BUMP, 4001)
    b = bump(vv)
    B = np.array([np.trapezoid(b * np.cos(2 * np.pi * uu * vv), vv) for uu in u])
    Frho = 2 * B * np.cos(2 * np.pi * H * u)    # Fourier transform of rho
    P = (a[None, :] * np.exp(-1j * np.outer(u, lam))).sum(axis=1)
    return np.trapezoid(Frho * np.abs(P) ** 2, u)


def sieve(lo, hi):
    """Primes in (lo, hi)."""
    lo, hi = int(lo) + 1, int(np.ceil(hi))
    n = int(hi**0.5) + 1
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    seg = np.ones(hi - lo, dtype=bool)
    for p in np.flatnonzero(s):
        start = max(p * p, ((lo + p - 1) // p) * p)
        seg[start - lo::p] = False
    return lo + np.flatnonzero(seg)


def big_omega(lo, hi):
    """Omega(n), the number of prime factors with multiplicity, for lo < n < hi."""
    lo, hi = int(lo) + 1, int(np.ceil(hi))
    n = int(hi**0.5) + 1
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    rem = np.arange(lo, hi, dtype=np.int64)
    om = np.zeros(hi - lo, dtype=np.int64)
    for p in np.flatnonzero(s):
        pk = int(p)
        while pk < hi:
            start = ((lo + pk - 1) // pk) * pk
            om[start - lo::pk] += 1
            rem[start - lo::pk] //= p
            pk *= int(p)
    om[rem > 1] += 1                           # one prime factor above sqrt(hi)
    return om


def count_pairs(S):
    S = np.asarray(S, dtype=np.int64)
    return int(np.isin(S + H, S).sum())


def remove_pairs(S, refill_from=None):
    """Delete one random member of every pair 2 apart; optionally refill to the
    original size from `refill_from` without creating new pairs."""
    S = set(int(v) for v in S)
    target = len(S)
    for n in sorted(S):
        if n in S and n + H in S:
            S.discard(n if rng.random() < 0.5 else n + H)
    if refill_from is not None:
        pool = rng.permutation(np.asarray(refill_from))
        for c in pool:
            if len(S) >= target:
                break
            c = int(c)
            if c not in S and c - H not in S and c + H not in S:
                S.add(c)
    return np.array(sorted(S), dtype=np.int64)


# --- information a typical argument uses -------------------------------------

def residue_fractions(S, q):
    return np.bincount(np.asarray(S) % q, minlength=q) / len(S)


def residue_zscore(S, moduli=None):
    """Largest deviation, in standard deviations, of the counts in the coprime
    residue classes modulo the given primes from an even split.  For a random
    set this is about 3 (about 4 for the long list); the primes score the same."""
    worst = 0.0
    for q in (moduli or SMALL):
        f = np.bincount(np.asarray(S) % q, minlength=q)[1:]
        e = len(S) / (q - 1)
        worst = max(worst, np.abs(f - e).max() / np.sqrt(e))
    return worst


def plus_minus_two_z(S):
    """Mean excess, in standard deviations, of the classes +2 and -2 modulo the
    small primes: the trace that naive pair removal leaves."""
    z = []
    for q in SMALL[1:]:                          # q = 3 is skipped: its classes +2 and -2 are all there is
        f = np.bincount(np.asarray(S) % q, minlength=q)
        e = len(S) / (q - 1)
        z += [(f[2] - e) / np.sqrt(e), (f[q - 2] - e) / np.sqrt(e)]
    return float(np.mean(z)) * np.sqrt(len(z))   # combined z-score


LARGE = [int(q) for q in sieve(47, 500)]


# --- candidate arguments: rules that predict the number of pairs --------------

def arg_density(S, M):
    """Uses only the size of S: pairs ~ |S|^2 / M (independent placement)."""
    return len(S) ** 2 / M


def arg_local(S, M):
    """Uses the size of S and its distribution modulo every prime up to 47
    (the Hardy-Littlewood / sieve / major-arc model):
        pairs ~ |S|^2 / M * prod_q  q * sum_r f_q(r) f_q(r + 2)."""
    pred = len(S) ** 2 / M
    for q in [2] + SMALL:
        f = residue_fractions(S, q)
        pred *= q * np.sum(f * np.roll(f, -H))
    return pred


ARGUMENTS = {"density only": arg_density, "density + residues mod q <= 47": arg_local}


def main():
    # 1. numerical check of the identity proved in Lean
    print("1. Identity check (integral vs pair sum), small x")
    for x in (3000.0, 5000.0, 10000.0):
        P = sieve(x, KAPPA * x)
        for name, S in (("primes", P), ("primes, pairs removed", remove_pairs(P))):
            lhs, rhs = pair_integral(S, x), pair_sum(S, x)
            print(f"   x={x:7.0f}  {name:22s} |S|={len(S):3d} pairs={count_pairs(S):2d}  "
                  f"integral={lhs:+.6e}  pair sum={rhs:+.6e}")

    # 2. the sets
    x = X
    lo, hi = x, KAPPA * x
    M = int(np.ceil(hi)) - int(lo) - 1
    P = sieve(lo, hi)
    ints = np.arange(int(lo) + 1, int(np.ceil(hi)))
    rough = ints[np.all([ints % q != 0 for q in [2] + SMALL], axis=0)]
    random_rough = np.sort(rng.choice(rough, size=len(P), replace=False))
    sets = {
        "primes": P,
        "random rough set (control)": random_rough,
        "primes = 1 mod 3": P[P % 3 == 1],
        "primes, one of each twin removed": remove_pairs(P),
        "random rough set, pair-free": remove_pairs(random_rough, refill_from=rough),
    }
    # the parity decoy: split the primes p by the parity of Omega(p + 2)
    om = big_omega(lo, hi + 4)
    om_next = om[(P + H) - (int(lo) + 1)]
    sets["primes p, Omega(p+2) even"] = P[om_next % 2 == 0]
    sets["primes p, Omega(p+2) odd"] = P[om_next % 2 == 1]

    print(f"\n2. Sets in ({lo:.0f}, {hi:.0f}); {M} integers, {len(rough)} of them with no prime factor <= 47")
    print("   residue z: worst class modulo primes <= 47 | modulo primes 53..499 | combined excess of classes +-2")
    print(f"   {'set':34s} {'size':>7s} {'residue z':>22s} {'pairs':>7s} {'J':>12s}"
          + "".join(f" {'pred: ' + k:>32s}" for k in ARGUMENTS))
    rows = {}
    for name, S in sets.items():
        preds = [f(S, M) for f in ARGUMENTS.values()]
        rows[name] = (count_pairs(S), preds)
        zs = f"{residue_zscore(S):6.2f} |{residue_zscore(S, LARGE):6.2f} |{plus_minus_two_z(S):+7.2f}"
        print(f"   {name:34s} {len(S):7d} {zs:>22s} {count_pairs(S):7d} {pair_sum(S, x):12.5e}"
              + "".join(f" {p:32.1f}" for p in preds))

    # 3. verdicts
    print("\n3. Verdicts: an argument FAILS if it predicts pairs for a set that has none")
    for i, k in enumerate(ARGUMENTS):
        bad = [n for n, (pairs, preds) in rows.items() if pairs == 0 and preds[i] >= 1]
        ok = rows["primes"][1][i] / rows["primes"][0]
        print(f"   {k:32s}: prediction/actual on the primes = {ok:.3f};  "
              + ("PASS" if not bad else "FAIL on: " + "; ".join(bad)))


if __name__ == "__main__":
    main()
