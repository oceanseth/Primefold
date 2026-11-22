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
exact rationals.  The eigenvector is found in floating point, rounded to
rationals, and the Rayleigh quotient is then recomputed exactly, so every
printed bound is a rigorous lower bound for M_k.

Usage:  python maynard_mk.py K D JS EPS [K D JS EPS ...]
        e.g.  105 11 2 0     54 12 2,4,6 0     50 12 2,4,6 1/25
"""
import sys
from fractions import Fraction
from itertools import product
from math import comb, factorial, prod

import mpmath as mp


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
            v = Fraction(factorial(A) * prod(factorial(x) for x in B) * self.G[B],
                         factorial(self.k + A + w))
            self.cache[key] = v
        return v


def matrices(k, D, js, eps=Fraction(0)):
    wt = lambda e: sum(j * x for j, x in zip(js, e))
    basis = [(a, b) for b in exps_up_to(js, D) for a in range(D - wt(b) + 1)]
    full = Simplex(js, k, 2 * D)
    less = Simplex(js, k - 1, 2 * D)
    n = len(basis)
    add = lambda u, v: tuple(x + y for x, y in zip(u, v))
    # With eps > 0 this is the Polymath8b quantity M_{k,eps} (their Theorem 3.12):
    # F lives on (1+eps)R_k, the basis uses (1+eps-P1)^a, and the outer integral
    # in J runs over (1-eps)R_{k-1} only.  eps = 0 gives M_k.
    def Ifull(A, B):
        return (1 + eps) ** (k + A + wt(B)) * full.integral(A, B)

    jcache = {}

    def Jless(A, B):
        v = jcache.get((A, B))
        if v is None:
            if eps == 0:
                v = less.integral(A, B)
            else:  # (1+eps-P1')^A = sum_i C(A,i) (2 eps)^(A-i) (1-eps-P1')^i
                v = sum(comb(A, i) * (2 * eps) ** (A - i)
                        * (1 - eps) ** (k - 1 + i + wt(B)) * less.integral(i, B)
                        for i in range(A + 1))
            jcache[(A, B)] = v
        return v

    I = [[Ifull(a + a2, add(b, b2)) for (a2, b2) in basis] for (a, b) in basis]

    # integral over t_k of (1-P1)^a prod P_j^{b_j}, in the (k-1)-variable basis:
    # P_j = P_j' + t^j, and int_0^u (u-t)^a t^s dt = a! s!/(a+s+1)! u^(a+s+1).
    def inner(a, b):
        out = []
        for i in product(*[range(x + 1) for x in b]):
            s = wt(i)
            c = Fraction(prod(comb(x, y) for x, y in zip(b, i)) * factorial(a) * factorial(s),
                         factorial(a + s + 1))
            out.append((c, a + s + 1, tuple(x - y for x, y in zip(b, i))))
        return out

    inn = [inner(a, b) for (a, b) in basis]
    J = [[Fraction(0)] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            v = sum(c1 * c2 * Jless(A1 + A2, add(B1, B2))
                    for (c1, A1, B1) in inn[i] for (c2, A2, B2) in inn[j])
            J[i][j] = J[j][i] = v
    return basis, I, J


def bound(k, D, js=(2,), eps=Fraction(0), dps=150):
    mp.mp.dps = dps
    basis, I, J = matrices(k, D, js, eps)
    n = len(basis)
    d = [mp.sqrt(mp.mpf(I[i][i].numerator) / I[i][i].denominator) for i in range(n)]
    toM = lambda M: mp.matrix([[mp.mpf(M[i][j].numerator) / M[i][j].denominator / (d[i] * d[j])
                                for j in range(n)] for i in range(n)])
    Im, Jm = toM(I), toM(J)
    L = mp.cholesky(Im)
    Li = mp.inverse(L)
    A = Li * Jm * Li.T
    A = (A + A.T) / 2
    # top eigenvector by power iteration (A is positive semidefinite)
    y = mp.matrix([1] * n)
    for _ in range(400):
        y = A * y
        y = y / mp.norm(y)
    y = Li.T * y
    x = [y[i] / d[i] for i in range(n)]
    scale = max(abs(v) for v in x)
    xr = [Fraction(int(mp.nint(v / scale * mp.mpf(10) ** 60)), 10 ** 60) for v in x]
    Jx = [sum(J[i][j] * xr[j] for j in range(n)) for i in range(n)]
    Ix = [sum(I[i][j] * xr[j] for j in range(n)) for i in range(n)]
    num = sum(xr[i] * Jx[i] for i in range(n))
    den = sum(xr[i] * Ix[i] for i in range(n))
    assert den > 0
    return k * num / den, n


if __name__ == "__main__":
    a = sys.argv[1:]
    for k, D, js, eps in zip(a[::4], a[1::4], a[2::4], a[3::4]):
        k, D, js, eps = int(k), int(D), tuple(int(x) for x in js.split(",")), Fraction(eps)
        m, n = bound(k, D, js, eps)
        print(f"k={k:4d}  eps={str(eps):>5}  degree<={D:2d}  power sums {js}  basis={n:4d}  "
              f"M >= {float(m):.7f}   (upper bound k/(k-1) log k = "
              f"{mp.nstr(mp.mpf(k) / (k - 1) * mp.log(k), 7)})", flush=True)
