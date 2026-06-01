## Thread
- **ID:** 20260601_phase7-mechanics
- **Objective:** Extract Vicaya Phase 7 mechanics into scripts/tools.

## Files Changed
- `pyproject.toml` — adds dev validation tools and pytest discovery config.
- `uv.lock` — locks added dev validation tools.
- `skill/vicaya/SKILL.md` — replaces inline Phase 7 PDF code with script commands and clarifies publish boundaries.
- `skill/vicaya/README.md` — documents Phase 7 utility commands.
- `tools/note_checks.py` — adds note path, frontmatter, and final-note validation helpers.
- `scripts/validate_note.py` — adds final-note validation CLI.
- `scripts/generate_note_pdf.py` — adds final-note PDF generation CLI.
- `tests/test_note_checks.py` — covers note utilities and validation rules.
- `tests/test_validate_note.py` — covers validation script behavior.
- `tests/test_generate_note_pdf.py` — covers PDF generation script behavior.

## Findings
| # | Severity | Location | What | Why | Fix |
|---|----------|----------|------|-----|-----|
| 1 | major | `tools/note_checks.py:135` | Quoted `library_refs` containing `: ` were rejected as YAML mappings. | Valid YAML scalar strings such as `"Author: Title"` would be blocked, violating the spec's scalar-string rule. | Added regression coverage and changed the mapping check to reject only unquoted `key: value` list entries. |

## Fixes Applied
- Added `test_quoted_library_ref_with_colon_space_is_valid` in `tests/test_note_checks.py`.
- Updated `tools/note_checks.py` to preserve quoted `library_refs` with colon-space.
- Moved `ruff`, `pyright`, and `pyrefly` from runtime dependencies to the `dev` dependency group in `pyproject.toml` and matching `uv.lock` metadata.

## Test Evidence
- `uv run pytest tests/test_note_checks.py -q` → pass.
- `uv run pytest tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py -q` → pass, 22 passed.
- `uv run pytest -q` → fail, 80 passed / 11 skipped / 2 failed in existing Calibre integration tests: empty `calibredb fts_search` parse error and `Buddha` FTS timeout.
- `uv run ruff check tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py` → pass.
- `uv run pyright tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py` → pass.
- `uv run pyrefly check --search-path . tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py` → pass.
- `uv run python -m py_compile tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py` → pass.
- `env UV_CACHE_DIR=.uv-cache VICAYA_PDF_PATH= uv run scripts/generate_note_pdf.py "Vicaya/2099-01-01 - missing.md"` → pass, skip message printed; temporary cache removed.
- `uv run ruff check .` → fail on existing unused `pytest` import in `tests/test_cross_check.py`.
- `uv run pyright` → fail on existing `temp/` and test issues outside Phase 7.
- `uv run pyrefly check` → fail after scanning parent `/Users/deva/Documents/dps` tree; targeted Phase 7 check passes.
- `env UV_CACHE_DIR=.uv-cache uv lock --check` → pass; default uv cache path is sandbox-blocked.
- `coderabbit review --agent` → pass, limited/free CLI mode, `findings: 0`.

## Verdict
PASSED
- Review date: 2026-06-01
- Reviewer: Codex
