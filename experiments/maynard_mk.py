"""Certified lower bounds for the Maynard sieve constant M_k.

M_k = sup_F  (sum_m J_k^(m)(F)) / I_k(F)  over square-integrable F supported on
the simplex R_k = {t_i >= 0, t_1 + ... + t_k <= 1}, where

    I_k(F)     = integral of F^2 over R_k
    J_k^(m)(F) = integral over the other k-1 variables of (integral of F dt_m)^2

(Maynard, "Small gaps between primes", Annals 2015, Prop. 4.2.)  If the primes
have level of distribution theta and M_k > 2/theta, then every admissible
k-tuple contains two primes infinitely often.  Bombieri-Vinogradov gives
theta = 1/2, so the unconditional requirement is M_k > 4.

F is restricted to the span of

    (1 - P1)^a * prod_{j in JS} P_j^{b_j},     a + sum_j j*b_j <= D,

where P_j = sum_i t_i^j is the j-th power sum.  JS = (2,) is Maynard's
original choice; a larger JS is the Polymath8b refinement.  All integrals are
exact rationals.  The eigenvector is found in ball arithmetic, rounded to
rationals, and the Rayleigh quotient is then recomputed exactly, so every
printed bound is a rigorous lower bound for M_k (printed rounded down).

Needs python-flint (pip install python-flint).

Usage:  python maynard_mk.py K D JS EPS [K D JS EPS ...]
        e.g.  105 11 2 0     54 12 2,4,6 0     50 12 2,4,6 1/25
"""
import sys
from fractions import Fraction
from itertools import product
from math import comb, factorial, log, prod

from flint import arb, arb_mat, ctx, fmpq, fmpq_mat, fmpz


def exps_up_to(js, W):
    """All exponent tuples n with sum_j j*n_j <= W."""
    out = [()]
    for j in js:
        out = [e + (n,) for e in out
               for n in range((W - sum(jj * x for jj, x in zip(js, e))) // j + 1)]
    return out


def series_power(js, k, W):
    """Coefficients of g(y)^k up to weight W, where
    g(y) = sum_n (sum_j j n_j)! / prod_j n_j!  *  y^n   (integer coefficients).
    g is what one variable t_i contributes to the integral of a monomial in the
    power sums over the simplex (Dirichlet's integral)."""
    wt = lambda e: sum(j * x for j, x in zip(js, e))
    base = {e: factorial(wt(e)) // prod(factorial(x) for x in e) for e in exps_up_to(js, W)}

    def mul(p, q):
        r = {}
        qs = sorted(q.items(), key=lambda t: wt(t[0]))
        qw = [wt(e) for e, _ in qs]
        for e1, c1 in p.items():
            room = W - wt(e1)
            for (e2, c2), w2 in zip(qs, qw):
                if w2 > room:
                    break
                e = tuple(x + y for x, y in zip(e1, e2))
                r[e] = r.get(e, 0) + c1 * c2
        return r

    result = {tuple(0 for _ in js): 1}
    e = k
    while e:
        if e & 1:
            result = mul(result, base)
        e >>= 1
        if e:
            base = mul(base, base)
    return result


class Simplex:
    """Exact integrals of (1-P1)^A * prod_j P_j^{B_j} over R_k."""

    def __init__(self, js, k, W):
        self.js, self.k = js, k
        self.G = series_power(js, k, W)
        self.cache = {}

    def integral(self, A, B):
        key = (A, B)
        v = self.cache.get(key)
        if v is None:
            w = sum(j * x for j, x in zip(self.js, B))
            v = fmpq(factorial(A) * prod(factorial(x) for x in B) * self.G[B],
                     factorial(self.k + A + w))
            self.cache[key] = v
        return v


def matrices(k, D, js, eps=Fraction(0)):
    """Exact Gram matrices I and J (fmpq_mat) for the basis described above.

    With eps > 0 this is the Polymath8b quantity M_{k,eps} (their Theorem 3.12):
    F lives on (1+eps)R_k, the basis uses (1+eps-P1)^a, and the outer integral
    in J runs over (1-eps)R_{k-1} only.  eps = 0 gives M_k."""
    eps = fmpq(eps.numerator, eps.denominator)
    wt = lambda e: sum(j * x for j, x in zip(js, e))
    add = lambda u, v: tuple(x + y for x, y in zip(u, v))
    basis = [(a, b) for b in exps_up_to(js, D) for a in range(D - wt(b) + 1)]
    n = len(basis)
    full = Simplex(js, k, 2 * D)
    less = Simplex(js, k - 1, 2 * D)

    icache = {}

    def Ifull(A, B):
        v = icache.get((A, B))
        if v is None:
            v = icache[(A, B)] = (1 + eps) ** (k + A + wt(B)) * full.integral(A, B)
        return v

    jcache = {}

    def Jless(A, B):
        v = jcache.get((A, B))
        if v is None:
            if eps == 0:
                v = less.integral(A, B)
            else:  # (1+eps-P1')^A = sum_i C(A,i) (2 eps)^(A-i) (1-eps-P1')^i
                v = fmpq(0)
                for i in range(A + 1):
                    v += (comb(A, i) * (2 * eps) ** (A - i)
                          * (1 - eps) ** (k - 1 + i + wt(B)) * less.integral(i, B))
            jcache[(A, B)] = v
        return v

    I = fmpq_mat(n, n, [Ifull(a + a2, add(b, b2)) for (a, b) in basis for (a2, b2) in basis])

    # T: integral over t_k of each basis element, in the (k-1)-variable basis.
    # P_j = P_j' + t^j, and int_0^u (u-t)^a t^s dt = a! s!/(a+s+1)! u^(a+s+1).
    ext = [(A, b) for b in exps_up_to(js, D) for A in range(1, D - wt(b) + 2)]
    pos = {e: i for i, e in enumerate(ext)}
    m = len(ext)
    T = fmpq_mat(n, m)
    for r, (a, b) in enumerate(basis):
        for i in product(*[range(x + 1) for x in b]):
            s = wt(i)
            c = fmpq(prod(comb(x, y) for x, y in zip(b, i)) * factorial(a) * factorial(s),
                     factorial(a + s + 1))
            T[r, pos[(a + s + 1, tuple(x - y for x, y in zip(b, i)))]] = c
    I2 = fmpq_mat(m, m, [Jless(A + A2, add(b, b2)) for (A, b) in ext for (A2, b2) in ext])
    J = T * I2 * T.transpose()
    return basis, I, J


def bound(k, D, js=(2,), eps=Fraction(0), prec=2000, squarings=12):
    """Return (certified lower bound as fmpq, basis size)."""
    basis, I, J = matrices(k, D, js, eps)
    n = len(basis)
    ctx.prec = prec
    A = arb_mat(I).solve(arb_mat(J))          # I^{-1} J, top eigenvector wanted
    for _ in range(squarings):
        A = A * A
        big = max(abs(A[i, 0]).mid() for i in range(n))
        A = A / big
    y = A * arb_mat(n, 1, [1] * n)
    scale = max(abs(y[i, 0]).mid() for i in range(n))
    x = fmpq_mat(n, 1, [fmpq(((y[i, 0] / scale).mid() * arb(2) ** 300).floor().unique_fmpz(),
                             fmpz(2) ** 300) for i in range(n)])
    num = (x.transpose() * J * x)[0, 0]
    den = (x.transpose() * I * x)[0, 0]
    assert den > 0
    return k * num / den, n


if __name__ == "__main__":
    a = sys.argv[1:]
    for k, D, js, eps in zip(a[::4], a[1::4], a[2::4], a[3::4]):
        k, D, js, eps = int(k), int(D), tuple(int(x) for x in js.split(",")), Fraction(eps)
        m, n = bound(k, D, js, eps)
        ub = k / (k - 1) * log(k)
        print(f"k={k:4d}  eps={str(eps):>5}  degree<={D:2d}  power sums {js}  basis={n:4d}  "
              f"M >= {float(m.p * 10**7 // m.q) / 1e7:.7f}   (upper bound k/(k-1) log k = "
              f"{ub:.6f})", flush=True)
