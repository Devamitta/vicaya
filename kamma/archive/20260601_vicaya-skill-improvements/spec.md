# Spec — vicaya skill improvements (3 from unprocessed runs)

## Overview
Three recurring frictions surfaced across the 18 unprocessed run reflections in
`runs/` (the 80 in `runs/processed/` are already digested in `runs/TODO.md`).
Fix all three in `tools/research_sources.py` + minimal `SKILL.md` doc updates.
Constraint from user: simplest, most elegant solution; prefer deleting lines;
no over-engineering.

## What it should do

**A — Thematic auto-skip (5 runs: metta, sila-caritta, silabbataparamasa,
anatta-free-will, pali-path-terms).** Non-sutta-anchored runs currently must run
empty `sc-parallels` and hand-log skip reasons just to get past the Phase 2.5
and 3b gates. Add a run class set at `scratch-init --class thematic`; for a
thematic run, `scratch_gate` auto-writes the 2.5 and 3b skip gates so the agent
never does that busywork.

**B — Scratch state file (3 runs: craving-tension, metta, jhana-training).**
The shell loses env between Bash calls, forcing `VICAYA_SCRATCH`/`VICAYA_PHASE`
to be re-exported on every helper invocation. Persist an active-state file
(`data/scratch/.active`) at `scratch-init`; `scratch_gate` advances the phase
automatically. Resolution order stays: env override → state file → slug.

**C — Honest calibre-check + graceful search-calibre (3 runs: abhibhayatana,
anatta-free-will, sannavedayitanirodha).** `calibre-check` runs a cheap `list`
probe that reports "ok" while the real FTS `search-calibre` dies with an
uncaught `CalibreUnavailable` traceback under a GUI lock. Make `calibre-check`
exercise the real `search_calibre` path so its verdict matches reality, and have
the `search-calibre` CLI catch `CalibreUnavailable` and emit a structured
`{"status": "unavailable", ...}` sentinel (exit 1) instead of a traceback.

## Assumptions & uncertainties
- `_re` and `json` are already imported module-wide (verified).
- Existing scratch files lack a `Run class:` line → default `sutta-anchored` →
  no behaviour change (backward compatible).
- Explicit env vars must still win over the state file (backward compatible).
- Calibre is not reachable in CI; calibre tests are function-level with mocks.

## Constraints
- Touch only `tools/research_sources.py`, `tests/test_research_sources.py`,
  `skill/vicaya/SKILL.md`. Do not modify `.env`/`.ini`.
- Behaviour-preserving for sutta-anchored runs.

## How we'll know it's done
- `uv run -m pytest` green.
- New tests: thematic run auto-skips 2.5/3b; state file resolves scratch path
  without env; `calibre_library_available` agrees with `search_calibre`.
- The three issues marked addressed in `runs/TODO.md`.

## What's not included
- Suttanipāta verse-citation resolution, scratch-log sub-phase keys, Vinaya-first
  triage, and other lower-frequency items remain in TODO.
