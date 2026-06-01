# Plan — Extract Vicaya Phase 7 Mechanics Into Scripts/Tools

Repo root: `/Users/deva/Documents/dps/vicaya`

## Architecture Decisions

- Add a new focused helper module at `tools/note_checks.py`.
  - Rationale: final-note path resolution, frontmatter extraction, note validation, and frontmatter stripping are reusable by scripts but do not belong in the already-large `tools/research_sources.py`.
  - Do not move unrelated helper logic out of `tools/research_sources.py`.

- Add two standalone business scripts:
  - `scripts/validate_note.py`
  - `scripts/generate_note_pdf.py`
  - Rationale: these are Phase 7 workflows the agent should execute, not keep in context or recreate from `SKILL.md`.

- Keep validation conservative and mechanical.
  - It should detect known Vicaya note-shape failures.
  - It should not judge source quality, argument quality, or whether scholarship is complete.

- Do not add a YAML dependency unless implementation proves the constrained parser is insufficient.
  - Rationale: the validator only needs to catch known frontmatter hazards: unquoted colon-space values, annotated URLs, YAML-mapping-style library refs, missing required fields, and `[REJECTED]` tags.
  - If a full YAML parser becomes necessary, use `uv add`, update the lockfile, and document why.

- Treat both publish scripts as pre-approved automation:
  - `scripts/sync_notes.py` may commit/push inside `$VICAYA_VAULT_PATH/Vicaya/`, after user approves publishing the note.
  - `scripts/sync_run_report.py` may commit/push run reports in the Vicaya project repo.
  - New or materially modified scripts are not automatically pre-approved.

- Do not edit the user's global `AGENTS.md`.
  - The global policy wording lives in `spec.md` for manual adoption.

## Model Strategy

| Phase | Tier | Reason |
|---|---|---|
| Planning | Pro | Already done by advanced model through `/kamma-1-plan`. |
| Implementation | Fast | Mostly mechanical Python scripts, tests, and skill-doc edits. |
| Review | Pro optional | Use Pro only if validator semantics, publish safety boundaries, or `SKILL.md` reduction need deeper judgment. |

## Phase 1 — TDD Red Tests

- [x] Perform the pre-edit scope check.
  - Confirm planned edits are limited to `tools/note_checks.py`, `scripts/validate_note.py`, `scripts/generate_note_pdf.py`, tests, and narrow Phase 7 edits in `skill/vicaya/SKILL.md`.
  - Do not edit `.env`, `.ini`, unrelated research helpers, or git scripts unless a test or spec requirement forces it.
  - Inspect current user changes first.
  - → verify: run `git status --short` and record any pre-existing unrelated changes before editing.

- [x] Add failing tests for note path resolution and frontmatter/body utilities in `tests/test_note_checks.py`.
  - Create the file if it does not exist.
  - Import the planned module as `from tools import note_checks`.
  - Use `tmp_path` and `monkeypatch`; do not touch real vault files.
  - Cover:
    - `Vicaya/YYYY-MM-DD - slug.md` resolves to `$VICAYA_VAULT_PATH/Vicaya/YYYY-MM-DD - slug.md`.
    - `YYYY-MM-DD - slug.md` resolves to `$VICAYA_VAULT_PATH/Vicaya/YYYY-MM-DD - slug.md`.
    - absolute note paths are accepted unchanged.
    - YAML frontmatter is stripped from note body.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect failure because `tools.note_checks` does not exist yet.

- [x] Add failing validation tests in `tests/test_note_checks.py`.
  - Define a valid note fixture string with frontmatter and all required sections.
  - Cover:
    - valid Vicaya note returns no validation errors.
    - missing frontmatter fails.
    - `tool` not equal to `https://github.com/bdhrs/vicaya` fails.
    - unquoted `topic:` value containing `: ` fails.
    - annotated `web_refs` entry fails.
    - YAML-mapping-style `library_refs` entry fails.
    - body containing `[REJECTED]` fails.
    - required core section missing fails.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect failure before implementation.

- [x] Add failing script CLI tests in `tests/test_validate_note.py` and `tests/test_generate_note_pdf.py`.
  - Create the files if they do not exist.
  - Use `subprocess.run` with `sys.executable` only if invoking script modules directly inside pytest; otherwise use `uv run` only for manual verification commands.
  - Cover:
    - `scripts/validate_note.py` exits `0` for a valid temp note.
    - `scripts/validate_note.py` exits nonzero and prints actionable text for invalid note.
    - `scripts/generate_note_pdf.py` exits `0` with a clear skip message when `VICAYA_PDF_PATH` is unset.
    - PDF output path is derived from note stem when `VICAYA_PDF_PATH` is set; mock or monkeypatch the render function so the test does not require actual WeasyPrint rendering.
  - → verify: run `uv run pytest tests/test_validate_note.py tests/test_generate_note_pdf.py -q`; expect failure because scripts do not exist yet.

- [x] Phase 1 automatic verification.
  - → verify: run `uv run pytest tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py -q`; confirm failures are red for missing implementation, not broken test syntax.

## Phase 2 — Shared Note Utilities and Validator

- [x] Create `tools/note_checks.py`.
  - File must start with a one-sentence purpose docstring.
  - Implement these public objects:
    - `ValidationIssue`
    - `load_dotenv(path: Path) -> dict[str, str]`
    - `resolve_note_path(note_arg: str, vault_path: Path) -> Path`
    - `extract_frontmatter(text: str) -> tuple[str, str]`
    - `strip_frontmatter(text: str) -> str`
    - `validate_note_text(text: str) -> list[ValidationIssue]`
    - `validate_note_file(path: Path) -> list[ValidationIssue]`
  - `ValidationIssue` should include at least:
    - `code: str`
    - `message: str`
    - `line: int`
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect utility tests to pass or fail only on still-unimplemented validator details.

- [x] Implement `.env` loading in `tools/note_checks.py`.
  - Read simple `KEY=value` lines.
  - Ignore blank lines and lines beginning with `#`.
  - Strip one surrounding quote pair from values when present.
  - Return a dictionary; do not mutate `os.environ` from this helper unless a script chooses to merge values.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect dotenv-related tests, if added, to pass.

- [x] Implement note path resolution in `tools/note_checks.py`.
  - If `note_arg` is absolute, return that path expanded.
  - If `note_arg` starts with `Vicaya/`, resolve against `vault_path`.
  - Otherwise resolve against `vault_path / "Vicaya"`.
  - Do not require the path to exist inside `resolve_note_path`; existence checks belong in callers.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect path tests to pass.

- [x] Implement the conservative frontmatter checks in `tools/note_checks.py`.
  - Detect frontmatter only when the file starts with `---` and has a closing `---`.
  - Detect top-level scalar fields by line:
    - `tool`
    - `agent`
    - `topic`
  - Detect list fields:
    - `canon_refs`
    - `library_refs`
    - `web_refs`
  - Reject:
    - missing frontmatter fences
    - wrong `tool`
    - missing `agent`
    - unquoted scalar values containing colon-space
    - `web_refs` entries with spaces or trailing annotations after URL
    - `library_refs` list items that look like YAML mappings, e.g. `- 223: Title`
    - any `[REJECTED]` in body
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect validation tests to pass or surface only section/footnote work.

- [x] Implement required-section checks.
  - Required headings:
    - `## Question`
    - `## Findings`
    - `## Canon Evidence (T1)`
    - `## Sources Investigated, Not Used`
    - `## Critical Gaps`
    - `## Bibliography`
  - If `## Canon Evidence (T1)` contains a non-empty evidence entry, require at least one `canon_refs` list item.
  - Keep this heuristic simple; do not parse full Markdown.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect required-section tests to pass.

- [x] Implement the footnote-placement check.
  - Detect footnote definitions with a regex equivalent to `^\[\^[^\]]+\]:`.
  - If no footnotes exist, pass.
  - If footnotes exist, require them to appear after the final footer line or final horizontal rule area described by the skill.
  - Prefer a conservative rule that catches obvious early footnotes without rejecting valid notes unnecessarily.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect all note-check tests to pass.

- [x] Phase 2 automatic verification.
  - → verify: run `uv run pytest tests/test_note_checks.py -q`; expect all pass.

## Phase 3 — Phase 7 CLI Scripts

- [x] Create `scripts/validate_note.py`.
  - File must start with a one-sentence purpose docstring.
  - It should:
    - use `argparse`
    - load `.env` from repo root without modifying it
    - require `VICAYA_VAULT_PATH` for relative note paths
    - resolve the passed note path using `tools.note_checks.resolve_note_path`
    - run `tools.note_checks.validate_note_file`
    - print each issue as `path:line: code: message`
    - exit `0` when valid
    - exit `1` when invalid
    - exit nonzero with a clear message when the note path cannot be resolved or read
  - → verify: run `uv run pytest tests/test_validate_note.py -q`; expect validate-note CLI tests to pass.

- [x] Create `scripts/generate_note_pdf.py`.
  - File must start with a one-sentence purpose docstring.
  - It should:
    - use `argparse`
    - load `.env` from repo root without modifying it
    - read `VICAYA_VAULT_PATH`
    - read `VICAYA_PDF_PATH`
    - if `VICAYA_PDF_PATH` is unset or empty, exit `0` and print a stable skip message
    - resolve note path using `tools.note_checks.resolve_note_path`
    - strip frontmatter before rendering
    - render Markdown with `markdown.markdown(..., extensions=["tables", "fenced_code"])`
    - render PDF with WeasyPrint
    - preserve the macOS `/opt/homebrew/lib` `DYLD_LIBRARY_PATH` re-exec workaround
    - write `<VICAYA_PDF_PATH>/<note stem>.pdf`
    - print stable output containing input note path and output PDF path
  - → verify: run `uv run pytest tests/test_generate_note_pdf.py -q`; expect PDF script tests to pass without requiring real PDF rendering.

- [x] Run a local smoke check for the skip path.
  - Use a temp note and unset `VICAYA_PDF_PATH` for only that command.
  - Bash-compatible command pattern:
    - `env -u VICAYA_PDF_PATH uv run scripts/generate_note_pdf.py <temp-note-path>`
  - → verify: command exits `0` and prints a skip message.

- [x] Phase 3 automatic verification.
  - → verify: run `uv run pytest tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py -q`; expect all pass.

## Phase 4 — Update `SKILL.md` Phase 7 Instructions

- [x] Replace the inline PDF-generation Python block in `skill/vicaya/SKILL.md`.
  - Remove the instruction to write `temp/gen_pdf_run.py`.
  - Replace it with:
    - `uv run scripts/validate_note.py "Vicaya/${today} - ${slug}.md"`
    - `uv run scripts/generate_note_pdf.py "Vicaya/${today} - ${slug}.md"`
  - Preserve the rule that PDF generation runs after every successful vault write.
  - Preserve skip behavior when `VICAYA_PDF_PATH` is unset.
  - → verify: run `rg -n "temp/gen_pdf_run|Generate PDF for the current vicaya note|generate_note_pdf|validate_note" skill/vicaya/SKILL.md`; expect no temp script recipe and expect the new commands.

- [x] Clarify publish script permissions in `skill/vicaya/SKILL.md`.
  - Keep `scripts/sync_notes.py` user-triggered after asking whether to publish the note.
  - State that `scripts/sync_notes.py` is a pre-approved script for the notes repo only.
  - State that `scripts/sync_run_report.py` is a pre-approved script allowed to commit/push Vicaya run reports.
  - State that newly created or materially modified scripts are not automatically pre-approved.
  - → verify: run `rg -n "sync_notes.py|sync_run_report.py|pre-approved|commit|push" skill/vicaya/SKILL.md`; expect both scripts and their permission boundaries to be explicit.

- [x] Keep the note template, citation rules, style rules, and research rules unchanged except where command references need updating.
  - → verify: run `git diff -- skill/vicaya/SKILL.md` and confirm the diff is limited to Phase 7 mechanical execution and publish-boundary wording.

- [x] Phase 4 automatic verification.
  - → verify: run `uv run pytest tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py -q`; expect all pass.

## Phase 5 — Documentation and Policy Output

- [x] Decide whether `skill/vicaya/README.md` needs a short command reference update.
  - Only update it if the new scripts are user-facing enough to matter outside `SKILL.md`.
  - If updated, keep it to a short “Phase 7 utilities” section.
  - → verify: if edited, run `git diff -- skill/vicaya/README.md`; expect only the new command reference.

- [x] Preserve the global `AGENTS.md` policy wording in `kamma/threads/20260601_phase7-mechanics/spec.md`.
  - Do not edit the global AGENTS file.
  - Do not add a separate policy file unless the user asks later.
  - Final implementation report should point the user to the snippet in `spec.md`.
  - → verify: run `rg -n "Pre-approved Automation Scripts|Script approval is not a bypass|sync_run_report.py" kamma/threads/20260601_phase7-mechanics/spec.md`; expect the policy language and explicit script allowance.

- [x] Phase 5 automatic verification.
  - → verify: run `rg -n "generate_note_pdf.py|validate_note.py|sync_run_report.py" skill/vicaya/SKILL.md scripts tests`; expect references to implemented scripts and tests.

## Phase 6 — Full Validation and Final Checks

- [x] Run the Python test suite.
  - → verify: run `uv run pytest -q`; expect all pass or only documented environment skips.
  - Result: `uv run pytest -q` initially discovered unrelated `temp/test_printer.py`; pytest discovery was narrowed to `tests/`. The rerun completed with 79 passed, 11 skipped, and 2 existing Calibre integration failures in `tests/test_research_sources.py`: empty `calibredb fts_search` parse error in `test_metadata_search_by_tag`, and 120s `calibredb fts_search Buddha` timeout in `test_search_returns_calibre_hits`. Targeted Phase 7 tests passed with `uv run pytest tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py -q`.

- [x] Run the Python validation stack required by project rules.
  - First try:
    - `uv run ruff check .`
    - `uv run pyright`
    - `uv run pyrefly check`
  - If these tools are missing from the uv environment, add them as dev dependencies:
    - `uv add --dev ruff pyright pyrefly`
  - Then rerun:
    - `uv run ruff check .`
    - `uv run pyright`
    - `uv run pyrefly check`
  - It is acceptable for this task to modify `pyproject.toml` and `uv.lock` for these dev dependencies.
  - → verify: record pass/fail output for all available validation commands. If a tool cannot run because of environment/network constraints, document the exact failure.
  - Result: user installed `ruff`, `pyright`, and `pyrefly` afterward. Targeted checks on the new Phase 7 files pass:
    - `uv run ruff check tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py`
    - `uv run pyright tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py`
    - `uv run pyrefly check --search-path . tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py tests/test_note_checks.py tests/test_validate_note.py tests/test_generate_note_pdf.py`
  - Remaining non-targeted issues: full `uv run ruff check .` reports an unrelated unused `pytest` import in `tests/test_cross_check.py`; plain `uv run pyright` reports unrelated `temp/` and existing-test issues plus the same broader project state; plain `uv run pyrefly check` picks up the parent `/Users/deva/Documents/dps/pyproject.toml` and scans unrelated sibling projects unless `--search-path .` is supplied for Vicaya files.

- [x] Perform a runtime sweep for undefined names.
  - Search relevant files:
    - `tools/note_checks.py`
    - `scripts/validate_note.py`
    - `scripts/generate_note_pdf.py`
  - Use compile checks:
    - `uv run python -m py_compile tools/note_checks.py scripts/validate_note.py scripts/generate_note_pdf.py`
  - → verify: command exits `0`.

- [x] Inspect final diffs.
  - → verify: run `git diff -- tools scripts tests skill/vicaya/SKILL.md skill/vicaya/README.md pyproject.toml uv.lock`; confirm no unrelated refactors or metadata churn.

- [x] Prepare final implementation report.
  - Include:
    - files changed
    - tests run
    - validation commands run
    - exact diffs or line-level change summary
    - note that no git commit/push was performed unless the user separately requested a pre-approved script run
    - reminder that the global AGENTS snippet is in the Kamma spec for manual adoption
  - → verify: final response includes manual verification request and does not claim unsupported test success.

- [x] Phase 6 automatic verification.
  - → verify: run `uv run pytest -q`; expect all pass or documented skips/failures.
