## Architecture Decisions
- Use pandoc (MD→HTML5, standalone) + google-chrome headless (HTML→PDF) pipeline.
  LaTeX is not installed; wkhtmltopdf is not installed; Chrome is confirmed available.
- PDF generation is added as agent instructions in SKILL.md Phase 7, not as a Python helper,
  because the writing step is already an agent-executed shell command (obsidian CLI).
- `VICAYA_PDF_PATH` is read from the environment, same pattern as all other paths.
- If the env var is unset, the step is skipped — no error, no orphaned temp files.

## Phase 1 — Add env var to .env.example

- [x] Add `VICAYA_PDF_PATH=~/Obsidian/Research/PDF` to `.env.example` with a comment.
  → verify: `.env.example` contains the new variable. ✓

## Phase 2 — Add PDF generation step to SKILL.md

- [x] In Phase 7 of SKILL.md, after the `obsidian vault=... create` block, added a PDF
  generation block using pandoc (MD→HTML5) + google-chrome headless (HTML→PDF).
  Skips silently if `VICAYA_PDF_PATH` unset; logs warning on failure.
  → verify: instructions appear in SKILL.md after vault write block. ✓

## Phase 3 — Verification

- [x] Ran the pipeline against an existing vault note (fourth-jhana-no-breathing).
  → verify: PDF appeared at target path (248K). ✓

## Phase 4 — Bulk backfill (added per user request)

- [x] Converted all 22 Research/*.md notes to PDF, overwriting existing ones.
  → verify: 22/22 succeeded, 0 failed. 24 total PDFs in output dir. ✓
