# Ideas log: routes to an actual twin prime proof

A running file. Each entry says what the idea is, what it would need, and my
honest estimate of whether it gets past the known obstruction. Nothing here is
a proof. Newest entries last.

The obstruction every idea has to answer is the **parity barrier**: methods
that only see how primes are distributed in arithmetic progressions cannot
tell numbers with an even number of prime factors from those with an odd
number, and so cannot give a positive lower bound for prime pairs.

## 1. Twin primes as a one-sided positivity statement (2026-11-21)

Lee's Lemma 3.1 is unconditional and exact. With
`P_x(t) = Σ_p log p · p^(−1/2−it) W(p/x)`, a smooth weight `W ≥ 0` supported in
`(1, κ)`, and `ℓ` the explicit real Schwartz function of the paper, for all
sufficiently large `x`,

    ∫ ℓ(t/T)² cos(2π h t/T) · abs(P_x(t))² dt  =  T · J_W(x),      T = 2πx,

where `J_W(x) ≥ 0` is a weighted count of primes `p ∈ (x, κx)` with `p + h`
prime. Therefore:

> There are infinitely many twin primes **if and only if** the left side is
> strictly positive for arbitrarily large `x` (with `h = 2`).

No asymptotic is needed, only a sign. The quantity is a quadratic form in a
Dirichlet polynomial, tested against a cosine at the scale `t ≈ x`.

- Why it is interesting: the claimed RH proof is, per the third-party reader's
  map, a positivity argument (a geometric one-sided inequality fed into
  Landau's theorem). This is the form of the twin prime problem closest in
  shape to that.
- Why it is not yet progress: the trivial bound is `abs(T·J_W) ≤ D_x`, the
  diagonal, which is the sieve upper bound up to a constant and a logarithm.
  A lower bound needs `abs(P_x)²` to correlate with the cosine. Replace `Λ` by
  `Λ·λ` (Liouville) and every distributional input stays the same while the
  sign of the correlation flips. Any argument has to use something that
  distinguishes the two. That is the parity barrier in this language.
- Lean: **done 2026-11-21.** `Primefold/PairIdentity.lean` proves the
  equivalence outright (`exists_twinPrime_iff_integral_pos`), in a simpler form
  than the paper's: sharp cut-off to primes in `(x, 51x/50)`, one test function
  `ρ` supported near `±2`, no "sufficiently large `x`".

## 2. The minimal analytic target, assuming RH (2026-11-21)

If RH holds, Lee's argument needs only this (his Lemma 2.3), for some
`θ < 7/8` and some `ν > 0`:

    ∫₀ᵁ ζ′/ζ(9/16 + i(t+u)) · ζ′/ζ(9/16 − i(t−v)) dt
        = U·D(z) + (2π)^z C(z) U^(1−z)/(1−z) + O(U^θ),   z = 1/8 + i(u+v),

uniformly for `abs(u), abs(v) ≤ U^(ν/2)`. This is strictly less than the full
ratios hypothesis: no ratios, one line, logarithmic derivatives only. It
should be the statement we formalise as the hypothesis of the chain, replacing
`RatiosHypothesis`, once Lemma 2.3 is in Lean.

- Estimate: still equivalent in strength to prime pairs with a power saving
  (see `LEE-CHECK.md`). Smaller target, same wall.

## 3. What RH buys and what it does not (2026-11-21)

Under RH, `ζ′/ζ(σ + it)` for `σ > 1/2` is a sum over zeros, so the integral in
idea 2 becomes a double sum over pairs of zeros `γ, γ′` of a kernel in
`γ − γ′`. The diagonal `γ = γ′` gives terms of the type `U·D(z)`. The second
main term, the one that carries `𝔖(h)`, comes entirely from correlations
between *different* zeros at spacing about `1/log`. RH fixes the real parts
and says nothing about those correlations.

- A proof would have to establish the pair correlation of zeros including its
  arithmetic lower-order terms (Bogomolny–Keating). Montgomery proved the
  smooth part for restricted test functions under RH; the restriction is
  exactly the range where prime pairs do not enter.
- Estimate: this is the real frontier. No idea here yet.

## 4. Numerical observations worth keeping (2026-11-21)

- `experiments/twin_zeros.py`: prime-pair remainders carry each zeta zero with
  amplitude about `4·C_d` relative to the primes, twice what inheritance alone
  gives. Measured 10–30 % low with a consistent phase lag. Unexplained.
- `experiments/ratios_test.py`: the ratios formula has a bounded remainder
  (about 0.2 at height 20000) for real shifts, and a random-walk remainder
  with increment exponent 0.35–0.46 once shifts have imaginary parts. The
  remainder is largest when the two denominator zetas are evaluated at the
  same height (`Im(γ+δ) ≈ 0`) and the numerators are offset from them: every
  zero then produces a spike of height about `1/(Re γ · Re δ)`.
- Next experiment suggested by idea 2: test the logarithmic-derivative mean
  directly, with imaginary shifts growing like a power of `U`, which is the
  uniformity the proof actually uses and which is untested.

## 5. What the formalised criterion says, and a test any proof must pass (2026-11-21)

With `ρ` a bump at `2` plus its reflection, `𝓕ρ(u) = 2·B(u)·cos(4πu)` where `B`
is the Fourier transform of the centred bump. So the criterion reads

    ∫ B(u) cos(4πu) · abs(P_x(u))² du > 0   for arbitrarily large x.

In words: the Dirichlet polynomial over the primes just above `x` must be, on
average, larger near half-integer multiples of the scaled time than between
them. A twin pair `p, p+2` contributes two terms whose phases realign at
exactly those times.

The same identity holds for any coefficients, so it gives a clean test for a
proposed argument. Run it with the primes replaced by

- the integers in `(x, 51x/50)` with an **odd** number of prime factors on one
  side and an **even** number on the other (no "twins" by construction in the
  sense the argument needs), or
- a random set of the same density with pairs at distance 2 removed.

If the argument still "proves" positivity for those inputs, it is wrong. An
argument that survives must use a property of the primes that these decoys do
not share. This is the parity barrier as an executable check, and it is worth
building as `experiments/` code before trusting any positivity idea.

- Estimate: no route to positivity yet. The value of this entry is the
  filter, which is cheap and kills most wrong ideas quickly.
- **Built 2026-11-21:** `experiments/decoy_filter.py`. First result: the
  Hardy–Littlewood local model (size plus residues modulo primes up to 47)
  predicts 7805 pairs for the primes in (10^8, 1.02·10^8), where there are
  7704, and predicts 6292 and 7227 pairs for two decoys that have none. The
  decoys carry a residue bias of 5 to 6 standard deviations in the classes
  `±2`, which is the trace pair-removal must leave; a sharper decoy would
  spread that bias below detection, and whether that is always possible is a
  precise form of the parity question.

## Open questions I would like answered

1. Is the statement in idea 2 known to be *equivalent* to a uniform
   Hardy–Littlewood conjecture, or only implied by one? If only implied, it
   could be genuinely weaker.
2. Does the lattice / slope-inequality machinery of the RH archive produce any
   inequality for `abs(P_x(t))²` against an oscillating weight? The reader's
   map mentions only one-sided bounds for sums over primes with positive
   weights.
