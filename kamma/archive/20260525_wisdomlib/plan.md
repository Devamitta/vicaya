# Plan — WisdomLib integration

## Architecture Decisions
- Add as Phase 4c (between YouTube 4b and Synthesis Phase 5). Rationale: WisdomLib
  is mandatory every run, so it deserves a named phase boundary agents can confirm.
  Folding it into 4a would bury the requirement and make it easy to skip.
- No new helper — WebFetch on `/definition/<term>` is sufficient.
- Evidence tier T2 by default (encyclopaedic secondary); upgrade to T1 only when
  the entry quotes a primary canon text verbatim.
- Citation form: `[wisdomlib.org — <Term>](https://www.wisdomlib.org/definition/<term>) — retrieved YYYY-MM-DD`

## Phase 1 — Verify URL structure [DONE]
- [x] Fetch `/definition/dukkha` → readable HTML, definitions with tradition + source labels ✓
- [x] Fetch `/definition/duhkha` (Sanskrit) → readable, covers Hindu + Buddhist traditions ✓
- [x] Fetch `/definition/paticcasamuppada` → readable, URL confirms ASCII-only path ✓

## Phase 2 — Implement Phase 4c in SKILL.md

- [x] Locate exact line numbers for Phase 4b end and Phase 5 start in SKILL.md.
  → verify: `grep -n "Phase 4b\|Phase 5" skill/vicaya/SKILL.md` shows boundary. ✓

- [x] Insert `### Phase 4c — WisdomLib` block between Phase 4b and Phase 5.
  → verify: Phase 4c at line 1298, Phase 5 at line 1333. ✓

- [x] Add Phase 4c row to the scratchpad template block.
  → verify: `grep -n "Phase 4c" SKILL.md` returns 3 hits. ✓

## Phase 3 — Final check

- [x] Read ~120 lines around the insertion point to confirm clean formatting.
  → verify: heading level ###, no broken structure, Phase 5 follows cleanly. ✓
