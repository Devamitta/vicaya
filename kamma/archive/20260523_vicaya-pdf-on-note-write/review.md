## Thread
- **ID:** 20260523_vicaya-pdf-on-note-write
- **Objective:** Auto-generate a PDF copy of every research note written by the vicaya skill

## Files Changed
- `.env.example` — added `VICAYA_PDF_PATH` variable with comment
- `pyproject.toml` — added `weasyprint` and `markdown` dependencies
- `skill/vicaya/SKILL.md` — added PDF generation block to Phase 7
- `uv.lock` — updated by uv

## Findings
No findings.

## Fixes Applied
- Replaced pandoc+Chrome pipeline (headers/footers could not be suppressed in Chrome 147) with weasyprint — simpler, no external renderer needed.

## Test Evidence
- `uv run python3 <weasyprint script>` on all 22 Research/*.md → 22/22 converted, 0 failed
- `pdftotext` on output → no headers, no footers, Pāḷi diacritics intact

## Verdict
PASSED
- Review date: 2026-05-23
- Reviewer: kamma (inline)
