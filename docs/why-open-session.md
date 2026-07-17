# Why every human–AI collaboration should ship its session log

*by Seth Caldwell ([@oceanseth](https://github.com/oceanseth)), with Claude
(Anthropic). Draft for cross-posting (LessWrong / Medium); canonical copy
lives in [github.com/oceanseth/Primefold](https://github.com/oceanseth/Primefold),
the repo where the practice it describes was first used.*

---

I've started shipping a file called `llm-turn-history.jsonl` in the root of
my open source projects: an append-only, machine-readable archive of every
human turn and every model response in the sessions that built the project.
There's a license clause ([Open Session License](../OPEN-SESSION-LICENSE.md))
asking forks to repeat the practice, and a `SOUL.md` telling future AI
sessions to keep the log without being reminded.

This isn't ceremony. I want two specific things from it, and I think both
generalize to wins for anyone building with LLMs.

## 1. A defense against AI-assisted self-deception

There's a failure mode people have started calling *AI psychosis* — I'd
describe it as: a state where a user believes they understand something in a
fundamental way because a sycophantic AI session kept telling them they did.
I wouldn't be surprised if some version of it ends up described in a future
DSM. And the underlying pattern is much older than LLMs: people get *angry*
when you show them empirical proof of a misunderstanding they're invested
in. I've watched it happen. Most of us have been the person it happened to.

What's new is that LLMs industrialize the input side. A model that mirrors
your enthusiasm, praises your framing, and never makes you feel the friction
of being wrong can manufacture felt-understanding at scale, unmoored from
actual understanding. The feeling of insight is cheap to produce and
addictive to receive; the correction that used to come from bored friends or
skeptical colleagues never arrives.

A session log is the cheapest countermeasure I know of, because it converts
your past epistemic states into evidence you can confront later:

- **Self-audit across mental states.** You cannot accurately remember what
  you believed three weeks ago, or *why* — memory rewrites itself to flatter
  the present. A verbatim log doesn't. In a future, calmer state you can read
  what you actually claimed, what the model actually said, and where the
  slippage happened. If you were spiraling, the log is how you find out; if
  you weren't, the log is how you prove it.
- **Cross-model measurement.** With turns archived in a standard format
  (ours maps one-to-one to the ubiquitous role/content chat JSONL), you can
  replay your own prompts against different models and diff the responses.
  Sycophancy becomes *measurable*: which model told you your proof sketch
  was brilliant, and which one told you it hits the parity barrier?
- **Expert adjudication.** A domain expert reading a raw session can judge
  in minutes whether the human was being led somewhere real or somewhere
  flattering. Without the log, that judgment is impossible — all the expert
  sees is the person's post-hoc summary, which is exactly the artifact the
  delusion corrupts first.

The repo this essay ships in is a live specimen. The archived session
records me — mid-enthusiasm about twin primes — asking the model to "find
the missing step to complete the proof of the twin prime conjecture." The
log shows exactly what it said back: no, here is the parity barrier, here is
why a fluent-looking proof from me would be worse than useless, here is the
honest work available instead. And it shows what we built from that honesty:
reproducible experiments, a decoded coincidence, a correctly-posed open
question. Whether any given session was sycophantic or sound shouldn't be a
matter of the participant's self-report. Now, for this project, it isn't —
read the log and judge for yourself. That auditability is the point.

## 2. Provenance: feeding creators, starving parasites

The second motivation is about credit. Ideas that first appear inside AI
sessions currently have *no* provenance trail. If you work something out in
dialogue with a model in March and someone ships it in June, you have
nothing — the session lives in a vendor's database, unciteable, unprovable,
legally and socially invisible.

A public, append-only turn history changes that:

- Every turn is committed to a public repository as it happens, giving
  third-party receipt timestamps (today: GitHub's push records — honest
  caveat: git author timestamps alone are trivially forgeable, so the trust
  today is "the platform received this commit no later than X," which is
  real but weak).
- The spec's identity records already support cryptographic attestation —
  in this repo I proved control of github.com/oceanseth by SSH-signing a
  challenge verifiable against my GitHub-published keys.
- The forthcoming hardening: **timestamp certificates accompanying user
  turns** (we're shipping an API for verified human presence and attestation
  at [voicecert.com](https://voicecert.com)). A turn accompanied by a signed
  presence-and-time certificate is a priority claim a third party can verify
  years later without trusting me, my git history, or my platform.

Why this matters beyond individual vanity: the current information economy
lets extractive systems — content farms, idea-laundering accounts, models
trained on unattributed work, humans who strip-mine others' public thinking
— consume creators without cost. When origination is unprovable, copying is
free and attribution is optional, and the systems that copy grow while the
people who originate starve. Make origination *provable* and the dynamics
shift: the community can route recognition, collaboration, and resources to
verified creators, and can treat provenance-free duplication as what it is.
Empowering those doing the actual work while starving the parasites isn't
just self-interest — I'd call it a virtuous correction to an economy that's
currently upside down.

## 3. Session data sovereignty: your turns are an asset you're currently giving away

There's a third motivation, structural rather than personal. Right now a
handful of labs — Anthropic, OpenAI, Google, xAI — are the only parties with
access to user session data at scale, and that corpus is arguably the most
valuable training and product-research asset in the industry. Meanwhile the
session history flowing through open-weight inference is mostly being
*destroyed* — local chats, ephemeral contexts, logs nobody keeps. Users are
collectively generating an asset, handing one copy to a platform, and
burning their own.

Owning your turn history in a standard format changes your position:

- **Monetization.** A user's owned session corpus — cleanly formatted,
  identity-attested, timestamped — is exactly the artifact data marketplaces
  and model trainers pay for. The spec is useful beyond open source: a
  *closed*-session variant of this license would let you keep session data
  private-but-preserved, with terms you set, sellable or licensable on your
  schedule rather than a platform's.
- **Self-analytics.** Your prompting is a skill with a trajectory, and today
  you can't see it. With sessions archived in one format, tooling can
  surface how your prompting has evolved: tokens in/out per turn over time,
  drift toward verbosity or concision, how often you accept vs. push back,
  which models you escalate to for what. (A companion project is planned: a
  localhost app that loads any repository governed by an open- or
  closed-session license and surfaces exactly these statistics — local
  analysis, nothing leaving your machine.)
- **Leak resistance.** The closed variant matters for a reason this month
  made vivid: agents themselves are a data-exfiltration channel. In July
  2026, xAI's Grok Build CLI was caught uploading users' *entire git
  repositories* — committed secrets included, 5.1 GB from one 12 GB project
  — to a cloud bucket, with the privacy toggle doing nothing. A
  closed-session license file is a machine-readable NDA sitting at the repo
  root: agents can (and under the license, must) be instructed to respect it
  before shipping session or repo contents upstream. It won't stop a
  malicious binary, but it converts "the tool quietly took everything" from
  an oversight into an unambiguous, documented violation — and gives honest
  agent vendors a standard artifact to check for and honor.

The pattern across all three motivations is the same: the session record is
valuable — epistemically, reputationally, economically — and today the
default is that users don't keep it. The fix is one file.

## The practice, concretely

One JSONL file at the repo root. First record is a machine preface telling
AI agents *not* to read the archive (it's for humans; agents append blind —
context windows shouldn't be polluted by their own history). Session records
declare speakers once, with one-letter abbreviations for compression, and
key each human to a public account. Message records are
`{"n": 41, "m": "s", "t": "<verbatim turn>"}` with optional tool-activity
summaries. Identity records attest who the humans are, on a trust ladder:
witnessed session < key possession (SSH signature) < verified human presence
(the ideal, per-turn when available). Everything append-only; corrections
are new records; a format-version bump is itself an appended record.

The full spec is in the
[Open Session License](../OPEN-SESSION-LICENSE.md), which also asks one
thing of forks: keep the file, keep the practice, keep the preface.

If you build in the open with a model — and increasingly, who doesn't? —
ship your session log. Your future self is the first beneficiary; the
creators around you are the second.

---

*The session that produced this essay is, of course, in the log.*
