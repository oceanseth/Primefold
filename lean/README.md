# Primefold in Lean

A Lean 4 + Mathlib project that machine-checks the elementary propositions of
the Primefold note and states the open problems around them.

**It does not prove the twin prime conjecture, and it does not derive anything
about twin primes from the Riemann Hypothesis.** The section
[Why RH does not give twin primes](#why-rh-does-not-give-twin-primes) explains
why no such file exists here.

## What is proved

Everything below compiles with no `sorry`, no added axioms and no
`native_decide`; `#print axioms` reports only Lean's three standard axioms
(`propext`, `Classical.choice`, `Quot.sound`).

| Lean name | Note | Statement |
|---|---|---|
| `fi_mod_eight` | Prop. 1 | an odd `a² + b⁴` is 1 or 5 mod 8; it is 5 exactly when `a ≡ 2 (mod 4)` and `b` is odd |
| `IsFIPrime.mod_four` | Prop. 1 | an FI prime other than 2 is 1 mod 4 |
| `IsFIPrime.add_two_not_sq_add_sq` | Prop. 2(i) | `p + 2` is never a sum of two squares |
| `IsFIPrime.add_two_not_fi` | | the twin of an FI prime is never of FI form |
| `IsFIPrime.add_two_mod_eight` | Prop. 2(ii), (iii) | `p ≡ 1 → p + 2 ≡ 3`, `p ≡ 5 → p + 2 ≡ 7` (mod 8) |
| `IsFIPrime.four_dvd_sub` | FI gaps | two odd FI primes differ by a multiple of 4, so the minimum gap is at least 4 |
| `fold_reduction` | Prop. 3 | `b⁴ + 2 = 2y²` forces `b = 2c` and `y² = 8c⁴ + 1` |
| `twinPrime_of_fiTwin` | §1 | infinitely many FI twins would imply the twin prime conjecture |
| `fiTwin_of_foldSixteen`, `fiTwin_of_foldOne` | §4 | infinitude of either fold family would imply infinitely many FI twins |
| `GRHDirichlet.riemannZeta` | | the Dirichlet hypothesis contains the critical-strip statement for ζ |

The last three rows are implications **from open problems**. They show the FI
statements are at least as hard as twin primes, which is the note's own
conclusion: the fold transfers the difficulty, undiminished.

## The conditional chain to twin primes

    ratios formula  ⟶  Hardy–Littlewood asymptotic  ⟶  infinitely many twin primes

| Lean name | File | Status |
|---|---|---|
| `RatiosHypothesis θ ν` | `Ratios.lean` | **Open conjecture**, stated formally (Hypothesis 2.1 of Lee, arXiv:2610.32672v2) |
| `LeeTheorem θ ν` | `Ratios.lean` | The first arrow, as a named proposition. **Not proved here.** Our reading of the paper: [LEE-CHECK.md](LEE-CHECK.md) |
| `infinite_pairs_of_hardyLittlewood`, `twinPrime_of_hardyLittlewood` | `HardyLittlewood.lean` | The second arrow. **Proved.** |
| `twinPrime_of_ratios` | `Ratios.lean` | The chain, with `LeeTheorem`, `RatiosHypothesis` and `0 < twinConstant` as explicit hypotheses. **Proved** as an implication. |
| `ratiosY_degenerate` | `Ratios.lean` | `𝒴(α, η; η, η) = 1`, a check that the Euler product is transcribed correctly. **Proved.** |

This is not a proof of the twin prime conjecture and is not evidence for it.
The ratios formula is open, is not known to follow from the Riemann
Hypothesis, and is in effect the prime-pair conjecture restated in terms of
zeta (see LEE-CHECK.md). To do: prove `0 < twinConstant`; formalise the
paper's lemmas one at a time so that `LeeTheorem` becomes a theorem.

Ideas toward an unconditional proof are logged in [IDEAS.md](IDEAS.md).

## Twin primes as a positivity statement (unconditional)

`Primefold/PairIdentity.lean` proves, with no hypotheses, an exact
reformulation of the twin prime conjecture. Write

    P_x(u) = ∑ over primes x < p < 51x/50 of (log p / √p) · p^(−2πixu).

| Lean name | Statement | Status |
|---|---|---|
| `integral_fourier_mul_normSq` | `∫ 𝓕ψ(u) · abs(∑ aₙ e^(−iuλₙ))² du = ∑ₘ ∑ₙ aₘ aₙ ψ((λₙ − λₘ)/2π)` for continuous integrable `ψ` with integrable Fourier transform | **Proved** |
| `eq_add_of_window` | for integers `x < m < n < (1 + 1/(25h))·x`, if `x·(log n − log m)` is within `1/4` of `h` then `n = m + h` | **Proved** |
| `pairSum_pos_iff` | the pair sum is positive exactly when the set contains two elements differing by `h` | **Proved** |
| `exists_pairTest` | a suitable smooth test function `ρ` exists for every `h ≥ 1` | **Proved** |
| `twinPrime_iff_integral_pos`, `exists_twinPrime_iff_integral_pos` | the twin prime conjecture holds **if and only if** `∫ 𝓕ρ(u) · abs(P_x(u))² du > 0` for arbitrarily large `x` | **Proved** |

This is the mechanism of Lemma 3.1 of Lee's paper, simplified: sharp cut-offs
instead of smooth ones, a single test function supported near `±h` instead of
two nonnegative weights, and exact inequalities for the logarithm so that no
"for sufficiently large `x`" is needed.

It is a reformulation, not progress toward a proof. The right-hand side is a
weighted count of twin primes in `(x, 51x/50)`, so proving it positive is
exactly as hard as finding the twin primes.

## What is stated but not proved

`Primefold/Statements.lean` defines `TwinPrimeConjecture`, `FITwinConjecture`,
`FoldFamilySixteen` and `FoldFamilyOne`. All four are open. `Primefold/Zeta.lean`
defines `GRHDirichlet` as a hypothesis.

Parts of the note that are **not** formalised: the representations
`x² + 2y²` and `x² − 2y²` in Proposition 2, the uniqueness of `c = 1` for
`y² = 8c⁴ + 1` in Proposition 3, the Hardy–Littlewood predictions and every
computational count.

## The 2026-11-20 Riemann Hypothesis claim

On 2026-11-20 Levent Alpöge published a Lean archive claiming proofs of
Mathlib's `RiemannHypothesis` and of the corresponding statement for Dirichlet
L-functions. Status when this directory was written, the same day:

- no expert review of the mathematics; the independent kernel check
  (Comparator) had not finished;
- 175,187 Lean files, 17.4 million lines; a build is reported to need about
  100 GB of disk, hundreds of GB of RAM and 7 to 10 hours on 48 cores;
- published without a license.

Sources: the third-party mirror and its verification notes at
<https://github.com/Deicyde/riemann-hypothesis>, and
<https://lean4.dev/proofs/riemann-hypothesis-claim>. Neither was built or
checked here.

For those reasons the archive is neither vendored nor imported. This project
pins the same toolchain (Lean `v4.33.1`) and the same Mathlib revision
(`0df444a3`, tag `v4.33.1`), so a theorem written here against
`RiemannHypothesis` or `GRHDirichlet` can be discharged by the archive later
without porting, if the claim survives review.

## Why RH does not give twin primes

No implication from RH or GRH to the twin prime conjecture is known.

- GRH gives strong control of primes in arithmetic progressions for each
  modulus. On average over moduli, that level of control is already known
  unconditionally (Bombieri–Vinogradov), and it is the input to the
  bounded-gaps theorems.
- Even the far stronger Elliott–Halberstam conjecture, which GRH does not
  imply, yields only gaps of at most 12 (Maynard), or 6 under its generalised
  form (Polymath). Neither reaches 2.
- The obstruction is the parity barrier of sieve theory: sieve methods fed with
  distribution estimates cannot tell numbers with an even number of prime
  factors from those with an odd number. Knowing where the zeros lie does not
  remove it.

So a verified RH would be a landmark and would still leave twin primes open. A
Lean file here claiming otherwise would need a `sorry` standing in for an
unknown theorem, and this repository does not ship that.

## Build

```
cd lean
lake exe cache get    # prebuilt Mathlib, about 5 GB
lake build
```

Needs [elan](https://github.com/leanprover/elan). The first build takes a few
minutes after the cache download.
