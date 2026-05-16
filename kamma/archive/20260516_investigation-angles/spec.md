# Spec — Investigation angles checklist for vicaya

## Overview
Add a standing, comprehensive list of investigation angles to the vicaya skill so that every research run systematically considers each perspective when applicable, rather than relying on whatever the keyword searches happen to surface.

## Current behavior (what the skill does today)
- Phase 1 builds a *perspective map* (2–5 competing positions, only if interpretive dispute exists).
- Phase 1 mandates a *counter-perspective search* per named position.
- Beyond that, the choice of which angles to investigate is left to the agent's judgment — which means runs vary in coverage and rare angles (archaeology, sociology, other religions, late Khuddaka, ṭīkā) routinely get skipped without record.

## What it should do
Introduce a new top-level section in `skill/vicaya/SKILL.md` titled **"Investigation angles"**, placed immediately before `### Phase 1 — Vault context`. The section:

1. **Lists 15 standing angles**, grouped logically:
   - Textual layers: early Pāḷi (dhamma + vinaya); EBT āgama parallels; Abhidhamma; late Khuddaka Nikāya; commentaries & ṭīkā.
   - Other Buddhist schools: Mahāyāna / Vajrayāna / Yogācāra.
   - Comparative religion: Sanskrit & Indian religions (Hindu, Jain, etc.); other religions broadly.
   - Voices: modern teachers.
   - Academic disciplines: sociology, psychology, philosophy, cognitive science, archaeology, history.
2. **For each angle, gives concrete search guidance**: which source to query (canon DB book scope, Calibre tag cluster, suggested authors, web targets), and what counts as a satisfying hit.
3. **Mandates a triage procedure** at the start of Phase 1: the agent walks the list, decides applicability for *this* question, records the decision per angle. Applicable angles must be searched in Phases 2–4; non-applicable angles get a one-line reason recorded.
4. **Surfaces the result in the vault note** via a new `## Angles Not Pursued` subsection (sibling to `## Sources Investigated, Not Used`), so coverage is transparent and future runs can revisit.

## Assumptions & uncertainties
- **Assumption:** the perspective map (Phase 1) and the angle list are complementary — the perspective map is about *positions within a topic*; the angle list is about *evidentiary lenses across sources*. They will reference each other but not collapse into one.
- **Assumption:** for each angle, a one-line concrete search recipe is enough — the agent can adapt patterns (book codes, tag clusters) from the existing skill content.
- **Uncertainty:** there is no `Hinduism`/`Indology`/`Jainism` tag cluster verified in the Calibre tag table inside SKILL.md. The spec will instruct the agent to use the existing `data/calibre_tags.csv` to discover the right tag(s) per run rather than hard-coding tags the user may not have. Same caveat for `Archaeology` and `Sociology`.
- **Uncertainty:** "if applicable" is a judgment call. The triage step makes the call explicit and auditable rather than silent.

## Constraints
- Do not break existing Phase 1 logic (perspective map, counter-perspective search). The angle list extends, not replaces, them.
- Do not add a new phase — runs are already long. Triage happens inside Phase 1.
- Scratchpad must record angle triage so the vault note's `## Angles Not Pursued` table can be reconstructed even after context compaction.
- Phase 7 source-coverage check and template must be updated to include angle coverage.
- No emojis. Keep existing tone.

## Affected files
- `skill/vicaya/SKILL.md` — primary edit; new section + updates to Phase 1, Phase 5/7 checklists, scratchpad section, template.

The skill file is symlinked from `~/.claude/skills/vicaya/`, so edits propagate live.

## How we'll know it's done
- A new `## Investigation angles` section exists in SKILL.md before Phase 1.
- It contains all 15 user-named angles with concrete search guidance per angle.
- Phase 1 explicitly cross-references it (triage step).
- Scratchpad block for Phase 1 includes angle triage output.
- Phase 7 template includes `## Angles Not Pursued`.
- Source-coverage check in Phase 5/7 references angle coverage.
- The skill still reads as one coherent document (no orphan references, no duplicate hard rules).

## What's not included
- Automating angle search (no helper changes).
- Adding new helper subcommands.
- Verifying every suggested Calibre tag exists in `data/calibre_tags.csv` — agent verifies at runtime per question.
- Backfilling existing vault notes.
