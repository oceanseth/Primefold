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

## 6. The parity decoy, computed (2026-11-21)

Question from idea 5: can a pair-free set always hide the residue bias that
pair deletion leaves? **Yes**, and without any tuning. Split the primes
`p ∈ (10^8, 1.02·10^8)` by the parity of `Ω(p + 2)`:

| | size | worst residue class, q ≤ 47 | q = 53..499 | excess in classes ±2 | pairs 2 apart | local model predicts |
|---|---|---|---|---|---|---|
| `Ω(p+2)` even | 53988 | 2.67 σ | 3.57 σ | +0.05 σ | **0** | 1929 |
| `Ω(p+2)` odd | 54536 | 2.57 σ | 3.55 σ | −0.20 σ | **3873** | 1973 |

The even half cannot contain a twin pair (if `p + 2` is prime then `Ω(p+2) = 1`).
The two halves have the same size to within 1.7 σ and the same residue
statistics as a random set, yet one has no pairs and the other has twice the
predicted number.

Consequences for any proposed proof:

- It must use information that separates these two halves. Size, residues to
  moduli up to 499, and anything computed from them, do not.
- The information that does separate them is the parity of the number of
  prime factors of `p + 2`, i.e. the Liouville function on a shifted prime.
  A proof must therefore contain, somewhere, a statement that controls
  `∑ Λ(n) λ(n + 2)` or something equivalent. That sum being `o(x)` is a case of
  Chowla's conjecture and is open; the observed split 53988 / 54536 is
  consistent with it.
- This matches what the analytic side said (ideas 2 and 3): the missing input
  is a correlation statement, not a location statement about zeros.

Next concrete step, if we continue: extend the filter with bilinear
("type II") statistics, which are the known way around parity (Friedlander–
Iwaniec, and the `a² + b⁴` primes this repository started from), and see
whether they separate the two halves at this size.

## 7. Bilinear statistics do not get around parity for free (2026-11-21)

`experiments/type2_filter.py`. For the parity halves `E` (no twins) and `O`
of idea 6, sums of `α(m)β(n)` over factorisations `p + 2 = mn`:

- Divisor counts, signed type I sums and random ±1 weights do not separate
  the halves (all within 3 σ of a random split, at `M = 100, 1000, 10000`).
- `α = β = λ` separates them by 143 to 163 σ, trivially, because
  `λ(m)λ(n) = λ(p+2)`.
- `α = 1, β = λ` separates them at `M = 100` (32 σ) only because the mean of
  `λ(m)` over that short range is not zero; it is the same information.
- On all primes, `∑ λ(p+2)·τ_M(p+2)` is −392, −111, −192 out of about 49000:
  the cancellation a proof needs is there numerically. `O` contains 7704
  primes `p+2`, which have no divisors in range, and its composites make up
  the difference almost exactly.

What this means. "Use type II information" is not an idea by itself: the
bilinear sum that matters is a parity sum, and bounding it for the sequence
`p + 2` is the open problem again. Friedlander and Iwaniec could bound their
bilinear sums because `a² + b⁴` lives in the Gaussian integers, where the
sequence factorises. For twins that door is shut in a precise way, and this
repository already proves it: `IsFIPrime.add_two_not_sq_add_sq` says `p + 2`
is never a sum of two squares when `p` is an FI prime.

- Estimate: negative result, but a sharp one. A route to twin primes needs a
  sequence in which *both* `p` and `p + 2` sit inside some algebraic structure
  that makes a parity-type bilinear sum provable. No such structure is known.
- Worth recording: the three probes so far (zeta zeros, residue decoys,
  bilinear sums) each end at a correlation of `λ` or `Λ` with a shift of
  itself. That is the Chowla / Hardy–Littlewood family, and it is one problem
  seen from three sides.

## Open questions I would like answered

1. Is the statement in idea 2 known to be *equivalent* to a uniform
   Hardy–Littlewood conjecture, or only implied by one? If only implied, it
   could be genuinely weaker.
2. Does the lattice / slope-inequality machinery of the RH archive produce any
   inequality for `abs(P_x(t))²` against an oscillating weight? The reader's
   map mentions only one-sided bounds for sums over primes with positive
   weights.
