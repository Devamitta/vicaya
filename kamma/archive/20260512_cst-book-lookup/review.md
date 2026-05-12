## Thread
- **ID:** 20260512_cst-book-lookup
- **Objective:** Expose dpd-db's `cst_book_translator` to the vicaya skill via a new `lookup-book` CLI subcommand. No changes to citation format or the embedded book-code map.

## Files Changed
- `tools/research_sources.py` — added `_load_cst_translator()`, `lookup_book()`, and `lookup-book` argparse subcommand
- `tests/test_research_sources.py` — added `cst_translator_available` skip marker and `TestLookupBook` (7 tests)
- `skill/vicaya/SKILL.md` — added helper-table row and "Book-identifier lookups" usage subsection

## Findings
| # | Severity | Location | What | Why | Fix |
|---|----------|----------|------|-----|-----|
| 1 | minor | `tools/research_sources.py` ~795 | Dead `_dpd_tools_paths_stub` block left over from an earlier approach | Confuses future readers; never referenced | Removed |
| 2 | nit | `tools/research_sources.py` ~879 | Unused `sep` variable from `rpartition` | Lint noise | Renamed to `_` |

No blocking or major findings.

## Fixes Applied
- Removed the dead stub block.
- Replaced unused `sep` with `_`.

## Test Evidence
- `uv run pytest tests/test_research_sources.py::TestLookupBook -q` → 7 passed
- `uv run pytest -q` (full suite, includes integration) → 31 passed
- `uv run tools/research_sources.py lookup-book s0101m_mul` → 1 hit, dot/underscore both populated
- `uv run tools/research_sources.py lookup-book DN` → 3 hits (all DN mūla volumes)
- `uv run tools/research_sources.py lookup-book dn1` → 1 hit
- `uv run tools/research_sources.py lookup-book "Dīghanikāya, Sīlakkhandhavaggapāḷi"` → 1 hit
- `uv run tools/research_sources.py lookup-book bogus` → `[]`, exit 0

## Verdict
PASSED
- Review date: 2026-05-12
- Reviewer: kamma (inline)
