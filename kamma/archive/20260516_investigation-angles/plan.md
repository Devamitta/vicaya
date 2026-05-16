# Plan — Investigation angles checklist

## Architecture Decisions
- **New top-level section, not a new phase.** Avoids adding workflow weight. Triage happens inside Phase 1.
- **Angles list complements, does not replace, the perspective map.** Perspective map = positions within the topic. Angles = evidentiary lenses across sources. Both run in Phase 1.
- **Concrete search guidance per angle.** Each angle names the source(s), example book scope or tag cluster, and what a satisfying hit looks like. Keeps the agent reliable across runs.
- **Triage is explicit and recorded.** Applicable / not-applicable decisions go to scratchpad and (for non-applicable) the vault note's new `## Angles Not Pursued` table. Coverage becomes auditable.
- **Tags only suggested, not hardcoded.** For unverified clusters (Hindu, archaeology, sociology), instruct the agent to consult `data/calibre_tags.csv` at runtime rather than baking in names that may not exist.
- **Single file edit.** All changes land in `skill/vicaya/SKILL.md`. No helper changes.

## Phase 1 — Draft and insert the Investigation angles section

- [ ] Draft the new `## Investigation angles` section. Structure: intro paragraph (what the section is for, when to use it), triage instructions, then the 15 angles in 4 logical groups (Textual layers / Other Buddhist schools / Comparative religion / Modern voices / Academic disciplines), each with: name, when it applies, where to search (concrete: book codes, Calibre tag clusters or csv-lookup directive, suggested authors, web targets), what counts as a satisfying hit.
  → verify: drafted section reviewed for completeness — all 15 user-named angles present, each has concrete search guidance, intro mentions triage.

- [ ] Insert the section into `skill/vicaya/SKILL.md` immediately before `### Phase 1 — Vault context` (i.e. right after the "## The seven phases" header and its one-line intro, but before the first phase heading).
  → verify: `rg -n "^## Investigation angles" skill/vicaya/SKILL.md` returns exactly one line, and `rg -n "^### Phase 1" skill/vicaya/SKILL.md` returns a line number greater than that.

## Phase 2 — Wire Phase 1 to the angle triage

- [ ] Add a new step at the top of `### Phase 1 — Vault context` that mandates running the angle triage from the new section before the perspective map is built. One short paragraph. Cross-reference: "See **Investigation angles** above."
  → verify: `rg -n "Investigation angles" skill/vicaya/SKILL.md` returns at least two hits (the section header + the Phase 1 reference).

- [ ] Update the Phase 1 scratchpad block (around line 165) so the appended Phase 1 summary includes an "Angles applicable" and "Angles not pursued (with reason)" line.
  → verify: the scratch block snippet in SKILL.md lists angle-triage output alongside perspective-map output.

## Phase 3 — Update Phase 5 source-completeness check and Phase 7 template

- [ ] Extend the Phase 5 "Source completeness check before you write" step to include angle coverage: "For every angle marked applicable in Phase 1's triage, have I cited at least one source?" Add it as a bullet beneath the existing perspective-map check.
  → verify: the Phase 5 source-completeness paragraph in SKILL.md contains the new angle-coverage bullet.

- [ ] Extend the Phase 7 pre-write source-coverage checklist with an "Angles Not Pursued logged?" bullet.
  → verify: the Phase 7 checklist in SKILL.md lists the new bullet.

- [ ] Add a new `## Angles Not Pursued` subsection to the Phase 7 vault-note template, positioned between `## Sources Investigated, Not Used` and `## Critical Gaps`. Format: small markdown table with columns `Angle | Reason not pursued`.
  → verify: the template in SKILL.md contains the new subsection with example rows.

## Phase 4 — Final consistency pass

- [ ] Read the modified `skill/vicaya/SKILL.md` end-to-end (or at least every section touched + adjacent sections). Confirm: no orphan references, no duplicated hard rules, no broken cross-links, intro of "## The seven phases" still flows into the new section then into Phase 1.
  → verify: read complete; no inconsistencies found, or any found are fixed.

- [ ] Grep for any stale references that imply the perspective map is the only Phase 1 lens. Reword if the new section makes them misleading.
  → verify: `rg -n "perspective map" skill/vicaya/SKILL.md` results reviewed; none contradict the new angle list.
