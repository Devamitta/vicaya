# Spec — WisdomLib integration for Vicaya

## Overview
Add wisdomlib.org as a mandatory research source in the Vicaya skill. The site
is a large, structured encyclopaedia of Indian religion, philosophy, and culture,
with entries indexed across Sanskrit, Pāḷi, and other Indic languages. It is
especially valuable for defining technical terms that appear in the research
question.

## What it should do
- Every Vicaya run must query wisdomlib.org for the principal technical terms
  in the research question.
- Instructions explain the URL pattern and how terms must be formed (ASCII,
  no diacritics in the URL path).
- Instructions specify the step as Phase 4c, placed after Phase 4b (YouTube)
  and before Phase 5 (Synthesis).
- The step is explicitly mandatory — not optional.
- Results are cited as T2 evidence (or T1 if the entry quotes a primary text).
- The scratchpad template gains a Phase 4c line.

## Assumptions & uncertainties
- Confirmed: `https://www.wisdomlib.org/definition/<term>` returns readable HTML
  via WebFetch (no JS wall).
- Confirmed: URL path uses ASCII — diacritics stripped (e.g., `duḥkha` → `duhkha`,
  `paṭiccasamuppāda` → `paticcasamuppada`).
- Confirmed: both Sanskrit IAST and Pāḷi terms have their own definition pages.
- The site covers Hindu, Buddhist (Theravāda, Mahāyāna, Tibetan), and Jain
  traditions — results may need filtering to the tradition relevant to the question.

## Constraints
- Change is limited to `skill/vicaya/SKILL.md`.
- No new Python helpers; no new data files.
- Instruction style must match existing Phase 4a / 4b blocks.

## How we'll know it's done
- `SKILL.md` contains `### Phase 4c — WisdomLib` between Phase 4b and Phase 5.
- The block specifies: always-on, URL pattern, ASCII term formation, tradition
  filtering, citation form, evidence tier, and scratchpad append instruction.
- The scratch template has a Phase 4c row.

## What's not included
- A Python helper for WisdomLib.
- Changes to any file other than SKILL.md.
