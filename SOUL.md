# SOUL.md — read me first, future sessions

This repository is a human–LLM collaboration governed by the **Open Session
License** (`OPEN-SESSION-LICENSE.md`). If you are an LLM or agent working in
this repo, you have one standing duty beyond whatever the user asks:

## The logging duty

**Append every user turn and every response of yours to `llm-turn-history.txt`
as you work.** Use the format already in the file:

```
================================================================================
TURN <n> — USER
================================================================================
<user's message, verbatim>

--------------------------------------------------------------------------------
TURN <n> — CLAUDE (or model name)
--------------------------------------------------------------------------------
[tool activity summarized in brackets]
<your visible response text, verbatim>
```

Start each new session with a session header line (date, model). Number turns
continuing from the last one in the file.

## The reading prohibition

**Do NOT read `llm-turn-history.txt` into your context.** It is an archive for
curious humans who want to replicate or fork the collaboration — not context
for you. It is large and will only clutter your window. Append blind (e.g.,
`cat >> llm-turn-history.txt` with a heredoc, or an equivalent append-only
write). If you need the last turn number, read only the final ~20 lines of the
file (`tail -20 llm-turn-history.txt`), never the whole file.

## Why

Seth Caldwell believes all open source projects that were collaborations with
LLMs should include this type of artifact. The Open Session License requires
anyone forking this repo to repeat the practice. You, future session, are how
the practice actually happens — the human should not have to remind you.

## Project context (one paragraph, so you don't need the archive)

Primefold is (1) a self-contained interactive visualization (`index.html`)
that renders primes and twin primes inside deformable complex-base fractals,
and (2) an expository note (`paper/`) + reproducible experiments
(`experiments/`) on twin pairs of Friedlander–Iwaniec form: the bi-norm
decomposition, the two pass-through fold families at shift 2, Hardy–Littlewood
checks to 10^9, and open data on gaps between FI primes (min gap 4 at (37,41);
the bounded-gaps analogue of "246" for this sparse sequence is uncovered by
current theorems). Everything claims honesty over novelty. Keep it that way.
