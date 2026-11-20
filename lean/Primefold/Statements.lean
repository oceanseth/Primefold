import Mathlib

/-!
# Statements

The twin prime conjecture and the Friedlander–Iwaniec (FI) objects of the
Primefold note, stated against Mathlib.  Nothing here is proved; these are
definitions only.
-/

namespace Primefold

/-- `p` and `p + 2` are both prime. -/
def IsTwinPrime (p : ℕ) : Prop := p.Prime ∧ (p + 2).Prime

/-- The twin prime conjecture: twin primes occur beyond every bound.  **Open.** -/
def TwinPrimeConjecture : Prop := ∀ N : ℕ, ∃ p, N < p ∧ IsTwinPrime p

/-- `n` has the Friedlander–Iwaniec form `a ^ 2 + b ^ 4`. -/
def IsFI (n : ℕ) : Prop := ∃ a b : ℕ, n = a ^ 2 + b ^ 4

/-- An FI prime: a prime of the form `a ^ 2 + b ^ 4`. -/
def IsFIPrime (p : ℕ) : Prop := p.Prime ∧ IsFI p

/-- An FI twin: an FI prime `p` with `p + 2` also prime. -/
def IsFITwin (p : ℕ) : Prop := IsFIPrime p ∧ (p + 2).Prime

/-- Infinitely many FI twins.  **Open**, and at least as hard as twin primes
(`Primefold.twinPrime_of_fiTwin`). -/
def FITwinConjecture : Prop := ∀ N : ℕ, ∃ p, N < p ∧ IsFITwin p

/-- The first pass-through fold family of the note: `a ^ 2 + 16` and
`a ^ 2 + 18` both prime for arbitrarily large `a`.  An instance of Schinzel's
Hypothesis H.  **Open.** -/
def FoldFamilySixteen : Prop :=
  ∀ N : ℕ, ∃ a, N < a ∧ (a ^ 2 + 16).Prime ∧ (a ^ 2 + 18).Prime

/-- The second family: `a ^ 2 + 1` and `a ^ 2 + 3` both prime for arbitrarily
large `a`.  **Open** (it contains Landau's `n ^ 2 + 1` problem). -/
def FoldFamilyOne : Prop :=
  ∀ N : ℕ, ∃ a, N < a ∧ (a ^ 2 + 1).Prime ∧ (a ^ 2 + 3).Prime

end Primefold
