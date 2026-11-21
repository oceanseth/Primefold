# Check of Lee, arXiv:2610.32672v2

S. Lee, *The Hardy–Littlewood asymptotic for prime pairs of fixed even
difference from a uniform zeta-ratios conjecture*, v2, 3 November 2026.
16 pages, single author, not peer reviewed. The paper's own declaration reads
"ChatGPT was used in generating proofs."

Read in full (HTML version) on 2026-11-21 by Claude Fable 5.2. This is one
reader's check, done in a few hours. It is not a referee report.

## Verdict

I found no error in the argument. Every algebraic identity I recomputed came
out as stated. What I could not check are the facts the paper imports from
other sources (listed at the end). The conclusion is conditional on
Hypothesis 2.1, which is an open conjecture.

## The argument, and what I verified

Notation: `η = 1/16`, `σ₀ = 9/16`, `T = 2πx`, `W` a smooth weight supported in
`(1, 1 + 1/(25h))`, `P_x(t) = Σ Λ(n) n^(−1/2−it) W(n/x)`.

| Step | Claim | Checked |
|---|---|---|
| Lemma 2.2 | The hypothesis forces a zero-free strip `35/64 ≤ Re s ≤ 37/64`, a bound on `ζ′/ζ` on `Re s = σ₀`, and `N(σ₀, T) ≪ T^(θ+ε)`. | Logic followed. The zero-free strip comes from "a zero would make the integral diverge", so the hypothesis is, by itself, stronger than it looks. `𝒴(α,η;η,η) = 1` is proved in Lean (`ratiosY_degenerate`). |
| Lemma 2.3 | Differentiating the ratios formula gives the mean of `ζ′/ζ(½+a+it) · ζ′/ζ(½+b−it)`: `U·D(z) + (2π)^z C(z) U^(1−z)/(1−z) + O(U^(θ+ε))`, `z = a+b`. | The Euler factor identity and the identification of the constant term with `Σ Λ(n)²/n^(1+z)` recomputed by hand: correct. The differentiated main terms themselves are quoted from Conrey–Snaith Theorem 2.5 and agree with my recollection of it; not re-derived. |
| Lemma 3.1 | For two nonnegative weights `g±`, `∫ g±(t/T)·abs(P_x)² dt = D_x ± T·J_W(x)`, where `J_W` is a sum over pairs `n, n+h` only. | Recomputed: the Fourier supports exclude every difference `j ≠ h` for `n ∈ (x, κ_h x)`. Correct. This identity is unconditional. |
| Lemma 4.1 | `P = Q + R − Z` (contour shift; `R` from the pole, `Z` from zeros right of `σ₀`). | Residues and signs recomputed: correct. |
| Prop. 4.2 | `∫ g(t/T)·abs(Q)² dt` = diagonal + a contour integral of `C(z)` + `O(x^(θ+1/8+ε))`. | Followed line by line, including the split at `U₀ = √x` that keeps the shifts inside the hypothesis's uniformity range. Exponents recomputed: correct. |
| Lemma 5.1 | `Σ 𝔖(k) k^(−z) = ζ(z) ζ(1+z) A(z)`. | Both Euler-factor identities recomputed, including `p = 2`: correct. |
| Lemma 5.2, Prop. 5.3 | The contour integral equals `± T 𝔖(h) K`. | Followed. The pole at `z = 1` is cancelled by `Φ(1) = g(0)/2 = 0`. Correct. |
| Lemma 6.1 | The cross term with `Z` is `≪ x^(1−Δ(θ)+ε)`. | Exponent arithmetic recomputed: `Δ(θ) = 7/16 − θ + θ/(3−θ)`, positive exactly for `θ < (39−√177)/32`. Correct. |
| Prop. 6.2 | Dropping the nonnegative term `g±·abs(R−Z)²` gives a lower bound for `+J_W` and for `−J_W`, hence an asymptotic. | Correct. This is the step that turns two one-sided inequalities into a two-sided result. |
| Lemma 7.1, Thm 1.1 | Unsmoothing; partial summation to `π_h(x)`. | Followed: correct. |
| Section 8 | Identities with Nyman–Beurling approximants. | Skimmed only. Not needed for twin primes. |

## Not checked

- Conrey–Snaith (2007), eq. (2.8), (2.10), (2.12): quoted, not re-derived from
  their paper.
- Titchmarsh, Theorems 9.2, 9.6(A), 9.19(B): standard, cited from memory.
- Uniformity claims of the form "polynomial growth, so the tails are
  negligible": plausible and standard, not written out.

## What the hypothesis really is

My assessment, not the paper's. The proof only uses Hypothesis 2.1 through
Lemma 2.3, i.e. through the mean of a product of two logarithmic derivatives
with shifts of real part `1/16` and imaginary parts up to `U^(ν/2)`, with a
power-saving error. Expanding `ζ′/ζ` into primes, that mean is a weighted sum
of `Λ(m)Λ(n)` over pairs with `m/n` close to 1. Uniformity in the *imaginary*
parts is what lets Lee's Fourier weights isolate one difference `h`.

So the hypothesis is not an independent fact about zeros from which prime
pairs follow as a surprise. It is the prime-pair conjecture, with a power
saving and uniformly over a range of differences, written in the language of
zeta. The paper is a correct-looking translation between two forms of the
same open problem. `experiments/ratios_test.py` shows the same thing
numerically: with real shifts the formula holds almost exactly, and all the
difficulty appears when the shifts acquire imaginary parts.

If the Riemann Hypothesis is granted, `Z = 0`, Lemmas 2.2 and 6.1 are not
needed, and any `θ < 7/8` suffices.
