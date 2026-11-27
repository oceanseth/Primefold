"""Do the zeta zeros show up in the twin primes?

Under RH the explicit formula says that the primes, weighted by log p, are
the smooth density 1 plus one oscillation per zeta zero rho = 1/2 + i*gamma:

    d psi(x) ~ (1 - sum_rho x^(rho-1)) dx
    =>  x^(-1/2) d psi(x) - x^(-1/2) dx  ~  - sum_gamma e^(i*gamma*t) dt,   t = log x.

So the Fourier transform in t = log x of "primes minus main term" has a line
of amplitude -1 at every zero ordinate.  This script measures the same thing
for prime PAIRS (p, p+d), d = 2 (twins), 4 (cousins), 6 (sexy), weighted by
log p * log(p+d), after subtracting the Hardy-Littlewood main term 2*C_d*x.

Heuristic prediction (Hardy-Littlewood circle method, major arcs, keeping the
cross term between the main term and the zeros):

    pairs minus main term  ~  -4*C_d * sum_gamma e^(i*gamma*t) + other terms

i.e. the pair remainder carries every zeta zero with amplitude 4*C_d relative
to the primes: 2.6406 for d = 2 and d = 4, 5.2813 for d = 6.

Control: random thinnings of the primes (keep p with probability 2*C2/log p,
weight log(p)^2).  They have the same density as the twins but only inherit
the primes' own oscillation once, so they should give 2*C2 = 1.3203.  Their
scatter is the error bar.

The scatter of pair counts is of size sqrt(x)*log(x), larger than the zero
terms (sqrt(x)), so each increment is weighted by 1/t^2 (inverse noise
variance) and the range starts at small x where the signal is cleanest.

Usage:  python twin_zeros.py [N]     (default N = 10**9)
"""
import sys
import numpy as np
from mpmath import zetazero

N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**9
C2 = 0.6601618158468695739          # twin prime constant
CD = {2: C2, 4: C2, 6: 2 * C2}      # Hardy-Littlewood constants C_d
X0 = 100                            # start of the analysed range
M = 1 << 18                         # bins, uniform in t = log x
NZ = 100                            # zeros used for the stacked amplitude
NCTL = 20                           # independent thinned controls
rng = np.random.default_rng(20261121)


def small_primes(n):
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.flatnonzero(s)


def primes_upto(n, seg=1 << 23):
    """Segmented sieve over odd numbers >= 3; yields arrays of primes."""
    base = small_primes(int(n**0.5) + 1)
    base = base[base > 2]
    lo = 3
    while lo <= n:
        hi = min(lo + 2 * seg, n + 1)
        size = (hi - lo + 1) // 2
        s = np.ones(size, dtype=bool)
        for p in base:
            if p * p >= hi:
                break
            start = max(p * p, ((lo + p - 1) // p) * p)
            if start % 2 == 0:
                start += p
            s[(start - lo) // 2::p] = False
        yield lo + 2 * np.flatnonzero(s).astype(np.int64)
        lo = hi if hi % 2 == 1 else hi + 1


t0, t1 = np.log(X0), np.log(N)
dt = (t1 - t0) / M
edges = t0 + dt * np.arange(M + 1)
tc = 0.5 * (edges[:-1] + edges[1:])            # bin centres


def binned(tp, w):
    idx = np.floor((tp - t0) / dt).astype(np.int64)
    ok = (idx >= 0) & (idx < M)
    return np.bincount(idx[ok], weights=w[ok], minlength=M)


# g[j] = sum over events in bin j of weight * p^(-1/2)
g_pr = np.zeros(M)
g_pair = {d: np.zeros(M) for d in CD}
g_ctl = np.zeros((NCTL, M))
count = {d: 0 for d in CD}
npr = 0
carry = np.array([], dtype=np.int64)

for chunk in primes_upto(N + 6):
    p = np.concatenate([carry, chunk])
    if len(p) < 3:
        carry = p
        continue
    carry = p[-2:]                 # the next two primes decide d = 2, 4, 6
    b, n1, n2 = p[:-2], p[1:-1], p[2:]
    keep = b <= N
    b, n1, n2 = b[keep], n1[keep], n2[keep]
    lp = np.log(b)
    tp = lp
    amp = np.exp(-0.5 * lp)
    g_pr += binned(tp, lp * amp)
    npr += len(b)
    for d in CD:
        hit = ((n1 - b) == d) | ((n2 - b) == d)
        count[d] += int(hit.sum())
        g_pair[d] += binned(tp[hit], (lp * np.log(b + float(d)) * amp)[hit])
    q = np.minimum(1.0, 2 * C2 / lp)
    w = lp * lp * amp
    for c in range(NCTL):
        sel = rng.random(len(b)) < q
        g_ctl[c] += binned(tp[sel], w[sel])
# (the last two primes below N+6 are left in `carry`; at most two events lost)

print(f"N = {N:.1e}: {npr} odd primes; pairs (p, p+d): "
      + ", ".join(f"d={d}: {count[d]}" for d in CD))

# main terms: density c in x  ->  c * integral of x^(-1/2) dx over each bin
main = 2.0 * (np.exp(0.5 * edges[1:]) - np.exp(0.5 * edges[:-1]))
r_pr = g_pr - main
r_pair = {d: g_pair[d] - 2 * CD[d] * main for d in CD}
r_ctl = g_ctl - 2 * C2 * main

# inverse-variance weight 1/t^2 with a smooth taper at both ends
u = (tc - t0) / (t1 - t0)
taper = np.sin(np.pi * np.clip(u / 0.1, 0, 0.5)) ** 2 * np.sin(np.pi * np.clip((1 - u) / 0.1, 0, 0.5)) ** 2
win = taper / tc**2
norm = (win * dt).sum()


NFFT = 1 << 23                      # zero-padded FFT: frequency step 2*pi/(NFFT*dt)
dg = 2 * np.pi / (NFFT * dt)


def amp_at(r, freqs):
    """Amplitude a such that r ~ a * e^(i*g*t) dt, for each frequency g
    (read off the nearest bin of a zero-padded FFT; step dg << window width)."""
    F = np.fft.rfft(r * win, NFFT)
    k = np.rint(np.asarray(freqs) / dg).astype(np.int64)
    return F[k] * np.exp(-1j * (k * dg) * tc[0]) / norm


gam = np.array([float(zetazero(k).imag) for k in range(1, NZ + 1)])
mid = 0.5 * (gam[:-1] + gam[1:])
mid = mid[np.diff(gam) > 2.0]          # between zeros, clear of both neighbours

print(f"\nStacked amplitude: mean over the first {NZ} zeros, and over {len(mid)} "
      f"frequencies midway between well-separated zeros")
print("                         at the zeros (re, im)      between zeros (re, im)   predicted at zeros")


def stacked(r):
    return amp_at(r, gam).mean(), amp_at(r, mid).mean()


def show(name, r, pred):
    z, m = stacked(r)
    print(f"  {name:22s} {z.real:+8.3f} {z.imag:+7.3f}        {m.real:+8.3f} {m.imag:+7.3f}        {pred:+.3f}")


show("primes", r_pr, -1.0)
for d in CD:
    show(f"pairs d={d}", r_pair[d], -4 * CD[d])
zc = np.array([stacked(r_ctl[c]) for c in range(NCTL)])
print(f"  {'thinned control (mean)':22s} {zc[:, 0].real.mean():+8.3f} {zc[:, 0].imag.mean():+7.3f}        "
      f"{zc[:, 1].real.mean():+8.3f} {zc[:, 1].imag.mean():+7.3f}        {-2 * C2:+.3f}")
print(f"  scatter of one control (sd)  re {zc[:, 0].real.std(ddof=1):.3f}  im {zc[:, 0].imag.std(ddof=1):.3f}"
      f"   |  re {zc[:, 1].real.std(ddof=1):.3f}  im {zc[:, 1].imag.std(ddof=1):.3f}")

# regression of each remainder's spectrum on the primes' spectrum, all frequencies
grid = np.arange(5.0, gam[-1] + 2.0, 0.1)
S_pr = amp_at(r_pr, grid)
den = (np.abs(S_pr) ** 2).sum()


def ratio(r):
    return (amp_at(r, grid) * np.conj(S_pr)).sum() / den


rc = np.array([ratio(r_ctl[c]) for c in range(NCTL)])
sd = rc.real.std(ddof=1)
print(f"\nRatio to the primes' spectrum (least squares over frequencies {grid[0]:.0f}..{grid[-1]:.0f}):")
print(f"  thinned controls: mean {rc.real.mean():+.3f} {rc.imag.mean():+.3f}i, "
      f"sd of one run {sd:.3f}   (predicted {2 * C2:.4f})")
for d in CD:
    r = ratio(r_pair[d])
    pred = 4 * CD[d]
    # pair noise scales with sqrt(density) relative to the control
    s = sd * np.sqrt(CD[d] / C2)
    print(f"  pairs d={d}: {r.real:+.3f} {r.imag:+.3f}i  +- {s:.3f}   "
          f"(predicted {pred:.4f}; inherited-only would be {2 * CD[d]:.4f})")
