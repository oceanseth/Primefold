import Primefold.HardyLittlewood

/-!
# The two-over-two zeta-ratios formula, and the conditional chain to twin primes

S. Lee, *The Hardy–Littlewood asymptotic for prime pairs of fixed even
difference from a uniform zeta-ratios conjecture*, arXiv:2610.32672v2
(3 November 2026; not peer reviewed), derives the Hardy–Littlewood asymptotic
for every even difference from a restricted form of the Conrey–Snaith ratios
conjecture ("Hypothesis 2.1" there).

This file

* states Hypothesis 2.1 formally (`RatiosHypothesis`);
* states the singular series `𝔖(h)`;
* names the content of Lee's Theorem 1.1 as a proposition (`LeeTheorem`) —
  it is **not** proved here and is **not** an axiom: every theorem that uses
  it takes it as an explicit hypothesis;
* proves that the twin prime constant is positive (`twinConstant_pos`);
* proves the chain `LeeTheorem → RatiosHypothesis → TwinPrimeConjecture`.

Nothing in this file is evidence for the twin prime conjecture.
`RatiosHypothesis` is open, and is not known to follow from the Riemann
Hypothesis.

## Faithfulness notes

* The paper fills removable singularities "by continuation".  The only ones
  that occur are the factors `1 / ζ(1)`; `invZeta` sets them to `0`.
* The paper's Lemma 2.2 argues that a zero of `ζ` in the shift strip would make
  the integral infinite, contradicting the hypothesis.  Lean's integral of a
  non-integrable function is `0`, so integrability of the integrand is made an
  explicit part of `RatiosHypothesis`.
-/

open Filter Topology Complex MeasureTheory

namespace Primefold

/-- `1 / ζ(s)`, with the removable singularity at `s = 1` filled by `0`. -/
noncomputable def invZeta (s : ℂ) : ℂ := if s = 1 then 0 else (riemannZeta s)⁻¹

/-- The local factor at `p` of the Euler product `𝒜(α, β; γ, δ)`
(Lee (2.1), Conrey–Snaith (2.10)). -/
noncomputable def eulerAFactor (α β γ δ : ℂ) (p : ℕ) : ℂ :=
  ((1 - (p : ℂ) ^ (-1 - γ - δ)) *
      (1 - (p : ℂ) ^ (-1 - β - γ) - (p : ℂ) ^ (-1 - α - δ) + (p : ℂ) ^ (-1 - γ - δ))) /
    ((1 - (p : ℂ) ^ (-1 - β - γ)) * (1 - (p : ℂ) ^ (-1 - α - δ)))

/-- The Euler product `𝒜(α, β; γ, δ)`. -/
noncomputable def eulerA (α β γ δ : ℂ) : ℂ :=
  ∏' p : Nat.Primes, eulerAFactor α β γ δ p

/-- `𝒴(α, β; γ, δ) = ζ(1+α+β) ζ(1+γ+δ) / (ζ(1+α+δ) ζ(1+β+γ)) · 𝒜(α, β; γ, δ)`
(Lee (2.2)). -/
noncomputable def ratiosY (α β γ δ : ℂ) : ℂ :=
  riemannZeta (1 + α + β) * riemannZeta (1 + γ + δ) *
    invZeta (1 + α + δ) * invZeta (1 + β + γ) * eulerA α β γ δ

/-- The integrand `ζ(½+α+it) ζ(½+β−it) / (ζ(½+γ+it) ζ(½+δ−it))`. -/
noncomputable def ratiosIntegrand (α β γ δ : ℂ) (t : ℝ) : ℂ :=
  riemannZeta (1 / 2 + α + t * I) * riemannZeta (1 / 2 + β - t * I) /
    (riemannZeta (1 / 2 + γ + t * I) * riemannZeta (1 / 2 + δ - t * I))

/-- The two main terms of the ratios formula (Lee (2.3)). -/
noncomputable def ratiosMain (α β γ δ : ℂ) (U : ℝ) : ℂ :=
  U * ratiosY α β γ δ +
    (∫ t in (0 : ℝ)..U, ((t / (2 * Real.pi) : ℝ) : ℂ) ^ (-α - β)) * ratiosY (-β) (-α) γ δ

/-- The admissible shifts at height `U` (Lee (2.4)). -/
def ShiftRange (ν U : ℝ) (s : ℂ) : Prop :=
  3 / 64 ≤ s.re ∧ s.re ≤ 5 / 64 ∧ |s.im| ≤ U ^ ν

/-- **Hypothesis 2.1 of Lee** (uniform two-over-two ratios formula) with error
exponent `θ` and imaginary-shift exponent `ν`.  **Open.**  The paper needs it
for some `1/2 ≤ θ < (39 − √177)/32` and some `0 < ν ≤ 1/4`. -/
def RatiosHypothesis (θ ν : ℝ) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ C U₀ : ℝ, ∀ U : ℝ, U₀ ≤ U → ∀ α β γ δ : ℂ,
    ShiftRange ν U α → ShiftRange ν U β → ShiftRange ν U γ → ShiftRange ν U δ →
      IntervalIntegrable (ratiosIntegrand α β γ δ) volume 0 U ∧
        ‖(∫ t in (0 : ℝ)..U, ratiosIntegrand α β γ δ t) - ratiosMain α β γ δ U‖
          ≤ C * U ^ (θ + ε)

/-! ## A check on the transcription

Lee's Lemma 2.2 uses `𝒴(α, η; η, η) = 1`.  It is proved here from the
definitions above, as a guard against a mis-stated Euler product. -/

private theorem one_sub_cpow_ne_zero {p : ℕ} (hp : p.Prime) {s : ℂ} (hs : s.re < 0) :
    1 - (p : ℂ) ^ s ≠ 0 := by
  intro h
  have h1 : ‖(p : ℂ) ^ s‖ = 1 := by
    rw [← sub_eq_zero.mp h]; simp
  rw [Complex.norm_natCast_cpow_of_pos hp.pos] at h1
  have : (p : ℝ) ^ s.re < 1 :=
    Real.rpow_lt_one_of_one_lt_of_neg (by exact_mod_cast hp.one_lt) hs
  linarith

theorem eulerAFactor_degenerate {α η : ℂ} (hα : 0 < α.re) (hη : 0 < η.re) {p : ℕ}
    (hp : p.Prime) : eulerAFactor α η η η p = 1 := by
  have h1 : 1 - (p : ℂ) ^ (-1 - η - η) ≠ 0 :=
    one_sub_cpow_ne_zero hp (by simp; linarith)
  have h2 : 1 - (p : ℂ) ^ (-1 - α - η) ≠ 0 :=
    one_sub_cpow_ne_zero hp (by simp; linarith)
  unfold eulerAFactor
  rw [div_eq_one_iff_eq (mul_ne_zero h1 h2)]
  ring

/-- **Proved.**  `𝒴(α, η; η, η) = 1` for shifts with positive real part. -/
theorem ratiosY_degenerate {α η : ℂ} (hα : 0 < α.re) (hη : 0 < η.re) :
    ratiosY α η η η = 1 := by
  have hA : eulerA α η η η = 1 := by
    unfold eulerA
    have : ∀ p : Nat.Primes, eulerAFactor α η η η p = 1 :=
      fun p => eulerAFactor_degenerate hα hη p.2
    simp [this]
  have re1 : 1 < (1 + α + η).re := by simp; linarith
  have re2 : 1 < (1 + η + η).re := by simp; linarith
  have n1 : (1 + α + η) ≠ 1 := fun h => by rw [h] at re1; simp at re1
  have n2 : (1 + η + η) ≠ 1 := fun h => by rw [h] at re2; simp at re2
  have z1 := riemannZeta_ne_zero_of_one_lt_re re1
  have z2 := riemannZeta_ne_zero_of_one_lt_re re2
  unfold ratiosY invZeta
  rw [hA, if_neg n1, if_neg n2]
  field_simp

/-- The upper end of the admissible error exponents, `(39 − √177)/32 ≈ 0.803`. -/
noncomputable def thetaStar : ℝ := (39 - Real.sqrt 177) / 32

/-- The twin prime constant `C₂ = ∏_{p > 2} (1 − 1/(p−1)²)`. -/
noncomputable def twinConstant : ℝ :=
  ∏' p : Nat.Primes, if (p : ℕ) = 2 then 1 else 1 - 1 / (((p : ℕ) : ℝ) - 1) ^ 2

/-- The local factor of the twin prime constant at `p`. -/
noncomputable def twinFactor (p : Nat.Primes) : ℝ :=
  if (p : ℕ) = 2 then 1 else 1 - 1 / (((p : ℕ) : ℝ) - 1) ^ 2

theorem twinConstant_eq : twinConstant = ∏' p : Nat.Primes, twinFactor p := rfl

/-- Every local factor is positive: for `p ≥ 3`, `(p − 1)² ≥ 4`. -/
theorem twinFactor_pos (p : Nat.Primes) : 0 < twinFactor p := by
  unfold twinFactor
  split_ifs with h
  · exact one_pos
  · have h3 : (3 : ℝ) ≤ ((p : ℕ) : ℝ) := by
      have : 3 ≤ (p : ℕ) := by
        have := p.2.two_le
        omega
      exact_mod_cast this
    have h4 : (1 : ℝ) < (((p : ℕ) : ℝ) - 1) ^ 2 := by nlinarith
    have : 1 / (((p : ℕ) : ℝ) - 1) ^ 2 < 1 := by
      rw [div_lt_one (by linarith)]; exact h4
    linarith

/-- The deviations `1 − (local factor)` are summable: they are at most `4 / p²`. -/
theorem summable_twinFactor_sub_one : Summable fun p : Nat.Primes => twinFactor p - 1 := by
  have hs : Summable fun p : Nat.Primes => 4 * (1 / (((p : ℕ) : ℝ)) ^ 2) := by
    have h := (Real.summable_one_div_nat_pow (p := 2)).mpr one_lt_two
    exact (h.comp_injective Nat.Primes.coe_nat_injective).mul_left 4
  refine Summable.of_norm_bounded hs fun p => ?_
  unfold twinFactor
  split_ifs with h
  · simp
  · have h3 : (3 : ℝ) ≤ ((p : ℕ) : ℝ) := by
      have : 3 ≤ (p : ℕ) := by
        have := p.2.two_le
        omega
      exact_mod_cast this
    have hpos : (0 : ℝ) < (((p : ℕ) : ℝ) - 1) ^ 2 := by nlinarith
    have hp2 : (0 : ℝ) < (((p : ℕ) : ℝ)) ^ 2 := by nlinarith
    have e : (1 - 1 / (((p : ℕ) : ℝ) - 1) ^ 2 - 1 : ℝ) = -(1 / (((p : ℕ) : ℝ) - 1) ^ 2) := by
      ring
    rw [e, norm_neg, Real.norm_of_nonneg (by positivity), div_le_iff₀ hpos]
    have : 4 * (1 / ((p : ℕ) : ℝ) ^ 2) * (((p : ℕ) : ℝ) - 1) ^ 2
        = 4 * (((p : ℕ) : ℝ) - 1) ^ 2 / ((p : ℕ) : ℝ) ^ 2 := by ring
    rw [this, le_div_iff₀ hp2]
    nlinarith

/-- **Proved.**  The twin prime constant is positive.  The product converges
absolutely because `∑ 1/(p−1)²` does, and no factor vanishes. -/
theorem twinConstant_pos : 0 < twinConstant := by
  have hlog : Summable fun p : Nat.Primes => Real.log (twinFactor p) := by
    have := Real.summable_log_one_add_of_summable summable_twinFactor_sub_one
    simpa using this
  rw [twinConstant_eq, ← Real.rexp_tsum_eq_tprod twinFactor_pos hlog]
  exact Real.exp_pos _

/-- The singular series `𝔖(h) = 2 C₂ ∏_{p ∣ h, p > 2} (p−1)/(p−2)` for even `h`
(Lee (1.1)).  Only meaningful for even `h`. -/
noncomputable def singularSeries (h : ℕ) : ℝ :=
  2 * twinConstant * ∏ p ∈ h.primeFactors.filter (2 < ·), ((p : ℝ) - 1) / ((p : ℝ) - 2)

theorem singularSeries_two : singularSeries 2 = 2 * twinConstant := by
  have : (Nat.primeFactors 2).filter (2 < ·) = ∅ := by
    rw [Nat.Prime.primeFactors Nat.prime_two]; rfl
  simp [singularSeries, this]

/-- The content of Lee's Theorem 1.1 for exponents `θ`, `ν`: the ratios
hypothesis implies the Hardy–Littlewood asymptotic for every positive even
difference.  **Not proved here**; see `lean/README.md` for the status of the
paper and of our check of its argument. -/
def LeeTheorem (θ ν : ℝ) : Prop :=
  RatiosHypothesis θ ν → ∀ h : ℕ, 0 < h → Even h → HardyLittlewoodPair h (singularSeries h)

/-- **The conditional chain.**  If Lee's theorem holds for some exponents and
the ratios hypothesis holds for the same exponents, then there are infinitely
many twin primes.

Both hypotheses are explicit.  The second is an open conjecture; the first is
a published argument that is not formalised here. -/
theorem twinPrime_of_ratios {θ ν : ℝ}
    (lee : LeeTheorem θ ν) (hr : RatiosHypothesis θ ν) : TwinPrimeConjecture := by
  have hl := lee hr 2 (by norm_num) (by decide)
  rw [singularSeries_two] at hl
  exact twinPrime_of_hardyLittlewood (mul_pos two_pos twinConstant_pos) hl

end Primefold
