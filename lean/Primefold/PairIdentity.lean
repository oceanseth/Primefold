import Primefold.HardyLittlewood

/-!
# An exact identity for prime pairs, and a positivity criterion for twin primes

Unconditional.  This is the mechanism of Lemma 3.1 of S. Lee,
arXiv:2610.32672v2, in a slightly simpler form (see `lean/IDEAS.md`, idea 1).
-/

open MeasureTheory FourierTransform

namespace Primefold

/-- The Dirichlet polynomial `∑ₙ aₙ e^{-i u λₙ}` over a finite set. -/
noncomputable def dirPoly (s : Finset ℕ) (a lam : ℕ → ℝ) (u : ℝ) : ℂ :=
  ∑ n ∈ s, (a n : ℂ) * Complex.exp (((-(u * lam n) : ℝ) : ℂ) * Complex.I)

/-- `|∑ₙ aₙ e^{-i u λₙ}|²` expanded as a double sum. -/
theorem normSq_dirPoly (s : Finset ℕ) (a lam : ℕ → ℝ) (u : ℝ) :
    ((‖dirPoly s a lam u‖ ^ 2 : ℝ) : ℂ) =
      ∑ m ∈ s, ∑ n ∈ s, ((a m * a n : ℝ) : ℂ) *
        Complex.exp (((-(u * (lam m - lam n)) : ℝ) : ℂ) * Complex.I) := by
  have hconj : (starRingEnd ℂ) (dirPoly s a lam u) =
      ∑ n ∈ s, (a n : ℂ) * Complex.exp (((u * lam n : ℝ) : ℂ) * Complex.I) := by
    unfold dirPoly
    rw [map_sum]
    refine Finset.sum_congr rfl fun n _ => ?_
    rw [map_mul, Complex.conj_ofReal, ← Complex.exp_conj, map_mul, Complex.conj_ofReal,
      Complex.conj_I]
    congr 2
    push_cast
    ring
  have hsq : ((‖dirPoly s a lam u‖ ^ 2 : ℝ) : ℂ) =
      dirPoly s a lam u * (starRingEnd ℂ) (dirPoly s a lam u) := by
    rw [Complex.mul_conj']
    push_cast
    rfl
  rw [hsq, hconj]
  unfold dirPoly
  rw [Finset.sum_mul_sum]
  refine Finset.sum_congr rfl fun m _ => Finset.sum_congr rfl fun n _ => ?_
  rw [mul_mul_mul_comm, ← Complex.exp_add]
  push_cast
  congr 2
  ring

/-- Fourier inversion in the form used below: the Fourier transform of `𝓕 ψ`
against a pure frequency returns a value of `ψ`. -/
theorem integral_fourier_mul_exp {ψ : ℝ → ℂ} (hc : Continuous ψ) (hi : Integrable ψ)
    (hF : Integrable (𝓕 ψ)) (w : ℝ) :
    ∫ u, 𝓕 ψ u * Complex.exp (((-(u * w) : ℝ) : ℂ) * Complex.I) = ψ (-(w / (2 * Real.pi))) := by
  have key : 𝓕 (𝓕 ψ) (w / (2 * Real.pi)) = ψ (-(w / (2 * Real.pi))) := by
    have h1 := Real.fourierInv_eq_fourier_neg (𝓕 ψ) (-(w / (2 * Real.pi)))
    rw [neg_neg] at h1
    rw [← h1, hc.fourierInv_fourier_eq hi hF]
  rw [← key, Real.fourier_real_eq_integral_exp_smul]
  refine integral_congr_ae (Filter.Eventually.of_forall fun u => ?_)
  simp only [smul_eq_mul]
  rw [mul_comm]
  congr 3
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

/-- **The general identity.**  For a continuous integrable `ψ` with integrable
Fourier transform, integrating `𝓕 ψ` against `|∑ aₙ e^{-iuλₙ}|²` returns the
values of `ψ` at the frequency differences. -/
theorem integral_fourier_mul_normSq {ψ : ℝ → ℂ} (hc : Continuous ψ) (hi : Integrable ψ)
    (hF : Integrable (𝓕 ψ)) (s : Finset ℕ) (a lam : ℕ → ℝ) :
    ∫ u, 𝓕 ψ u * ((‖dirPoly s a lam u‖ ^ 2 : ℝ) : ℂ) =
      ∑ m ∈ s, ∑ n ∈ s, ((a m * a n : ℝ) : ℂ) * ψ ((lam n - lam m) / (2 * Real.pi)) := by
  simp_rw [normSq_dirPoly, Finset.mul_sum]
  have hint : ∀ m n, Integrable (fun u => 𝓕 ψ u * (((a m * a n : ℝ) : ℂ) *
      Complex.exp (((-(u * (lam m - lam n)) : ℝ) : ℂ) * Complex.I))) := by
    intro m n
    refine (hF.norm.const_mul |a m * a n|).mono' (hF.aestronglyMeasurable.mul ?_)
      (Filter.Eventually.of_forall fun u => ?_)
    · exact Continuous.aestronglyMeasurable (by fun_prop)
    · rw [norm_mul, norm_mul, Complex.norm_exp_ofReal_mul_I, mul_one, Complex.norm_real,
        Real.norm_eq_abs, mul_comm]
  rw [integral_finsetSum _ fun m _ => integrable_finsetSum _ fun n _ => hint m n]
  refine Finset.sum_congr rfl fun m _ => ?_
  rw [integral_finsetSum _ fun n _ => hint m n]
  refine Finset.sum_congr rfl fun n _ => ?_
  have h2 : (fun u => 𝓕 ψ u * (((a m * a n : ℝ) : ℂ) *
      Complex.exp (((-(u * (lam m - lam n)) : ℝ) : ℂ) * Complex.I))) =
      fun u => ((a m * a n : ℝ) : ℂ) *
        (𝓕 ψ u * Complex.exp (((-(u * (lam m - lam n)) : ℝ) : ℂ) * Complex.I)) := by
    funext u; ring
  rw [h2, integral_const_mul, integral_fourier_mul_exp hc hi hF]
  congr 2
  ring

/-! ## Only the difference `h` survives -/

/-- For integers `x < m < n < (1 + 1/(25h))·x`, the quantity
`x·(log n − log m)` lies strictly between `(n − m)/κ` and `n − m`. -/
theorem log_window_bounds {x κ : ℝ} (hx : 0 < x) {m n : ℕ} (hm : x < m) (hmn : m < n)
    (hn : (n : ℝ) < κ * x) :
    x * (Real.log n - Real.log m) < (n : ℝ) - m ∧
      (n : ℝ) - m < κ * (x * (Real.log n - Real.log m)) := by
  have hm0 : (0 : ℝ) < m := hx.trans hm
  have hmn' : (m : ℝ) < n := by exact_mod_cast hmn
  have hn0 : (0 : ℝ) < n := hm0.trans hmn'
  have hκx : 0 < κ * x := hn0.trans hn
  have hd : (0 : ℝ) < (n : ℝ) - m := sub_pos.mpr hmn'
  constructor
  · -- log n − log m ≤ n/m − 1
    have h1 : Real.log n - Real.log m ≤ (n : ℝ) / m - 1 := by
      rw [← Real.log_div hn0.ne' hm0.ne']
      exact Real.log_le_sub_one_of_pos (div_pos hn0 hm0)
    have h2 : (n : ℝ) / m - 1 = ((n : ℝ) - m) / m := by field_simp
    calc x * (Real.log n - Real.log m) ≤ x * (((n : ℝ) - m) / m) := by
          rw [← h2]; exact mul_le_mul_of_nonneg_left h1 hx.le
      _ = ((n : ℝ) - m) * (x / m) := by ring
      _ < ((n : ℝ) - m) * 1 := by
          apply mul_lt_mul_of_pos_left _ hd
          rw [div_lt_one hm0]; exact hm
      _ = (n : ℝ) - m := mul_one _
  · -- log n − log m ≥ (n − m)/n
    have h1 : ((n : ℝ) - m) / n ≤ Real.log n - Real.log m := by
      have := Real.log_le_sub_one_of_pos (div_pos hm0 hn0)
      rw [Real.log_div hm0.ne' hn0.ne'] at this
      have h3 : ((n : ℝ) - m) / n = 1 - (m : ℝ) / n := by field_simp
      rw [h3]; linarith
    calc (n : ℝ) - m = ((n : ℝ) - m) * 1 := (mul_one _).symm
      _ < ((n : ℝ) - m) * (κ * x / n) := by
          apply mul_lt_mul_of_pos_left _ hd
          rw [one_lt_div hn0]; exact hn
      _ = κ * (x * (((n : ℝ) - m) / n)) := by ring
      _ ≤ κ * (x * (Real.log n - Real.log m)) := by
          have hκ : 0 < κ := by
            by_contra hneg
            have := mul_nonpos_of_nonpos_of_nonneg (not_lt.mp hneg) hx.le
            linarith
          exact mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left h1 hx.le) hκ.le

/-- **Window lemma.**  For integers `x < m < n < (1 + 1/(25h))·x`, if
`x·(log n − log m)` is within `1/4` of `h` then `n = m + h`. -/
theorem eq_add_of_window {h : ℕ} (hh : 1 ≤ h) {x : ℝ} (hx : 0 < x) {m n : ℕ} (hm : x < m)
    (hmn : m < n) (hn : (n : ℝ) < (1 + 1 / (25 * (h : ℝ))) * x)
    (hw : |x * (Real.log n - Real.log m) - h| < 1 / 4) : n = m + h := by
  obtain ⟨hup, hlo⟩ := log_window_bounds hx hm hmn hn
  rw [abs_lt] at hw
  obtain ⟨hw1, hw2⟩ := hw
  set v := x * (Real.log n - Real.log m) with hv
  have hh' : (1 : ℝ) ≤ h := by exact_mod_cast hh
  set c : ℝ := 1 / (25 * (h : ℝ)) with hc
  have hc0 : 0 < c := by positivity
  have hch : c * h = 1 / 25 := by rw [hc]; field_simp
  have hc1 : c ≤ 1 / 25 := by nlinarith
  rcases lt_trichotomy n (m + h) with hlt | heq | hgt
  · exfalso
    have : (n : ℝ) + 1 ≤ m + h := by exact_mod_cast hlt
    linarith
  · exact heq
  · exfalso
    have h5 : (m : ℝ) + h + 1 ≤ n := by exact_mod_cast hgt
    have h6 : (1 + c) * v < (1 + c) * (h + 1 / 4) := by
      apply mul_lt_mul_of_pos_left _ (by linarith)
      linarith
    nlinarith

/-! ## The pair sum and its sign -/

/-- A test function for difference `h`: continuous, even, nonnegative, with
integrable Fourier transform, vanishing unless `|v|` is within `1/4` of `h`, and
positive just below `h`. -/
structure PairTest (h : ℕ) (ρ : ℝ → ℝ) : Prop where
  cont : Continuous ρ
  integrable : Integrable (fun v => (ρ v : ℂ))
  integrable_fourier : Integrable (𝓕 fun v => (ρ v : ℂ))
  nonneg : ∀ v, 0 ≤ ρ v
  even : ∀ v, ρ (-v) = ρ v
  supp : ∀ v, 0 ≤ v → ρ v ≠ 0 → |v - h| < 1 / 4
  pos : ∀ v, (h : ℝ) - 1 / 25 < v → v < h → 0 < ρ v

/-- The double sum `∑ₘ ∑ₙ aₘ aₙ ρ(x (log n − log m))`. -/
noncomputable def pairSum (ρ : ℝ → ℝ) (x : ℝ) (s : Finset ℕ) (a : ℕ → ℝ) : ℝ :=
  ∑ m ∈ s, ∑ n ∈ s, a m * a n * ρ (x * (Real.log n - Real.log m))

/-- **The identity**, in the scaled variable `u = t / (2πx)`:
`∫ 𝓕ρ(u) |∑ₙ aₙ n^{-2πixu}|² du` is the pair sum. -/
theorem integral_eq_pairSum {h : ℕ} {ρ : ℝ → ℝ} (hρ : PairTest h ρ) (x : ℝ) (s : Finset ℕ)
    (a : ℕ → ℝ) :
    ∫ u, 𝓕 (fun v => (ρ v : ℂ)) u *
        ((‖dirPoly s a (fun n => 2 * Real.pi * x * Real.log n) u‖ ^ 2 : ℝ) : ℂ) =
      (pairSum ρ x s a : ℂ) := by
  have hcont : Continuous (fun v => (ρ v : ℂ)) := Complex.continuous_ofReal.comp hρ.cont
  rw [integral_fourier_mul_normSq hcont hρ.integrable hρ.integrable_fourier]
  unfold pairSum
  push_cast
  refine Finset.sum_congr rfl fun m _ => Finset.sum_congr rfl fun n _ => ?_
  congr 3
  have : (2 * Real.pi) ≠ 0 := by positivity
  field_simp

/-- **Sign criterion.**  If every element of `s` lies in `(x, (1 + 1/(25h))·x)`
and the coefficients are positive on `s`, the pair sum is positive exactly when
`s` contains two elements differing by `h`. -/
theorem pairSum_pos_iff {h : ℕ} (hh : 1 ≤ h) {ρ : ℝ → ℝ} (hρ : PairTest h ρ) {x : ℝ}
    (hx : 0 < x) {s : Finset ℕ} {a : ℕ → ℝ}
    (hs : ∀ n ∈ s, x < n ∧ (n : ℝ) < (1 + 1 / (25 * (h : ℝ))) * x) (ha : ∀ n ∈ s, 0 < a n) :
    0 < pairSum ρ x s a ↔ ∃ m ∈ s, m + h ∈ s := by
  have hh' : (1 : ℝ) ≤ h := by exact_mod_cast hh
  set c : ℝ := 1 / (25 * (h : ℝ)) with hc
  have hc0 : 0 < c := by positivity
  have hch : c * h = 1 / 25 := by rw [hc]; field_simp
  -- for m < n in s: ρ at the pair is nonzero only if n = m + h
  have key : ∀ m ∈ s, ∀ n ∈ s, m < n → ρ (x * (Real.log n - Real.log m)) ≠ 0 → n = m + h := by
    intro m hm n hn hmn hne
    obtain ⟨_, hlo⟩ := log_window_bounds hx (hs m hm).1 hmn (hs n hn).2
    have hd : (0 : ℝ) < (n : ℝ) - m := sub_pos.mpr (by exact_mod_cast hmn)
    have hv : 0 ≤ x * (Real.log n - Real.log m) := by
      by_contra hneg
      have := mul_neg_of_pos_of_neg (show (0 : ℝ) < 1 + c by linarith) (not_le.mp hneg)
      linarith
    exact eq_add_of_window hh hx (hs m hm).1 hmn (hs n hn).2 (hρ.supp _ hv hne)
  have hzero : ρ 0 = 0 := by
    by_contra hne
    have := hρ.supp 0 le_rfl hne
    rw [abs_lt] at this
    linarith [this.1]
  constructor
  · intro hpos
    by_contra hno
    push Not at hno
    have : pairSum ρ x s a = 0 := by
      unfold pairSum
      refine Finset.sum_eq_zero fun m hm => Finset.sum_eq_zero fun n hn => ?_
      have hρ0 : ρ (x * (Real.log n - Real.log m)) = 0 := by
        rcases lt_trichotomy m n with hlt | heq | hgt
        · by_contra hne
          exact hno m hm (key m hm n hn hlt hne ▸ hn)
        · subst heq; simpa using hzero
        · by_contra hne
          have hne' : ρ (x * (Real.log m - Real.log n)) ≠ 0 := by
            rw [← hρ.even]
            convert hne using 2
            ring
          exact hno n hn (key n hn m hm hgt hne' ▸ hm)
      rw [hρ0, mul_zero]
    linarith
  · rintro ⟨m, hm, hmh⟩
    unfold pairSum
    have hnn : ∀ m ∈ s, ∀ n ∈ s, 0 ≤ a m * a n * ρ (x * (Real.log n - Real.log m)) :=
      fun m hm n hn => mul_nonneg (mul_nonneg (ha m hm).le (ha n hn).le) (hρ.nonneg _)
    refine Finset.sum_pos' (fun m hm => Finset.sum_nonneg fun n hn => hnn m hm n hn)
      ⟨m, hm, Finset.sum_pos' (fun n hn => hnn m hm n hn) ⟨m + h, hmh, ?_⟩⟩
    have hmn : m < m + h := by omega
    obtain ⟨hup, hlo⟩ := log_window_bounds hx (hs m hm).1 hmn (hs _ hmh).2
    have hcast : (((m + h : ℕ) : ℝ)) - m = h := by push_cast; ring
    rw [hcast] at hup hlo
    refine mul_pos (mul_pos (ha m hm) (ha _ hmh)) (hρ.pos _ ?_ hup)
    nlinarith

/-! ## Twin primes -/

open Classical in
/-- The primes in the open interval `(x, (51/50)·x)`. -/
noncomputable def twinSet (x : ℝ) : Finset ℕ :=
  (Finset.range (⌈(51 / 50 : ℝ) * x⌉₊ + 1)).filter fun p =>
    x < p ∧ (p : ℝ) < 51 / 50 * x ∧ p.Prime

/-- `∑ (log p / √p) · p^{-2πixu}` over the primes `p` in `(x, (51/50)·x)`. -/
noncomputable def twinPoly (x u : ℝ) : ℂ :=
  dirPoly (twinSet x) (fun n => Real.log n / Real.sqrt n)
    (fun n => 2 * Real.pi * x * Real.log n) u

theorem mem_twinSet {x : ℝ} {p : ℕ} :
    p ∈ twinSet x ↔ x < p ∧ (p : ℝ) < 51 / 50 * x ∧ p.Prime := by
  unfold twinSet
  simp only [Finset.mem_filter, Finset.mem_range, and_iff_right_iff_imp]
  rintro ⟨_, h2, _⟩
  have := Nat.le_ceil ((51 / 50 : ℝ) * x)
  have h3 : (p : ℝ) < (⌈(51 / 50 : ℝ) * x⌉₊ : ℝ) + 1 := by linarith
  exact_mod_cast h3

/-- **Twin primes as a positivity statement.**  For any test function `ρ` for
difference `2`, the twin prime conjecture holds if and only if the integral
`∫ 𝓕ρ(u) · |∑_{x < p < 51x/50} (log p / √p) p^{-2πixu}|² du` is strictly positive
for arbitrarily large `x`.  Unconditional; both sides are open. -/
theorem twinPrime_iff_integral_pos {ρ : ℝ → ℝ} (hρ : PairTest 2 ρ) :
    TwinPrimeConjecture ↔ ∀ N : ℕ, ∃ x : ℝ, (N : ℝ) < x ∧
      0 < (∫ u, 𝓕 (fun v => (ρ v : ℂ)) u * ((‖twinPoly x u‖ ^ 2 : ℝ) : ℂ)).re := by
  have crit : ∀ x : ℝ, 0 < x →
      (0 < (∫ u, 𝓕 (fun v => (ρ v : ℂ)) u * ((‖twinPoly x u‖ ^ 2 : ℝ) : ℂ)).re ↔
        ∃ m ∈ twinSet x, m + 2 ∈ twinSet x) := by
    intro x hx
    unfold twinPoly
    rw [integral_eq_pairSum hρ, Complex.ofReal_re]
    refine pairSum_pos_iff (h := 2) (by norm_num) hρ hx (fun n hn => ?_) (fun n hn => ?_)
    · obtain ⟨h1, h2, _⟩ := mem_twinSet.mp hn
      refine ⟨h1, ?_⟩
      norm_num
      linarith
    · obtain ⟨_, _, hp⟩ := mem_twinSet.mp hn
      have h2 : (2 : ℝ) ≤ n := by exact_mod_cast hp.two_le
      exact div_pos (Real.log_pos (by linarith)) (Real.sqrt_pos.mpr (by linarith))
  constructor
  · intro htp N
    obtain ⟨p, hpN, hp1, hp2⟩ := htp (max N 200)
    have hN : (N : ℝ) + 1 ≤ p := by
      have : N + 1 ≤ p := by omega
      exact_mod_cast this
    have h200 : (201 : ℝ) ≤ p := by
      have : 201 ≤ p := by omega
      exact_mod_cast this
    refine ⟨(p : ℝ) - 1 / 2, by linarith, (crit _ (by linarith)).mpr ⟨p, ?_, ?_⟩⟩
    · exact mem_twinSet.mpr ⟨by linarith, by linarith, hp1⟩
    · refine mem_twinSet.mpr ⟨by push_cast; linarith, by push_cast; linarith, hp2⟩
  · intro hpos N
    obtain ⟨x, hNx, hx⟩ := hpos N
    have hx0 : 0 < x := lt_of_le_of_lt (Nat.cast_nonneg N) hNx
    obtain ⟨m, hm, hm2⟩ := (crit x hx0).mp hx
    obtain ⟨h1, _, hp⟩ := mem_twinSet.mp hm
    obtain ⟨_, _, hp2⟩ := mem_twinSet.mp hm2
    exact ⟨m, by exact_mod_cast hNx.trans h1, hp, hp2⟩

/-! ## Test functions exist -/

open scoped SchwartzMap ContDiff in
/-- **Proved.**  A test function exists for every difference `h ≥ 1`: the sum
of a smooth bump at `h` and its reflection. -/
theorem exists_pairTest {h : ℕ} (hh : 1 ≤ h) : ∃ ρ : ℝ → ℝ, PairTest h ρ := by
  have hh' : (1 : ℝ) ≤ h := by exact_mod_cast hh
  let f : ContDiffBump (h : ℝ) := ⟨1 / 10, 1 / 5, by norm_num, by norm_num⟩
  have hz : ∀ v : ℝ, 1 / 5 ≤ |v - h| → f v = 0 := by
    intro v hv
    by_contra hne
    have hmem : v ∈ Function.support f := hne
    rw [f.support_eq, Metric.mem_ball, Real.dist_eq] at hmem
    have hmem' : |v - h| < 1 / 5 := hmem
    linarith
  have hp : ∀ v : ℝ, |v - h| < 1 / 5 → 0 < f v := by
    intro v hv
    apply f.pos_of_mem_ball
    rw [Metric.mem_ball, Real.dist_eq]
    exact hv
  let ρ : ℝ → ℝ := fun v => f v + f (-v)
  have hsm : ContDiff ℝ ∞ (fun v => (ρ v : ℂ)) :=
    Complex.ofRealCLM.contDiff.comp (f.contDiff.add (f.contDiff.comp contDiff_neg))
  have hcs : HasCompactSupport (fun v => (ρ v : ℂ)) := by
    refine HasCompactSupport.intro (isCompact_closedBall (0 : ℝ) ((h : ℝ) + 1)) fun v hv => ?_
    rw [Metric.mem_closedBall, Real.dist_eq, sub_zero, not_le] at hv
    have hha : |(h : ℝ)| = h := abs_of_nonneg (by linarith)
    have h1 : f v = 0 := hz v (by
      have := abs_sub_abs_le_abs_sub v (h : ℝ)
      linarith)
    have h2 : f (-v) = 0 := hz (-v) (by
      have := abs_sub_abs_le_abs_sub (-v) (h : ℝ)
      rw [abs_neg] at this
      linarith)
    simp [ρ, h1, h2]
  let S : 𝓢(ℝ, ℂ) := hcs.toSchwartzMap hsm
  refine ⟨ρ, ⟨f.continuous.add (f.continuous.comp continuous_neg), S.integrable, ?_,
    fun v => add_nonneg f.nonneg f.nonneg, fun v => by simp [ρ, add_comm], ?_, ?_⟩⟩
  · have hi : Integrable ((𝓕 S : 𝓢(ℝ, ℂ)) : ℝ → ℂ) volume := (𝓕 S : 𝓢(ℝ, ℂ)).integrable
    rw [SchwartzMap.fourier_coe] at hi
    exact hi
  · intro v hv0 hne
    by_contra hnot
    rw [not_lt] at hnot
    have h1 : f v = 0 := hz v (by linarith)
    have h2 : f (-v) = 0 := hz (-v) (by
      have : |(-v) - (h : ℝ)| = v + h := by
        rw [show (-v) - (h : ℝ) = -(v + h) by ring, abs_neg, abs_of_nonneg (by linarith)]
      linarith)
    exact hne (by simp [ρ, h1, h2])
  · intro v hv1 hv2
    have h1 : 0 < f v := hp v (by rw [abs_lt]; constructor <;> linarith)
    have h2 : 0 ≤ f (-v) := f.nonneg
    exact add_pos_of_pos_of_nonneg h1 h2

/-- **Twin primes as a positivity statement, with no hypotheses.**  There is an
explicit kind of weight `ρ` for which the twin prime conjecture is equivalent
to the strict positivity, for arbitrarily large `x`, of
`∫ 𝓕ρ(u) · |∑_{x < p < 51x/50} (log p / √p) p^{-2πixu}|² du`.
This reformulates the conjecture; it does not prove it. -/
theorem exists_twinPrime_iff_integral_pos :
    ∃ ρ : ℝ → ℝ, PairTest 2 ρ ∧
      (TwinPrimeConjecture ↔ ∀ N : ℕ, ∃ x : ℝ, (N : ℝ) < x ∧
        0 < (∫ u, 𝓕 (fun v => (ρ v : ℂ)) u * ((‖twinPoly x u‖ ^ 2 : ℝ) : ℂ)).re) := by
  obtain ⟨ρ, hρ⟩ := exists_pairTest (h := 2) (by norm_num)
  exact ⟨ρ, hρ, twinPrime_iff_integral_pos hρ⟩

end Primefold
