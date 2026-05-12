# Plan — Human-readable canon citations

## Architecture decisions
- Lookup via `sutta_info` in `dpd.db` (not `cst_source_sutta_example.py` — that
  requires BeautifulSoup and CST XML files; `sutta_info` is pre-computed and fast)
- SQL: `WHERE cst_file LIKE '%{stem}.{type}%' AND CAST(cst_paranum AS INT) <= N
  ORDER BY CAST(cst_paranum AS INT) DESC, LENGTH(dpd_code) ASC LIMIT 1`
  — gives single-sutta entry (MN101) before book-range entry (MN101-152)
- Commentary (`_att`): remap to `_mul` for the lookup; prefix nikāya code + "a"
- cst_sutta cleaning: strip leading `^\d+\.\s+` → `"10. Apaṇṇakasuttaṃ"` → `"Apaṇṇakasuttaṃ"`
- Non-numeric paranum → bare `dpd_code sutta_name` (no para suffix)
- Graceful degradation: if `VICAYA_DPD_DB` unset or lookup fails → return old format

## Phase 1 — Config + helper

- [x] 1.1 Add `VICAYA_DPD_DB` to `.env.example`
  → verify: `grep VICAYA_DPD_DB .env.example` shows the entry

- [x] 1.2 Load `VICAYA_DPD_DB` in `research_sources.py`
  → verify: `python -c "from tools.research_sources import DEFAULT_DPD_DB; print(DEFAULT_DPD_DB)"` prints a path

- [x] 1.3 Add `_lookup_sutta_info(cst_stem, cst_type, paranum_int, db)` private helper
  → verify: calling with `("s0202m", "mul", 97, dpd_db)` returns `("MN60", "Apaṇṇakasuttaṃ")`

## Phase 2 — Rewrite resolve_citation

- [x] 2.1 Rewrite `resolve_citation` using `_lookup_sutta_info`
  → verify: `uv run tools/research_sources.py resolve-citation s0202m_mul 97` → human = `MN60 Apaṇṇakasuttaṃ para 97`
  → verify: `uv run tools/research_sources.py resolve-citation s0402m2_mul 66` → human = `AN3.65 Kesamuttisuttaṃ para 66`
  → verify: `uv run tools/research_sources.py resolve-citation s0202a_att 92` → human = `MNa60 para 92`

## Phase 3 — Update tests

- [x] 3.1 Update citation test to assert new format
  → verify: `uv run pytest tests/ -k "citation" -q` passes

## Phase 4 — Update SKILL.md

- [x] 4.1 Update citation format in SKILL.md note template
  → verify: `grep "s0[0-9].*_mul" skill/vicaya/SKILL.md` returns 0 output-format lines ✓

## Phase 5 — Vault cleanup

- [x] 5.1 Direct one-off edits to 3 existing vault notes (no subcommand needed)
  → verify: no CST codes remain in 3 Research/ notes ✓

- [x] 5.2 CST codes removed from all 3 vault notes
  → verify: rg pattern on all 3 files returns empty ✓
