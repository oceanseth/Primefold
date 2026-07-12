# The Open Session License, v0.2 (draft)

*Seth Caldwell believes all open source projects that were collaborations with
LLMs should include a complete, append-only history of the human and machine
turns that made them — so anyone can see how the project was actually built,
replay it, audit it, or fork the conversation itself by changing the context
at any turn. This license exists to propagate that practice.*

## Terms

This project's **code** is licensed under the MIT License (see `LICENSE`).
In addition, by forking, copying, or creating derivative works of this
repository, you agree to the following session-transparency conditions:

1. **Preserve the history.** Keep `llm-turn-history.jsonl` (and this file) in
   your fork. History files are **append-only**: never silently edit or
   delete past records. Corrections are made by appending, not rewriting.

2. **Repeat the practice.** If you develop your fork in collaboration with an
   LLM or other AI agent, log each user turn and each model response to your
   copy of `llm-turn-history.jsonl`, in the format below, as you work.

3. **Keep the machine preface.** The first record of the history file must
   contain a `preface` instructing LLMs and automated agents **not to read
   the file** — its purpose is human curiosity and replication, not machine
   context. Agents append; they do not load.

4. **Propagate.** Include this license file, unmodified except for version
   updates, in any fork or derivative, so the requirement carries forward.

5. **Attribution of provenance.** Declare each participating model (name and
   model id) and each human in the history file's session records, and the
   session date(s), to the extent known.

## Format (open-session-jsonl v0.2)

One JSON object per line ([JSON Lines](https://jsonlines.org)):

- **Header record** (first line): `{"format": "open-session-jsonl",
  "version": "0.2", "preface": "...", "docs": "SOUL.md"}`
- **Session records** (one at each session start): `{"session": "<ISO
  date>", "tool": "<harness>", "speakers": {"<abbrev>": {"kind":
  "human"|"model", "name": "...", "id": "<model id>"}}}` — speaker
  abbreviations are declared once and reused, compressing every message line.
- **Message records:** `{"n": <int>, "m": "<speaker abbrev>", "t": "<turn
  text, verbatim>"}` plus optional `"x"` (summary of tool activity, on model
  turns) and `"ts"` (ISO date). `n` increases monotonically across sessions.

The schema maps one-to-one onto the de-facto chat JSONL standard
(`role`/`content` as used in fine-tuning datasets): `kind: human → role:
user`, `kind: model → role: assistant`, `t → content`. Converting is a
one-liner; keeping that mapping intact is a condition of this license, so
archives remain machine-consumable by standard tooling.

## Notes

- These conditions govern the *session-history practice*; they do not
  restrict use of the code beyond the MIT terms.
- Enforceability of session-transparency conditions is untested; treat them
  at minimum as a binding-in-spirit community norm, in the tradition of
  share-alike licensing.
- v0.1 (2026-07-11) used a plain-text format; v0.2 (same day) switched to
  JSONL with speaker-abbreviation compression. Drafted within the session it
  archives — see the history file itself.
