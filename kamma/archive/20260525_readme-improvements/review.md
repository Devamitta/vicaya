## Thread
- **ID:** 20260525_readme-improvements
- **Objective:** Close issues #1 (already fixed) and #3 (README improvements for Calibre FTS and Obsidian CLI)

## Files Changed
- `README.md` — added `### Calibre full-text search` and `### Obsidian CLI` subsections; added `### Runtime requirements` block in agent setup
- `skill/vicaya/README.md` — expanded Calibre FTS bullet in Known limitations with FT button steps

## Findings
No findings.

## Fixes Applied
None — no issues found.

## Test Evidence
- `grep -n "FT button" README.md` → match at line 160 ✓
- `grep -n "obsidian version" README.md` → match at line 100 ✓
- `grep -n "Runtime requirements" README.md` → match at line 148 ✓
- `grep -n "walk them through" README.md` → match at line 160 ✓
- `grep -n "FT button" skill/vicaya/README.md` → match at lines 72, 77 ✓
- `gh issue view 1` → CLOSED ✓
- `gh issue view 3` → CLOSED ✓

## Verdict
PASSED
- Review date: 2026-05-25
- Reviewer: kamma (inline)
