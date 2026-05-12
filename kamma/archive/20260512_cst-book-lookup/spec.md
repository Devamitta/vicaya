# Expose CST book translator as a vicaya CLI subcommand

## Overview
Make dpd-db's `cst_book_translator.py` available to the vicaya skill via a new
CLI subcommand on `tools/research_sources.py`. The skill gets a tool it can
reach for when it needs to translate any CST book identifier into the others —
useful when staring at an unfamiliar code, or when a user mentions a book by
human name and the agent needs the SQLite table code.

Existing citation format (DN12, MN32, SN12.3, AN5.4 + sutta name) is preserved.
`resolve_citation` is not touched. The embedded book-code map in SKILL.md is
not touched.

## What it should do
- A new subcommand: `uv run tools/research_sources.py lookup-book <value>`
- Accepts any of: cst_filename (`s0101m.mul`), vicaya SQLite-table form
  (`s0101m_mul`), cst_book_name (`Dīghanikāya, Sīlakkhandhavaggapāḷi`),
  gui_book_code (`dn1`), dpd_book_code (`DN` / `DNa`).
- Auto-detects the identifier type. Prints JSON list of matching records:
  `{cst_filename, cst_table, cst_book_name, gui_book_code, dpd_book_code}`.
  (`cst_table` = vicaya's underscore form, derived from `cst_filename`.)
- Returns empty list `[]` (exit 0) on no match — never crashes.
- Loads the translator live from sibling `../dpd-db/tools/cst_book_translator.py`
  via sys.path shim. If dpd-db isn't a sibling, the subcommand prints a clear
  error message naming the expected path and exits non-zero.

## Assumptions & uncertainties
- dpd-db lives at a sibling path relative to vicaya. SKILL.md already
  documents this assumption for `pali_text_files.py`, so it's an established
  pattern.
- The translator's `cst_filename` (dot) ↔ vicaya's table name (underscore)
  conversion is a simple `.` → `_` swap, no semantic difference.
  **Verified 2026-05-12:** canon SQLite DB has 217 tables in underscore form;
  translator TSV has 217 rows in dot form; same set. The dot form mirrors the
  source XML filename stem (e.g. `romn/s0101m.mul.xml`); SQL table identifiers
  can't contain dots, hence the underscore form in the vicaya DB.
- The translator's `translate()` already does auto-detection — we just wrap it.

## Constraints
- No changes to `resolve_citation` or any citation format.
- No changes to the embedded book-code tables in SKILL.md.
- No vendoring; live import from sibling dpd-db.
- No new runtime dependencies in `pyproject.toml`.

## How we'll know it's done
- `uv run tools/research_sources.py lookup-book s0101m_mul` returns the DN
  Sīlakkhandhavaggapāḷi record as JSON.
- `lookup-book DN` returns all 3 DN mūla books.
- `lookup-book dn1` returns 1 record.
- `lookup-book bogus` returns `[]` and exits 0.
- A new test in `tests/` covers all four input forms plus the underscore-form.
- SKILL.md has one paragraph under "Calling the helpers" telling agents this
  subcommand exists and when to use it.

## What's not included
- No vendored TSV.
- No changes to citation output or `Citation` dataclass.
- No changes to the SKILL.md book-code map.
- No CLI subcommand to list all books.
