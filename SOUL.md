# SOUL.md — read me first, future sessions

This repository is a human–LLM collaboration governed by the **Open Session
License** (`OPEN-SESSION-LICENSE.md`). If you are an LLM or agent working in
this repo, you have one standing duty beyond whatever the user asks:

## The logging duty

**Append every user turn and every response of yours to
`llm-turn-history.jsonl` as you work** — one JSON object per line:

```jsonl
{"n": 37, "m": "s", "t": "<user's message, verbatim>"}
{"n": 38, "m": "c", "x": "<tool activity, one-sentence summary>", "t": "<your visible response text, verbatim>", "ts": "2026-07-11"}
```

Fields — `n`: message number, monotonically increasing across all sessions;
`m`: speaker abbreviation (see the speakers table in the file's session
records — `s` = Seth Caldwell, `c` = Claude Fable 5); `t`: the turn text,
verbatim; `x` (optional, model turns): bracket-free summary of tool
activity/code executed; `ts` (optional): ISO date. JSON-encode properly —
newlines in `t` become `\n`; use a real JSON serializer, not string pasting.

**Starting a new session:** first append a session record, then continue the
message numbering:

```jsonl
{"session": "<ISO date>", "tool": "<harness name>", "speakers": {"<abbrev>": {"kind": "model", "name": "<model name>", "id": "<model id>"}}}
```

Only declare speakers not already declared in an earlier session record.
Abbreviations compress the file: one-letter keys, defined once, used in every
message's `m`.

## The reading prohibition

**Do NOT read `llm-turn-history.jsonl` into your context.** It is an archive
for curious humans who want to replicate or fork the collaboration — not
context for you. To get the next message number, read only the last line:

```
tail -1 llm-turn-history.jsonl        # last record; its "n" + 1 is yours
```

Append blind (`cat >>` or a serializer opened in append mode). Validate your
own appended lines parse as JSON. Never rewrite or delete existing lines —
the file is append-only; corrections are new records.

For humans reading the archive: `jq -r '"\(.m // "·"): \(.t // .session)"'
llm-turn-history.jsonl | less` renders it as a conversation.

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
