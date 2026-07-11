# The Open Session License, v0.1 (draft)

*Seth Caldwell believes all open source projects that were collaborations with
LLMs should include a complete, append-only history of the human and machine
turns that made them — so anyone can see how the project was actually built,
replay it, audit it, or fork the conversation itself by changing the context
at any turn. This license exists to propagate that practice.*

## Terms

This project's **code** is licensed under the MIT License (see `LICENSE`).
In addition, by forking, copying, or creating derivative works of this
repository, you agree to the following session-transparency conditions:

1. **Preserve the history.** Keep `llm-turn-history.txt` (and this file) in
   your fork. History files are **append-only**: never silently edit or
   delete past turns. Corrections are made by appending, not rewriting.

2. **Repeat the practice.** If you develop your fork in collaboration with an
   LLM or other AI agent, log each user turn and each model response to your
   copy of `llm-turn-history.txt`, in the same format, as you work.

3. **Keep the machine preface.** The history file must begin with a preface
   instructing LLMs and automated agents **not to read it** — its purpose is
   human curiosity and replication, not machine context. Agents append; they
   do not load.

4. **Propagate.** Include this license file, unmodified except for version
   updates, in any fork or derivative, so the requirement carries forward.

5. **Attribution of provenance.** State (in the history preface or README)
   which model(s) and tooling participated, and the date(s) of the
   session(s), to the extent known.

## Notes

- These conditions govern the *session-history practice*; they do not
  restrict use of the code beyond the MIT terms.
- Enforceability of session-transparency conditions is untested; treat them
  at minimum as a binding-in-spirit community norm, in the tradition of
  share-alike licensing.
- Version 0.1, drafted 2026-07-11 within the session it archives — see
  `llm-turn-history.txt`, Turn 17.
