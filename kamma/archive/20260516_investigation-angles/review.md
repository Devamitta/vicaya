## Thread
- **ID:** 20260516_investigation-angles
- **Objective:** Add a standing 15-angle investigation checklist to the vicaya skill so every research run systematically considers each evidentiary lens.

## Files Changed
- `skill/vicaya/SKILL.md` — added `## Investigation angles` section (intro + triage rule + 15 angles in 5 groups); wired Phase 1 to run angle triage first; extended scratchpad block, Phase 5 source-completeness check, Phase 7 pre-write checklist, and Phase 7 note template (new `## Angles Not Pursued` table).

## Findings
No findings.

Reviewed across the five axes:
- **Correctness**: every spec requirement landed. 15 angles present, all 5 groups covered, triage step wired into Phase 1, scratchpad and template updated.
- **Readability**: angles follow consistent structure (*Applies to* / *Where to search* / *Satisfying hit*); section flows cleanly between "## The seven phases" intro and "### Phase 1".
- **Architecture**: single file edit, no new helper, no new phase. Triage absorbed into existing Phase 1.
- **Security**: N/A (markdown doc).
- **Performance**: N/A.

## Fixes Applied
None.

## Test Evidence
- `rg -n "^## Investigation angles" skill/vicaya/SKILL.md` → 1 hit at line 151
- `rg -n "^### Phase 1" skill/vicaya/SKILL.md` → line 372 (after the new section, as required)
- `rg -n "Investigation angles|Angles Not Pursued|angle triage|angle coverage"` → all cross-references resolve; no orphans
- Section ordering (`rg -n "^## |^### Phase"`) — clean: "## The seven phases" → "## Investigation angles" → "### Phase 1" → ... → "## Sources Investigated, Not Used" → "## Angles Not Pursued" → "## Critical Gaps"
- User confirmation after live test: "Yeah, it looks cool"

## Verdict
PASSED
- Review date: 2026-05-16
- Reviewer: kamma (inline)
