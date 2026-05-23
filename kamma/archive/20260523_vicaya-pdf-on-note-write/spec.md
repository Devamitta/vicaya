## Overview
Every time the vicaya skill writes or updates a vault research note, it should also
generate a PDF copy and save it to a configured output directory. This makes notes
portable and printable without requiring Obsidian to be open.

## What it should do
- After writing a vault note (Phase 7), generate a PDF of the same note.
- PDF filename matches the note: `YYYY-MM-DD - <slug>.pdf`
- PDF path comes from a new env var `VICAYA_PDF_PATH`.
- This also applies to the fallback path (writing directly to disk when Obsidian isn't running).
- If PDF generation fails, log the failure in the terminal report and continue — don't abort.

## Assumptions & uncertainties
- PDF generation tool: pandoc (MD→HTML) + google-chrome headless (HTML→PDF).
  Both confirmed available on this machine. LaTeX/wkhtmltopdf are not installed.
- `VICAYA_PDF_PATH` will be added to `.env.example`. The user's actual `.env` already
  has (or will have) this set to `/home/bodhirasa/MyFiles/Obsidian/Research/PDF`.
- "Updated" means: any run that writes the note file, whether it creates or overwrites.
  The PDF will always be regenerated to stay in sync.
- The existing 17 PDFs in the target directory were produced outside this skill; this
  thread adds the generation step to the skill itself going forward.

## Constraints
- Changes are limited to: `skill/vicaya/SKILL.md` and `.env.example`.
- No Python helper changes needed.
- Pāḷi diacritics must survive the pipeline (confirmed: Chrome headless handles UTF-8).
- If `VICAYA_PDF_PATH` is not set, skip PDF generation silently (don't error).

## How we'll know it's done
- SKILL.md Phase 7 includes a PDF generation block after vault write.
- `.env.example` has `VICAYA_PDF_PATH=~/Obsidian/Research/PDF`.
- Manual test: run the pipeline against a sample note and confirm a PDF appears.

## What's not included
- Retroactive PDF generation for existing notes.
- A standalone script for batch conversion.
- Any changes to research_sources.py or the helper CLI.
