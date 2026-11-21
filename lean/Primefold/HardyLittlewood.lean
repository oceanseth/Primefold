import Primefold.Statements

/-!
# From a prime-pair count to infinitely many prime pairs

The last link of the conditional chain

  ratios formula  ⟶  Hardy–Littlewood asymptotic  ⟶  infinitely many twin primes

is elementary and is proved here in full: if the number of `p ≤ x` with `p`
and `p + h` both prime is asymptotic to `S · x / (log x)²` with `S > 0`, then
there are such `p` beyond every bound.  No hypothesis other than the
asymptotic itself is used.
-/

open Filter Topology

namespace Primefold

/-- The number of `p ≤ x` with `p` and `p + h` both prime. -/
def pairCount (h x : ℕ) : ℕ :=
  ((Finset.range (x + 1)).filter fun p => p.Prime ∧ (p + h).Prime).card

/-- The Hardy–Littlewood asymptotic for prime pairs of difference `h`, with
constant `S`:  `π_h(x) ~ S · x / (log x)²`.  A statement, not a theorem;
for even `h` and `S = 𝔖(h)` it is **open**. -/
def HardyLittlewoodPair (h : ℕ) (S : ℝ) : Prop :=
  Tendsto (fun x : ℕ => (pairCount h x : ℝ) * Real.log x ^ 2 / x) atTop (𝓝 S)

/-- If only finitely many prime pairs of difference `h` existed, their count
would be bounded. -/
theorem pairCount_le_of_bounded {h N : ℕ}
    (hN : ∀ p, N < p → p.Prime → ¬(p + h).Prime) (x : ℕ) : pairCount h x ≤ N + 1 := by
  unfold pairCount
  calc ((Finset.range (x + 1)).filter fun p => p.Prime ∧ (p + h).Prime).card
      ≤ (Finset.range (N + 1)).card := by
        apply Finset.card_le_card
        intro p hp
        simp only [Finset.mem_filter, Finset.mem_range] at hp ⊢
        by_contra hlt
        exact hN p (by omega) hp.2.1 hp.2.2
    _ = N + 1 := Finset.card_range _

/-- **Proved.**  A Hardy–Littlewood asymptotic with positive constant forces
prime pairs of difference `h` beyond every bound. -/
theorem infinite_pairs_of_hardyLittlewood {h : ℕ} {S : ℝ} (hS : 0 < S)
    (hl : HardyLittlewoodPair h S) : ∀ N : ℕ, ∃ p, N < p ∧ p.Prime ∧ (p + h).Prime := by
  by_contra hcon
  push Not at hcon
  obtain ⟨N, hN⟩ := hcon
  have hzero : Tendsto (fun x : ℕ => ((N : ℝ) + 1) * (Real.log x ^ 2 / x)) atTop (𝓝 0) := by
    have h1 : Tendsto (fun x : ℝ => Real.log x ^ 2 / x) atTop (𝓝 0) :=
      (Real.isLittleO_pow_log_id_atTop (n := 2)).tendsto_div_nhds_zero
    simpa using (h1.comp tendsto_natCast_atTop_atTop).const_mul ((N : ℝ) + 1)
  have hle : Tendsto (fun x : ℕ => (pairCount h x : ℝ) * Real.log x ^ 2 / x) atTop (𝓝 0) := by
    refine tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hzero ?_ ?_
    · intro x; positivity
    · intro x
      have hb : (pairCount h x : ℝ) ≤ N + 1 := by
        exact_mod_cast pairCount_le_of_bounded hN x
      have hnn : 0 ≤ Real.log x ^ 2 / (x : ℝ) := by positivity
      calc (pairCount h x : ℝ) * Real.log x ^ 2 / x
          = (pairCount h x : ℝ) * (Real.log x ^ 2 / x) := by ring
        _ ≤ ((N : ℝ) + 1) * (Real.log x ^ 2 / x) := by gcongr
  have := tendsto_nhds_unique hl hle
  linarith

/-- **Proved.**  The Hardy–Littlewood asymptotic for difference `2` with a
positive constant implies the twin prime conjecture. -/
theorem twinPrime_of_hardyLittlewood {S : ℝ} (hS : 0 < S)
    (hl : HardyLittlewoodPair 2 S) : TwinPrimeConjecture := by
  intro N
  obtain ⟨p, hp, h1, h2⟩ := infinite_pairs_of_hardyLittlewood hS hl N
  exact ⟨p, hp, h1, h2⟩

end Primefold
