"""Numerical test of the "uniform two-over-two zeta-ratios formula".

S. Lee (arXiv:2610.32672v2, Hypothesis 2.1) shows that the Hardy-Littlewood
prime-pair asymptotic for every even gap -- hence infinitely many twin primes --
would follow from:

    I(U) := int_0^U  zeta(1/2+a+it) zeta(1/2+b-it)
                     ---------------------------------  dt
                     zeta(1/2+c+it) zeta(1/2+d-it)

          =  U * Y(a,b;c,d)  +  int_0^U (t/2pi)^(-a-b) Y(-b,-a;c,d) dt  +  O(U^(theta+eps))

uniformly for 3/64 <= Re a,b,c,d <= 5/64, |Im| <= U^nu, for some fixed
theta < (39 - sqrt(177))/32 = 0.8030..., where

    Y(a,b;c,d) = zeta(1+a+b) zeta(1+c+d) / (zeta(1+a+d) zeta(1+b+c)) * A(a,b;c,d)
    A(a,b;c,d) = prod_p (1 - p^(-1-c-d)) (1 - p^(-1-b-c) - p^(-1-a-d) + p^(-1-c-d))
                        / ((1 - p^(-1-b-c)) (1 - p^(-1-a-d)))

(the Conrey-Snaith ratios conjecture, restricted).

The factor (t/2pi)^(-a-b) is the leading approximation to chi(1/2+a+it) *
chi(1/2+b-it), chi(s) = zeta(s)/zeta(1-s).  With imaginary shifts the two differ
by a relative O(|Im|^2 / t), which integrates to about |Im|^2 log U.  That is
allowed by the hypothesis (it is below U^(1/2)), but it hides the real
remainder, so the remainder is reported both ways: "as stated" and with the
exact chi factors.  This script computes I(U)
for U up to UMAX, subtracts the two main terms, and measures the growth of the
remainder E(U).  It is evidence about the hypothesis, not a proof of it.

Usage:  python ratios_test.py [UMAX]      (default 10000)
"""
import sys
import numpy as np
import mpmath as mp

UMAX = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0e4
H = 0.02                      # step in t; integrand is analytic in a strip of width > 3/64
PAD = 8.0                     # room for imaginary shifts
SIG = np.array([3.0, 3.5, 4.0, 4.5, 5.0]) / 64      # real parts available
NEM = int(max(400, UMAX / 3))  # Euler-Maclaurin cut-off, about twice |t|/(2 pi)
KEM = 6
THETA_STAR = (39 - np.sqrt(177)) / 32

# shift sets (a, b, c, d): (index into SIG, imaginary part as a multiple of H)
SETS = {
    "real, spread":     ((0, 0.0), (2, 0.0), (4, 0.0), (1, 0.0)),
    "real, other":      ((4, 0.0), (3, 0.0), (0, 0.0), (2, 0.0)),
    "imaginary, small": ((0, 0.5), (2, -0.3), (4, 0.2), (1, 0.7)),
    "imaginary, large": ((1, 3.0), (3, -2.0), (0, 5.0), (4, -4.0)),
}


def zeta_grid(t):
    """zeta(1/2 + SIG[k] + i t[j]) by Euler-Maclaurin; shape (len(t), len(SIG))."""
    n = np.arange(1, NEM)
    logn = np.log(n)
    W = n[:, None] ** (-(0.5 + SIG))[None, :]           # (NEM-1, 5)
    out = np.empty((len(t), len(SIG)), dtype=complex)
    B = [mp.bernoulli(2 * k) / mp.factorial(2 * k) for k in range(1, KEM + 1)]
    B = [float(x) for x in B]
    lN = np.log(NEM)
    for i in range(0, len(t), 2000):
        tt = t[i:i + 2000]
        ph = np.exp(-1j * np.outer(tt, logn))
        S = ph @ W
        s = (0.5 + SIG)[None, :] + 1j * tt[:, None]
        Ns = np.exp(-s * lN)                             # N^(-s)
        tail = NEM * Ns / (s - 1) + 0.5 * Ns
        poch = s.copy()                                  # s (s+1) ... (s+2k-2)
        Npow = Ns / NEM                                  # N^(-s-2k+1)
        for k in range(1, KEM + 1):
            tail += B[k - 1] * poch * Npow
            poch = poch * (s + 2 * k - 1) * (s + 2 * k)
            Npow = Npow / NEM**2
        out[i:i + 2000] = S + tail
    return out


def chi_plus(shift, tt):
    """chi(1/2 + shift + i t) for an array of t."""
    from scipy.special import loggamma
    s = 0.5 + shift + 1j * tt
    out = np.empty(len(tt), dtype=complex)
    big = s.imag > 2.0
    z = np.pi * s[big] / 2
    logsin = -1j * z + np.log1p(-np.exp(2j * z)) + np.log(0.5j)
    out[big] = np.exp(s[big] * np.log(2) + (s[big] - 1) * np.log(np.pi) + logsin + loggamma(1 - s[big]))
    for i in np.flatnonzero(~big):
        w = mp.mpc(s[i])
        out[i] = complex(2**w * mp.pi**(w - 1) * mp.sin(mp.pi * w / 2) * mp.gamma(1 - w))
    return out


def primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.flatnonzero(s).astype(float)


LP = np.log(primes(10**7))


def A(a, b, c, d):
    x, y, z = np.exp(-(1 + c + d) * LP), np.exp(-(1 + b + c) * LP), np.exp(-(1 + a + d) * LP)
    return np.exp(np.sum(np.log((1 - x) * (1 - y - z + x) / ((1 - y) * (1 - z)))))


def Y(a, b, c, d):
    z = lambda w: complex(mp.zeta(w))
    return z(1 + a + b) * z(1 + c + d) / (z(1 + a + d) * z(1 + b + c)) * A(a, b, c, d)


t = np.arange(-PAD, UMAX + PAD + H / 2, H)
j0 = int(round(PAD / H))                 # index of t = 0
nU = int(round(UMAX / H))
Z = zeta_grid(t)

# accuracy check against mpmath
rng = np.random.default_rng(1)
worst = 0.0
for j in rng.integers(0, len(t), 12):
    for k in (0, 4):
        ref = complex(mp.zeta(mp.mpc(0.5 + SIG[k], t[j])))
        worst = max(worst, abs(Z[j, k] - ref) / abs(ref))
print(f"zeta on {len(t)} points, |t| <= {UMAX + PAD:.0f}; worst relative error vs mpmath at 24 spot checks: {worst:.1e}")
print(f"hypothesis needs remainder exponent theta < {THETA_STAR:.4f}; Conrey-Snaith predict 1/2\n")

Ugrid = t[j0:j0 + nU + 1]                # 0 .. UMAX
marks = [u for u in (UMAX / 2**k for k in range(6, -1, -1)) if u >= 100]



def col(spec, sign):
    k, m = spec                       # real part SIG[k], imaginary part m (rounded to the grid)
    off = int(round(m / H))
    if sign > 0:                      # zeta(1/2 + shift + it) = Z(t + Im)
        return Z[j0 + off: j0 + off + nU + 1, k]
    return np.conj(Z[j0 - off: j0 - off + nU + 1, k])   # zeta(1/2 + shift - it)


def remainder(sa, sb, sc, sd):
    a, b, c, d = (SIG[k] + 1j * round(m / H) * H for k, m in (sa, sb, sc, sd))
    f = col(sa, +1) * col(sb, -1) / (col(sc, +1) * col(sd, -1))
    I = np.concatenate([[0], np.cumsum(0.5 * (f[1:] + f[:-1]) * H)])
    Y1, Y2 = Y(a, b, c, d), Y(-b, -a, c, d)
    with np.errstate(divide="ignore", invalid="ignore"):
        swap = Y2 * (2 * np.pi) ** (a + b) * Ugrid ** (1 - a - b) / (1 - a - b)
    swap[0] = 0
    main1 = Y1 * Ugrid
    return (a, b, c, d), I, main1, swap, Y1, Y2


for name, (sa, sb, sc, sd) in SETS.items():
    (a, b, c, d), I, main1, swap, Y1, Y2 = remainder(sa, sb, sc, sd)
    E = I - main1 - swap
    # same with exact chi factors: chi(1/2+a+it) * chi(1/2+b-it)
    g = chi_plus(a, Ugrid) * np.conj(chi_plus(np.conj(b), Ugrid))
    g[~np.isfinite(g)] = 0
    swapx = Y2 * np.concatenate([[0], np.cumsum(0.5 * (g[1:] + g[:-1]) * H)])
    Ex = I - main1 - swapx
    print(f"== shifts: {name}:  a={a:.4f} b={b:.4f} c={c:.4f} d={d:.4f}")
    print(f"   Y(a,b;c,d) = {Y1:.6f}   Y(-b,-a;c,d) = {Y2:.6f}")
    print("        U        |I(U)|     |first term|   |swap term|   |E(U)|    max|E| on [U/2,U]   max|E|/sqrt(U)   |E| without swap   exact chi: |E|, max on [U/2,U]")
    xs, ys, yx = [], [], []
    for u in marks:
        j = int(round(u / H))
        blk = np.abs(E[j // 2: j + 1]).max()
        blkx = np.abs(Ex[j // 2: j + 1]).max()
        xs.append(np.log(u))
        ys.append(np.log(blk))
        yx.append(np.log(blkx))
        print(f"   {u:9.1f}  {abs(I[j]):10.3f}  {abs(main1[j]):10.3f}  {abs(swap[j]):12.3f}  {abs(E[j]):9.4f}"
              f"  {blk:12.4f}  {blk / np.sqrt(u):14.4f}  {abs(I[j] - main1[j]):14.3f}   {abs(Ex[j]):12.4f} {blkx:9.4f}")
    slope = np.polyfit(xs, ys, 1)[0]
    print(f"   fitted growth exponent of max|E|: {slope:+.3f} as stated, {np.polyfit(xs, yx, 1)[0]:+.3f} with exact chi   "
          f"(relative size of E at U={UMAX:.0f}: {np.abs(E[-1]) / abs(I[-1]):.1e})\n")

# Ensemble: random shift sets, distinct real parts from SIG, imaginary parts uniform in [-IMAX, IMAX].
# One remainder is a noisy walk, so two measures are reported:
#  - rms over the sets of max|E| on [U/2, U];
#  - the increment exponent theta of each set: mean |E(u+L) - E(u)|^2 over u in [UMAX/4, UMAX]
#    scales like L^(2 theta).  theta = 1/2 is a random walk (remainder ~ sqrt(U)), theta near 0
#    a bounded oscillation, theta = 1 a missing main term.  The hypothesis needs growth
#    slower than U^0.803.
LAGS = [L for L in (16.0 * 2**k for k in range(20)) if L <= UMAX / 8]


def increment_exponent(E):
    j4 = len(E) // 4
    S = []
    for L in LAGS:
        n = int(round(L / H))
        dE = E[j4 + n:] - E[j4:-n]
        S.append(np.mean(np.abs(dE) ** 2))
    return 0.5 * np.polyfit(np.log(LAGS), np.log(S), 1)[0]


for IMAX in (0.0, 1.0, 3.0):
    NSET = 12 if IMAX == 0 else 40
    rr = np.random.default_rng(int(100 * IMAX) + 7)
    idx = [int(round(u / H)) for u in marks]
    absE = np.empty((NSET, len(marks)))
    rel = np.empty(NSET)
    th = np.empty(NSET)
    for q in range(NSET):
        spec = [(int(k), float(rr.uniform(-IMAX, IMAX))) for k in rr.permutation(len(SIG))[:4]]   # distinct real parts
        _, I, main1, swap, _, _ = remainder(*spec)
        E = I - main1 - swap
        absE[q] = [np.abs(E[j // 2: j + 1]).max() for j in idx]
        rel[q] = absE[q, -1] / abs(I[-1])
        th[q] = increment_exponent(E)
    rms = np.sqrt((absE**2).mean(axis=0))
    slope = np.polyfit(np.log(marks), np.log(rms), 1)[0]
    half = len(marks) // 2
    slope_hi = np.polyfit(np.log(marks[half:]), np.log(rms[half:]), 1)[0]
    print(f"== ensemble of {NSET} random shift sets, |Im| <= {IMAX}")
    print("   U:                   " + "  ".join(f"{u:9.0f}" for u in marks))
    print("   rms max|E| [U/2,U]:  " + "  ".join(f"{x:9.3f}" for x in rms))
    print("   same / sqrt(U):      " + "  ".join(f"{x:9.4f}" for x in rms / np.sqrt(marks)))
    print(f"   increment exponent theta over lags {LAGS[0]:.0f}..{LAGS[-1]:.0f}: median {np.median(th):.3f}, "
          f"quartiles {np.percentile(th, 25):.3f}..{np.percentile(th, 75):.3f}, max {th.max():.3f}; "
          f"sets below {THETA_STAR:.3f}: {(th < THETA_STAR).sum()} of {NSET}")
    print(f"   exponent of the rms row: {slope:+.3f} over the whole range, {slope_hi:+.3f} over the upper half;"
          f"  median relative remainder at U={UMAX:.0f}: {np.median(rel):.1e}\n")
