import Primefold.Statements

/-!
# Where the Riemann Hypothesis sits relative to this project

On 2026-11-20 a Lean archive was published claiming proofs of Mathlib's
`RiemannHypothesis` and of the corresponding statement for Dirichlet
L-functions.  As of that date the claim has had no expert review.

This file does **not** import that archive (it is very large and was published
without a license).  It states the Dirichlet statement independently, as a
hypothesis, against the same Lean and Mathlib versions the archive pins, so
that results depending on it can be written here and discharged later if the
claim survives review.

## What is deliberately absent

There is no theorem `RiemannHypothesis → TwinPrimeConjecture` or
`GRHDirichlet → TwinPrimeConjecture` in this project, with or without `sorry`,
because no such implication is known.  GRH controls primes in arithmetic
progressions one modulus at a time; the twin prime problem is blocked by the
parity barrier of sieve theory, which information about zeros does not
address.  See `lean/README.md`.
-/

namespace Primefold

/-- The Riemann Hypothesis for Dirichlet L-functions: every zero in the open
critical strip lies on the line `Re s = 1 / 2`.  A hypothesis, not a theorem. -/
def GRHDirichlet : Prop :=
  ∀ (N : ℕ) [NeZero N] (χ : DirichletCharacter ℂ N) (s : ℂ),
    0 < s.re → s.re < 1 → DirichletCharacter.LFunction χ s = 0 → s.re = 1 / 2

/-- Sanity check on the statement: the Dirichlet hypothesis contains the
critical-strip statement for the Riemann zeta function (the character mod `1`). -/
theorem GRHDirichlet.riemannZeta (h : GRHDirichlet) (s : ℂ) (h0 : 0 < s.re)
    (h1 : s.re < 1) (hs : riemannZeta s = 0) : s.re = 1 / 2 :=
  h 1 (1 : DirichletCharacter ℂ 1) s h0 h1
    (by rw [DirichletCharacter.LFunction_modOne_eq]; exact hs)

end Primefold
