## Thread
- **ID:** 20260512_human_citations
- **Objective:** Replace CST machine codes with DPD human-readable sutta citations across skill, tests, SKILL.md, and vault notes

## Files Changed
- `tools/research_sources.py` — added `DEFAULT_DPD_DB`, `_book_code_parts`, `_lookup_sutta_info`, `_fallback_human`; rewrote `resolve_citation`
- `tests/test_research_sources.py` — split into `TestResolveCitation` (fallback) and `TestResolveCitationWithDPD` (DPD-backed)
- `.env.example` — added `VICAYA_DPD_DB` entry
- `.env` — set `VICAYA_DPD_DB` to local dpd.db path
- `skill/vicaya/SKILL.md` — updated all citation format examples to new style
- `Obsidian/Research/2026-05-12 - rebirth-wager-apannaka-mn60.md` — all CST codes replaced
- `Obsidian/Research/2026-05-11 - paticcasamuppada-interpretations-across-traditions.md` — all CST codes replaced
- `Obsidian/Research/2026-05-11 - arahant-and-unexperienced-kamma-at-parinibbana.md` — all CST codes replaced

## Findings
No findings.

## Fixes Applied
- `text_type` field was returning raw `"mul"` from DPD path vs `"mūla"` from fallback path — fixed by applying `_TEXT_TYPE_LABELS` mapping before all Citation returns.

## Test Evidence
- `uv run pytest tests/ -k "citation" -q` → 12 passed (including 5 DPD-backed), 0 failures
- `uv run tools/research_sources.py resolve-citation s0202m_mul 97` → `MN60 Apaṇṇakasuttaṃ para 97` ✓
- `uv run tools/research_sources.py resolve-citation s0202a_att 92` → `MNa60 para 92` ✓
- `uv run tools/research_sources.py resolve-citation s0402m2_mul 66` → `AN3.66 Kesamuttisuttaṃ para 66` ✓
- `rg 's0[0-9][0-9][0-9].*_[a-z]+' Research/` → 0 matches ✓

## Verdict
PASSED
- Review date: 2026-05-12
- Reviewer: kamma (inline)
