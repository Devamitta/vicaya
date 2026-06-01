## Thread
- **ID:** 20260601_vicaya-skill-improvements
- **Objective:** Fix the three highest-frequency frictions surfaced by the 18 unprocessed run reflections — thematic-run gate busywork, the per-call scratch env-var tax, and a dishonest/slow Calibre health check.

## Files Changed
- `tools/research_sources.py` — `--class thematic` auto-skips Phase 2.5/3b gates; `data/scratch/.active` state file persists scratch path + auto-advancing phase; `calibre-check` probes the real search path with a fast 15s timeout; `search-calibre` returns a structured `unavailable` sentinel on lock instead of a traceback.
- `tests/test_research_sources.py` — +6 tests (thematic auto-skip, anchored-still-requires-2.5, state-file resolution, phase auto-advance, calibre-check honesty, fast-probe timeout); 2 live-Calibre tests now skip on lock rather than fail.
- `skill/vicaya/SKILL.md` — trimmed the per-call `export VICAYA_*` instructions; documented `--class thematic`, the parallel-run pin, the calibre sentinel, and the `jq`-absent caveat.
- `runs/TODO.md` — three issues moved to the Done table.

## Findings
| # | Severity | Location | What | Why | Fix |
|---|----------|----------|------|-----|-----|
| 1 | minor | `research_sources.py:_write_state` | `.active` JSON write is not atomic | Two concurrent runs can interleave and corrupt the pointer | Out of scope; parallel runs are steered to pin `VICAYA_SCRATCH` (which overrides `.active`). Documented in SKILL.md. |
| 2 | minor | `research_sources.py` search-calibre CLI | Returns a dict `{"status":"unavailable",…}` on lock vs a list normally | A JSON consumer expecting a list could trip | Exit code is 1 and SKILL.md documents the sentinel; autolog handles the dict. Accepted. |

## Fixes Applied
- During the run the user caught two regressions in the first cut (B parallel-run race, C 120s probe hang) from live runs 20260601-135900 / -150000; both were fixed before this review: B via `scratch-init` emitting the explicit pin line + SKILL.md note, C via threading a 15s `timeout` through `search_calibre`.

## Test Evidence
- `uv run -m pytest tests/` → **77 passed, 2 skipped** (the 2 skips are live-Calibre tests sitting on the desktop GUI lock — exactly the condition Fix C addresses).
- CLI smoke test: `scratch-init --class thematic` → gate 0,1,2,3 auto-skips 2.5, advances active phase over 3b to 4. Confirmed.
- Verified `.active` is gitignored, `_re` is module-level, no external `search_calibre` caller breaks on the dict sentinel.

## Verdict
PASSED
- Review date: 2026-06-01
- Reviewer: kamma (inline)
