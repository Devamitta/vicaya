# Spec — Human-readable canon citations

## Overview
Replace CST machine references (e.g. `s0202m_mul:97-99`) with human-readable
citations (e.g. `MN60 Apaṇṇakasuttaṃ para 97–99`) across the skill output and
the three existing vault notes. Use the `sutta_info` table in `dpd.db` as the
authoritative lookup — it maps CST file patterns to DPD abbreviation codes and
sutta names across DN, MN, SN, AN, and all KN books.

## What it should do
- `resolve_citation("s0202m_mul", "97")` → `MN60 Apaṇṇakasuttaṃ para 97`
- Commentaries: derive from mūla lookup + "a" suffix → `MNa60 para 97`
- Non-sutta codes (Abhidhamma, extra): graceful fallback to existing label
- SKILL.md citation format updated to enforce the new style
- Three vault Research notes cleaned: all `s0NNN…_mul:N` patterns replaced

## Assumptions & uncertainties
- `sutta_info` covers all sutta mūla books (DN/MN/SN/AN/KN) — confirmed
- Commentary tables (`_att`) are NOT in `sutta_info`; commentary citations
  resolved via the mūla equivalent book → prepend nikāya code + "a"
- Non-integer paranums (e.g. `_subhead`, `_upanisa`) skipped; returned as
  bare sutta reference without para number
- `VICAYA_DPD_DB` added as a new env var; citation falls back to old style if unset

## Constraints
- Vinaya coverage deferred (suttas only for now)
- `resolve_citation` API signature unchanged (book_code, paranum → Citation)
- `Citation.machine` retains the CST code for internal reference
- No new runtime dependencies

## How we'll know it's done
- `uv run tools/research_sources.py resolve-citation s0202m_mul 97` prints
  `MN60 Apaṇṇakasuttaṃ para 97`
- `uv run pytest -q` passes
- All three vault notes contain zero `s0[0-9]…_mul` patterns
