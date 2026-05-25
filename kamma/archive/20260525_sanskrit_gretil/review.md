## Thread
- **ID:** 20260525_sanskrit_gretil
- **Objective:** Add Sanskrit primary-source search via local GRETIL corpus

## Files Changed
- `tools/research_sources.py` — added `DEFAULT_GRETIL_PATH`, `search_sanskrit()`, `search-sanskrit` CLI subcommand
- `skill/vicaya/SKILL.md` — updated angle 7; added Phase 3b with subfolder map and citation rules
- `.env.example` — added `VICAYA_GRETIL_PATH` with git clone instruction
- `tests/test_research_sources.py` — added `gretil_available` marker, two Sanskrit tests
- `README.md` — added Sanskrit/GRETIL row to Sources table; GRETIL clone step in Setup; agent setup section

## Findings
No findings.

## Fixes Applied
- Updated `--include` from `*.txt` to `*.htm` after discovering the GRETIL mirror uses `.htm` files, not plain `.txt`. Docstring, SKILL.md, and test assertion updated to match.

## Test Evidence
- `uv run pytest tests/ -q` → 47 passed in 151s
- `uv run tools/research_sources.py search-sanskrit "ātman" --limit 3` → returns VaultHit JSON from corpus
- `uv run tools/research_sources.py search-sanskrit "test" --limit 3` (corpus absent path) → `[]`

## Verdict
PASSED
- Review date: 2026-05-25
- Reviewer: kamma (inline)
