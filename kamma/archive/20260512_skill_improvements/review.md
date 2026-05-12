## Thread
- **ID:** 20260512_skill_improvements
- **Objective:** Fix SKILL.md structural corruption, relocate run reflections, add perspective mapping, recursive citation discovery, and paragraph numbering guidance

## Files Changed
- `skill/vicaya/SKILL.md` — all improvements
- `kamma/runs/` — new permanent directory; 4 reflection files moved here
- `kamma/threads/20260511_research_hub/` — deleted (defunct)

## Findings
No findings.

## Fixes Applied
- None during review

## Test Evidence
- `uv run pytest tests/ -q` → 24 passed, 0 failures
- Rules 1–10 confirmed in sequence under Hard Rules; none stranded in phase bodies
- `grep 20260511_research_hub SKILL.md` → 0 lines
- `kamma/runs/` contains 4 reflection files
- Reflection path in SKILL.md → `kamma/runs/<UTC-timestamp>.md`

## Verdict
PASSED
- Review date: 2026-05-12
- Reviewer: kamma (inline)
