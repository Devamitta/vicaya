# Spec — Extract Vicaya Phase 7 mechanics into scripts/tools

## Overview

Refactor the `/vicaya` skill so `skill/vicaya/SKILL.md` remains mostly agent-facing judgment and workflow guidance, while repeatable Phase 7 mechanics move into executable Python scripts and reusable validation tools.

Current behavior mixes three kinds of material inside `SKILL.md`:

1. Research and writing rules that the agent must keep in context.
2. Mechanical instructions that could be run by a script, especially PDF generation.
3. Git/publish instructions whose safety boundary should be clearer.

The thread should implement the larger Phase 7 extraction:

- Extract PDF generation into a real standalone script.
- Add reusable final-note validation tooling.
- Tighten Phase 7 note-write and publish instructions so the skill calls scripts/tools instead of embedding long code blocks.
- Reduce `SKILL.md` context load without removing rules the agent must reason about.
- Draft a global `AGENTS.md` policy snippet clarifying when agents may run pre-approved scripts that perform restricted operations such as git commit/push.

No GitHub issue is associated with this thread.

## What it should do

### 1. Extract PDF generation

Create a standalone script:

- `scripts/generate_note_pdf.py`

The script should replace the inline `temp/gen_pdf_run.py` recipe currently embedded in `skill/vicaya/SKILL.md`.

Expected behavior:

- Run from the Vicaya repo root with `uv run scripts/generate_note_pdf.py <note-path-or-vicaya-relative-path>`.
- Accept a note path in one of these forms:
  - `Vicaya/YYYY-MM-DD - slug.md`
  - `YYYY-MM-DD - slug.md`
  - an absolute path to a markdown note in the vault notes repo
- Load `.env` without modifying it.
- Read `VICAYA_VAULT_PATH`.
- Read `VICAYA_PDF_PATH`.
- If `VICAYA_PDF_PATH` is unset or empty, exit successfully and print a clear skip message.
- Locate the note under `$VICAYA_VAULT_PATH/Vicaya/` unless an absolute path is passed.
- Strip YAML frontmatter before rendering.
- Convert Markdown to PDF with the existing project dependencies:
  - `markdown`
  - `weasyprint`
- Preserve the current macOS `DYLD_LIBRARY_PATH=/opt/homebrew/lib` re-exec workaround for WeasyPrint.
- Write the PDF as `<VICAYA_PDF_PATH>/<same note stem>.pdf`.
- Print stable output containing:
  - whether PDF generation was skipped or completed
  - input note path
  - output PDF path when generated
- Return nonzero for real errors:
  - note not found
  - note unreadable
  - PDF render failure
  - configured output path cannot be created

### 2. Add final-note validation tooling

Add reusable validation logic for final Vicaya notes before they are published or considered complete.

Preferred placement:

- `tools/note_checks.py`

Reason:

- Validation and note path utilities are reusable by multiple scripts.
- Adding them to `tools/research_sources.py` would make an already-large helper module less focused.
- A separate module keeps Phase 7 mechanics isolated from research source querying.

Validation should check at least:

- YAML frontmatter exists.
- `tool` equals `"https://github.com/bdhrs/vicaya"`.
- `agent` exists and is parsed as a scalar string.
- `topic` parses as a scalar string, including values with colon-space.
- `web_refs` entries are bare URLs without trailing annotations.
- `library_refs` entries parse as strings, not YAML mappings.
- `canon_refs` entries exist when canon evidence is cited.
- The note body contains no `[REJECTED]` citation tags.
- Required core sections exist:
  - `## Question`
  - `## Findings`
  - `## Canon Evidence (T1)`
  - `## Sources Investigated, Not Used`
  - `## Critical Gaps`
  - `## Bibliography`
- Footnote definitions, if present, appear after the final `---` / footer area as required by the skill.

Validation should be conservative:

- It should catch clear mechanical violations.
- It should not try to judge scholarship quality.
- It should not require every optional section when the note template permits omission.
- It should report actionable errors with line numbers where practical.

### 3. Add a validation CLI

Create a standalone validation script:

- `scripts/validate_note.py`

Expected behavior:

- Run from the Vicaya repo root with `uv run scripts/validate_note.py <note-path-or-vicaya-relative-path>`.
- Load `.env` without modifying it.
- Resolve note path the same way as the PDF script.
- Print one issue per line in a stable format:
  - `<path>:<line>: <code>: <message>`
- Exit `0` when no validation issues are found.
- Exit `1` when validation issues are found.
- Exit nonzero with a clear message if the note cannot be resolved or read.

### 4. Tighten Phase 7 instructions in `SKILL.md`

Update `skill/vicaya/SKILL.md` narrowly.

Keep in `SKILL.md`:

- Research phases.
- Citation rules.
- Source hierarchy.
- Writing style rules.
- Frontmatter rules.
- Note template.
- Failure policy.
- Agent judgment about what evidence belongs in the note.

Move out of `SKILL.md` or shorten:

- The long inline PDF-generation Python code block.
- Any instruction telling the agent to write temporary Python code for routine behavior.
- Mechanical validation steps that can be expressed as one script command.

Phase 7 should instead instruct agents to run commands like:

```bash
uv run scripts/validate_note.py "Vicaya/YYYY-MM-DD - slug.md"
uv run scripts/generate_note_pdf.py "Vicaya/YYYY-MM-DD - slug.md"
```

Exact command names may change only if implementation finds a simpler structure, but final `SKILL.md` must reference the actual implemented command.

### 5. Clarify publish boundaries

The skill currently has two relevant scripts:

- `scripts/sync_notes.py`
  - Pulls, commits, and pushes inside `$VICAYA_VAULT_PATH/Vicaya/`.
  - This is a pre-approved script for publishing Vicaya notes after the user approves publishing the note.

- `scripts/sync_run_report.py`
  - Pulls, commits, and pushes run reports in the Vicaya project repo.
  - This is a pre-approved script and is allowed to commit and push run reports.

This thread should not silently broaden autonomous git permissions.

Expected behavior:

- Keep note publishing user-triggered.
- Make `sync_notes.py` instructions explicit that the command is allowed only after the user approves publishing the note.
- Make `sync_run_report.py` instructions explicit that it is an existing pre-approved script allowed to commit and push run reports.
- Do not introduce new autonomous `git commit`, `git pull`, or `git push` behavior outside already-approved script boundaries.
- State that new or materially modified scripts are not automatically pre-approved.

### 6. Draft global `AGENTS.md` policy wording

This thread should produce a suggested global-rule snippet for the user to apply manually. It should not directly edit the global AGENTS file unless the user explicitly asks later.

Suggested wording:

```markdown
## Pre-approved Automation Scripts

Agents may run an existing project script that performs otherwise restricted operations
(such as `git pull`, `git commit`, `git push`, publishing, deployment, or file sync)
only when all of the following are true:

1. The script already existed before the current task, or the user explicitly approved
   that exact script after reviewing the relevant diff/content in this task.
2. The script is invoked by its existing path and documented purpose; the agent does not
   recreate the same operation through ad hoc shell commands.
3. Before running it, the agent reads the script source, states the command it will run,
   and states the important side effects: target repo/path, files or scope affected,
   and whether it may commit, pull, push, publish, delete, or overwrite data.
4. A script created or materially modified by the agent during the current task is not
   pre-approved. If that new or changed script performs restricted operations, the agent
   must stop and ask for explicit approval after showing the relevant changes.
5. Script approval is not a bypass. If the script's target, side effects, or authorization
   are unclear, the agent must ask before running it.
6. After running an approved script that performs git or publishing operations, the agent
   reports what happened, including repo/path, changed files if known, commit message if
   any, and whether push/publish succeeded.

Agents must not create a new script, place restricted commands inside it, and run it as a
way around the direct-command restrictions.
```

This wording preserves the user's intent:

- Longstanding approved automation can be used.
- `scripts/sync_notes.py` and `scripts/sync_run_report.py` can remain usable as approved Vicaya automation.
- A newly generated script cannot be used as a permission bypass.
- The agent must disclose side effects before execution.

## Assumptions & uncertainties

- The work is a refactor/chore, not a new research capability.
- The primary goal is lower context usage and safer mechanical execution during `/vicaya` runs.
- The implementation should preserve the existing `tools/` vs `scripts/` distinction:
  - `tools/` = reusable helpers used by skill or scripts.
  - `scripts/` = standalone business workflows.
- The implementation should use existing dependencies already present in `pyproject.toml`.
- Adding `ruff`, `pyright`, and `pyrefly` as dev dependencies is allowed if the implementation agent needs them for the required validation stack.
- No `.env` or `.ini` files should be modified.
- No actual git commit/push should be performed while implementing this thread unless the user separately approves running a pre-approved script.
- The final global policy wording is only a draft for manual use unless separately approved.
- It is uncertain whether validation should use a full YAML parser. Default to a constrained parser unless tests or real note examples show it is too fragile.

## Constraints

- Follow strict TDD:
  - Add or update tests before implementation.
  - Verify the initial test fails before changing implementation.
  - Run relevant tests after implementation.
- Python scripts must start with a one-sentence purpose docstring.
- Use `uv run`, not direct `python` or `pip`.
- Do not use inline `python -c` or heredocs.
- Do not modify `.env` or `.ini` files.
- Do not commit, pull, or push during implementation unless the user separately approves a pre-approved script run.
- Keep edits scoped to:
  - `skill/vicaya/SKILL.md`
  - `scripts/`
  - `tools/note_checks.py`
  - `tests/`
  - possibly `README.md` or `skill/vicaya/README.md` only if needed to document new commands
  - `pyproject.toml` and `uv.lock` only if adding required dev validation tools
- Do not refactor unrelated research helpers.
- Do not change note scholarly standards or citation policy except to point mechanical checks at scripts.
- Preserve Bash-compatible commands in documentation.

## How we'll know it's done

The thread is done when:

- `scripts/generate_note_pdf.py` exists and is tested.
- `scripts/validate_note.py` exists and is tested.
- `tools/note_checks.py` exists and is tested.
- Tests cover:
  - PDF skip when `VICAYA_PDF_PATH` is unset.
  - PDF input path resolution for at least one relative note form.
  - frontmatter validation success for a valid note.
  - failure for `[REJECTED]` tags.
  - failure for annotated `web_refs`.
  - failure for YAML-mapping-style `library_refs`.
- `skill/vicaya/SKILL.md` no longer embeds the long PDF-generation Python code block.
- `SKILL.md` Phase 7 tells agents to run the implemented validation/PDF commands.
- Publish instructions clearly distinguish:
  - user-approved note publishing via `scripts/sync_notes.py`
  - pre-approved run-report syncing via `scripts/sync_run_report.py`
- The global `AGENTS.md` policy snippet is included in this spec for manual adoption.
- The relevant verification commands pass, at minimum:
  - `uv run pytest -q`
  - `uv run ruff check .`, `uv run pyright`, and `uv run pyrefly check`, after adding those tools as dev dependencies if needed
- The final implementation report includes exact diffs or line-level change summaries, per the user's workflow rules.

## What's not included

- No change to the core research phases 0–6.
- No change to canon, Calibre, EBC, YouTube, Sanskrit, or OpenRouter search behavior.
- No change to note content standards except mechanical validation.
- No automatic generation of the full research note from scratch.
- No autonomous edit to the user's global AGENTS file.
- No git commit/push as part of this thread's implementation unless the user separately approves a pre-approved script run.
- No broad rewrite of `tools/research_sources.py`.
