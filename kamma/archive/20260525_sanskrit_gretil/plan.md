# Plan — Sanskrit GRETIL integration

## Architecture Decisions
1. GRETIL local corpus, grep-based. Mirrors `search_ebc` exactly. No new dependencies.
2. Returns `list[VaultHit]` — same type as `search_ebc`. No new dataclass.
3. Phase 3b in SKILL.md is conditional on angle 7 being applicable. Skipped for purely Buddhist questions.
4. `.txt` files only. Default path `~/MyFiles/2_Resources/gretil`.

---

## Phase 1 — Core implementation (research_sources.py)

- [ ] Add `DEFAULT_GRETIL_PATH` env config after `DEFAULT_EBC_VAULT_PATH`
  → verify: `python -c "from tools.research_sources import DEFAULT_GRETIL_PATH; print(type(DEFAULT_GRETIL_PATH))"` prints Path or NoneType without error

- [ ] Add `search_sanskrit(query, folder, path, limit)` — `grep -rn -F --include="*.txt"`;
  returns `[]` when path is None/absent; returns `list[VaultHit]`
  → verify: returns `[]` without raising when corpus path is None

- [ ] Add `search-sanskrit` subparser and dispatch in `_cli()`
  → verify: `uv run tools/research_sources.py search-sanskrit --help` exits 0; returns `[]` when corpus absent

## Phase 2 — SKILL.md updates

- [ ] Update angle 7: add `search-sanskrit` command, note `Path(path).stem` for text name, citation format, satisfying hit definition
  → verify: `grep -n "search-sanskrit" skill/vicaya/SKILL.md` returns ≥1 hit in the angle 7 section

- [ ] Add Phase 3b section (after Phase 3, before Phase 4a): skip condition, command, citation format, scratchpad append
  → verify: `grep -n "Phase 3b" skill/vicaya/SKILL.md` returns a hit

## Phase 3 — Config + tests

- [ ] Update `.env.example` with `VICAYA_GRETIL_PATH` and git mirror URL comment
  → verify: `grep "VICAYA_GRETIL_PATH" .env.example` returns a hit

- [ ] Add to `tests/test_research_sources.py`: `gretil_available` skip marker,
  `test_search_sanskrit_returns_empty_when_unconfigured`, `test_search_sanskrit_returns_hits`
  → verify: `uv run pytest tests/test_research_sources.py -k "sanskrit" -v` exits 0

## Phase 4 — README

- [ ] Add GRETIL/Sanskrit row to the Sources table
  → verify: `grep -i "sanskrit\|gretil" README.md` returns a hit in the Sources table

- [ ] Add GRETIL clone step (exact `git clone` command, default path, optional) to the Setup section
  → verify: `git clone` command for the GRETIL mirror appears in README.md

## Phase 5 — Full verification

- [ ] Run full test suite
  → verify: `uv run pytest tests/` exits 0 (skips allowed, no failures)
