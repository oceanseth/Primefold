import Primefold.Statements

/-!
# The elementary content of the Primefold note, machine-checked

Propositions 1, 2(i) and the reduction in Proposition 3 of
`paper/primefold-note.pdf`, plus the trivial implications from the open FI
statements to the twin prime conjecture.

Everything in this file is proved.  None of it is deep, and none of it is
progress on the twin prime conjecture.
-/

namespace Primefold

/-! ## Residues (Proposition 1) -/

private lemma fi_residue_aux : ∀ r < 8, ∀ s < 8, (r ^ 2 + s ^ 4) % 2 = 1 →
    ((r ^ 2 + s ^ 4) % 8 = 5 ↔ r % 4 = 2 ∧ s % 2 = 1) ∧
      ((r ^ 2 + s ^ 4) % 8 = 1 ∨ (r ^ 2 + s ^ 4) % 8 = 5) := by
  decide

/-- **Proposition 1.**  An odd number `a ^ 2 + b ^ 4` is `1` or `5` mod `8`, and
it is `5` mod `8` exactly when `a ≡ 2 (mod 4)` and `b` is odd. -/
theorem fi_mod_eight (a b : ℕ) (hodd : (a ^ 2 + b ^ 4) % 2 = 1) :
    ((a ^ 2 + b ^ 4) % 8 = 5 ↔ a % 4 = 2 ∧ b % 2 = 1) ∧
      ((a ^ 2 + b ^ 4) % 8 = 1 ∨ (a ^ 2 + b ^ 4) % 8 = 5) := by
  have h8 : (a ^ 2 + b ^ 4) % 8 = ((a % 8) ^ 2 + (b % 8) ^ 4) % 8 :=
    (Nat.ModEq.add ((Nat.mod_modEq a 8).pow 2) ((Nat.mod_modEq b 8).pow 4)).symm
  have h2 : ((a % 8) ^ 2 + (b % 8) ^ 4) % 2 = 1 := by omega
  have ha : a % 4 = a % 8 % 4 := by omega
  have hb : b % 2 = b % 8 % 2 := by omega
  rw [h8, ha, hb]
  exact fi_residue_aux _ (Nat.mod_lt _ (by norm_num)) _ (Nat.mod_lt _ (by norm_num)) h2

/-- An odd number of FI form is `1` mod `4`. -/
theorem fi_mod_four {n : ℕ} (h : IsFI n) (hodd : n % 2 = 1) : n % 4 = 1 := by
  obtain ⟨a, b, rfl⟩ := h
  have := (fi_mod_eight a b hodd).2
  omega

/-- An FI prime other than `2` is `1` mod `4`. -/
theorem IsFIPrime.mod_four {p : ℕ} (h : IsFIPrime p) (h2 : p ≠ 2) : p % 4 = 1 :=
  fi_mod_four h.2 (h.1.eq_two_or_odd.resolve_left h2)

/-! ## The twin of an FI prime (Proposition 2) -/

private lemma sq_add_sq_aux : ∀ r < 4, ∀ s < 4, (r ^ 2 + s ^ 2) % 4 ≠ 3 := by decide

/-- A number that is `3` mod `4` is not a sum of two squares. -/
theorem not_sq_add_sq_of_mod_four {q : ℕ} (hq : q % 4 = 3) (x y : ℕ) :
    q ≠ x ^ 2 + y ^ 2 := by
  rintro rfl
  have h4 : (x ^ 2 + y ^ 2) % 4 = ((x % 4) ^ 2 + (y % 4) ^ 2) % 4 :=
    (Nat.ModEq.add ((Nat.mod_modEq x 4).pow 2) ((Nat.mod_modEq y 4).pow 2)).symm
  exact sq_add_sq_aux _ (Nat.mod_lt _ (by norm_num)) _ (Nat.mod_lt _ (by norm_num))
    (h4 ▸ hq)

/-- **Proposition 2(i).**  If `p ≠ 2` is an FI prime then `p + 2` is `3` mod `4`,
so it is never a sum of two squares: the shift by `2` always leaves the
Gaussian world. -/
theorem IsFIPrime.add_two_not_sq_add_sq {p : ℕ} (h : IsFIPrime p) (h2 : p ≠ 2)
    (x y : ℕ) : p + 2 ≠ x ^ 2 + y ^ 2 :=
  not_sq_add_sq_of_mod_four (by have := h.mod_four h2; omega) x y

/-- The twin of an FI prime is never of FI form. -/
theorem IsFIPrime.add_two_not_fi {p : ℕ} (h : IsFIPrime p) (h2 : p ≠ 2) :
    ¬ IsFI (p + 2) := by
  rintro ⟨a, b, hab⟩
  exact h.add_two_not_sq_add_sq h2 a (b ^ 2) (by rw [hab]; ring)

/-- **Proposition 2(ii), (iii), residues only.**  The residue of `p + 2` mod `8`
is fixed by that of `p`: `3` when `p ≡ 1`, `7` when `p ≡ 5`.  (The
representations `x ^ 2 + 2 y ^ 2` and `x ^ 2 - 2 y ^ 2` that the note derives
from these residues are *not* formalised here.) -/
theorem IsFIPrime.add_two_mod_eight {p : ℕ} (h : IsFIPrime p) (h2 : p ≠ 2) :
    (p % 8 = 1 ∧ (p + 2) % 8 = 3) ∨ (p % 8 = 5 ∧ (p + 2) % 8 = 7) := by
  obtain ⟨hp, a, b, rfl⟩ := h
  have := (fi_mod_eight a b (hp.eq_two_or_odd.resolve_left h2)).2
  omega

/-- Two odd FI primes differ by a multiple of `4`; in particular the minimum
gap between FI primes is at least `4` (attained at `37, 41`). -/
theorem IsFIPrime.four_dvd_sub {p q : ℕ} (hp : IsFIPrime p) (hq : IsFIPrime q)
    (hp2 : p ≠ 2) (hq2 : q ≠ 2) : 4 ∣ q - p := by
  have := hp.mod_four hp2
  have := hq.mod_four hq2
  omega

/-! ## The pass-through fold (Proposition 3) -/

/-- **Proposition 3, reduction.**  `b ^ 4 + 2 = 2 y ^ 2` forces `b = 2 c` with
`y ^ 2 = 8 c ^ 4 + 1`.  (That `c = 1` is the only positive solution is the
quartic Pell statement; it is *not* proved here.) -/
theorem fold_reduction {b y : ℕ} (h : b ^ 4 + 2 = 2 * y ^ 2) :
    ∃ c, b = 2 * c ∧ y ^ 2 = 8 * c ^ 4 + 1 := by
  have he : Even (b ^ 4) := by
    have : Even (b ^ 4 + 2) := ⟨y ^ 2, by omega⟩
    exact (Nat.even_add.mp this).mpr even_two
  obtain ⟨c, rfl⟩ := (Nat.even_pow.mp he).1
  refine ⟨c, by ring, ?_⟩
  have : (c + c) ^ 4 = 16 * c ^ 4 := by ring
  omega

/-- The coincidence behind the fold: `4 ^ 2 + 2 = 2 * 3 ^ 2`, so `a ^ 2 + 2 ^ 4`
shifted by `2` is `a ^ 2 + 2 * 3 ^ 2`. -/
theorem fold_sixteen (a : ℕ) : a ^ 2 + 2 ^ 4 + 2 = a ^ 2 + 2 * 3 ^ 2 := by ring

/-- A member of the first fold family is an FI twin. -/
theorem isFITwin_of_fold_sixteen {a : ℕ} (h1 : (a ^ 2 + 16).Prime)
    (h2 : (a ^ 2 + 18).Prime) : IsFITwin (a ^ 2 + 16) :=
  ⟨⟨h1, a, 2, by norm_num⟩, h2⟩

/-- A member of the second fold family is an FI twin. -/
theorem isFITwin_of_fold_one {a : ℕ} (h1 : (a ^ 2 + 1).Prime)
    (h2 : (a ^ 2 + 3).Prime) : IsFITwin (a ^ 2 + 1) :=
  ⟨⟨h1, a, 1, by norm_num⟩, h2⟩

/-! ## What would imply the twin prime conjecture

Each hypothesis below is an open problem.  These implications show only that
the FI statements are at least as hard as twin primes. -/

theorem IsFITwin.isTwinPrime {p : ℕ} (h : IsFITwin p) : IsTwinPrime p := ⟨h.1.1, h.2⟩

/-- Infinitely many FI twins would give the twin prime conjecture. -/
theorem twinPrime_of_fiTwin (h : FITwinConjecture) : TwinPrimeConjecture := fun N =>
  let ⟨p, hN, hp⟩ := h N
  ⟨p, hN, hp.isTwinPrime⟩

/-- Infinitude of the family `(a ^ 2 + 16, a ^ 2 + 18)` would give infinitely
many FI twins. -/
theorem fiTwin_of_foldSixteen (h : FoldFamilySixteen) : FITwinConjecture := fun N =>
  let ⟨a, hN, h1, h2⟩ := h N
  ⟨a ^ 2 + 16, by nlinarith, isFITwin_of_fold_sixteen h1 h2⟩

/-- Infinitude of the family `(a ^ 2 + 1, a ^ 2 + 3)` would give infinitely many
FI twins. -/
theorem fiTwin_of_foldOne (h : FoldFamilyOne) : FITwinConjecture := fun N =>
  let ⟨a, hN, h1, h2⟩ := h N
  ⟨a ^ 2 + 1, by nlinarith, isFITwin_of_fold_one h1 h2⟩

/-! ## The first members, checked -/

example : IsFITwin 5 := ⟨⟨by norm_num, 2, 1, by norm_num⟩, by norm_num⟩
example : IsFITwin 17 := ⟨⟨by norm_num, 1, 2, by norm_num⟩, by norm_num⟩
example : IsFITwin 41 := ⟨⟨by norm_num, 5, 2, by norm_num⟩, by norm_num⟩
example : IsFITwin 101 := ⟨⟨by norm_num, 10, 1, by norm_num⟩, by norm_num⟩
example : IsFITwin 137 := ⟨⟨by norm_num, 11, 2, by norm_num⟩, by norm_num⟩
example : IsFITwin 9041 := isFITwin_of_fold_sixteen (a := 95) (by norm_num) (by norm_num)

/-- The minimum gap `4` between FI primes is attained at `(37, 41)`. -/
example : IsFIPrime 37 ∧ IsFIPrime 41 :=
  ⟨⟨by norm_num, 6, 1, by norm_num⟩, ⟨by norm_num, 5, 2, by norm_num⟩⟩

end Primefold
