# Plan — Expose CST book translator as vicaya CLI subcommand

## Architecture Decisions
- **Live import from sibling dpd-db** via sys.path shim resolving
  `../dpd-db/tools/cst_book_translator.py` relative to vicaya repo root.
  Matches the existing pattern for `pali_text_files.py`.
- **Wrap, don't reimplement.** Call `translate()` from the translator directly;
  add the dot↔underscore adapter on the way out.
- **JSON-list output**, mirroring other subcommands. Empty list on no match,
  exit 0.
- **One derived field**, `cst_table`, from `cst_filename` by swapping `.` → `_`.

## Phase 1 — Implement the subcommand

- [ ] Add `_load_cst_translator()` helper in `tools/research_sources.py` that
      resolves sibling `dpd-db/tools/`, appends to `sys.path` if needed, imports
      `cst_book_translator`, caches the module, raises a clear `RuntimeError`
      naming the expected path if import fails.
      → verify: `uv run python -c "from tools.research_sources import _load_cst_translator; print(_load_cst_translator().translate('DN')[:1])"` prints one BookInfo.

- [ ] Add `lookup_book(value: str) -> list[dict]` that normalises underscore
      input (`s0101m_mul` → `s0101m.mul`), delegates to `translate()`, and
      serialises each `BookInfo` to a dict with `cst_filename`, `cst_table`,
      `cst_book_name`, `gui_book_code`, `dpd_book_code`.
      → verify: `uv run python -c "from tools.research_sources import lookup_book; import json; print(json.dumps(lookup_book('s0101m_mul'), ensure_ascii=False))"` prints a 1-element list with both filename and table fields populated.

- [ ] Wire `lookup-book` subcommand into the argparse CLI. Single positional
      `value`. Calls `lookup_book`, prints `_dump(result)`.
      → verify: `uv run tools/research_sources.py lookup-book DN` prints a JSON array of 3 DN mūla books.

- [ ] Phase 1 automatic verification.
      → verify: run all six invocations:
      - `lookup-book s0101m_mul` → 1 hit, contains "Sīlakkhandha"
      - `lookup-book s0101m.mul` → 1 hit (same)
      - `lookup-book "Dīghanikāya, Sīlakkhandhavaggapāḷi"` → 1 hit
      - `lookup-book dn1` → 1 hit
      - `lookup-book DN` → 3 hits, dpd_book_code = "DN"
      - `lookup-book bogus` → `[]`, exit 0

## Phase 2 — Test coverage

- [ ] Add tests in `tests/test_research_sources.py` (or new file if cleaner)
      covering each input form, underscore variant, empty-result case, and
      that result dict has all five expected keys.
      → verify: `uv run pytest -q -k lookup_book` all pass.

- [ ] Phase 2 automatic verification.
      → verify: `uv run pytest -q` — full suite passes.

## Phase 3 — Document in SKILL.md

- [ ] Add a row for `lookup-book` to the "Calling the helpers" table.
      → verify: re-read SKILL.md, confirm row present and concise.

- [ ] Add a short subsection (~6 lines) after helper-return-shapes describing
      when to use it, with one example invocation.
      → verify: re-read the section, confirm sufficient for an agent.

- [ ] Phase 3 automatic verification.
      → verify: grep `lookup-book` in SKILL.md returns ≥2 hits; full pytest still passes.
