# Spec — Borrow from academic-research-skills

## Overview
Study the `Imbad0202/academic-research-skills` (ARS) repo (cloned to
`/home/bodhirasa/MyFiles/2_Resources/Code/academic-research-skills`) and produce
a numbered list of concrete, actionable changes that could improve the vicaya
skill (`/home/bodhirasa/MyFiles/3_Active/vicaya/skill/vicaya/SKILL.md`).

## What it should do
- One `suggestions.md` file with numbered, discussable items.
- Each item: title, source-in-ARS, why it helps vicaya, where in vicaya it
  lands, rough effort, recommendation (adopt / adapt / skip).
- No edits to vicaya itself — discussion-first.

## Assumptions & uncertainties
- ARS is academic/medical evidence synthesis (PRISMA, RoB 2, meta-analysis);
  vicaya is canonical Pāḷi/Buddhist research with a *fundamentally different*
  evidence base (texts and lineages, not RCTs). Mechanical lifts will misfire;
  the value is in workflow patterns and integrity gates, not in the
  evidence-grading machinery.
- ARS is multi-agent (13 specialised agents, 6 phases, 3 mandatory
  checkpoints). Vicaya is single-agent, 7 phases. Many ARS ideas have to be
  collapsed into "checklist sections inside SKILL.md," not new agents.
- Vicaya already has: angle triage, perspective map, counter-perspective
  search, scratchpad, second-pass Gemini review, rejection log, self-improvement
  loop. Several ARS ideas overlap with these — flagged as `skip — already
  covered` where so.

## Constraints
- Single SKILL.md file, executed by one agent (Claude, Codex, Gemini)
  per run. No multi-agent orchestration.
- Pāḷi-canon evidence, not biomedical. RoB 2 / GRADE / FINER do not apply
  directly.
- Maintain portability — no agent-specific memory, no required external
  services beyond what's already wired (Calibre, CST SQLite, Obsidian CLI,
  Gemini CLI, YouTube).

## How we'll know it's done
- `suggestions.md` exists in this thread directory.
- Every ARS source area (shared/, deep-research/agents/, MODE_REGISTRY,
  POSITIONING) has been considered, even if the verdict is "skip."
- User can discuss item-by-item without re-reading either codebase.

## What's not included
- No edits to `skill/vicaya/SKILL.md` or `tools/research_sources.py`.
- No new helper scripts. No new modes.
- No vendoring of ARS files into vicaya.
