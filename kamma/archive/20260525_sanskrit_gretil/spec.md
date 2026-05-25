# Spec — Sanskrit GRETIL integration

## Overview
Add a Sanskrit primary-source search capability to Vicaya, backed by a locally-cloned GRETIL corpus at `/home/bodhirasa/MyFiles/2_Resources/gretil`. When a research question touches pre-Buddhist Brahmanical/Vedic context (SKILL.md angle 7), the skill will grep the local GRETIL plain-text files and return cited IAST passages — enabling direct quotation of Sanskrit primary sources in research notes.

GRETIL (Göttingen Register of Electronic Texts in Indian Languages) is the most comprehensive open corpus of Vedic, Epic, Upaniṣadic, and philosophical Sanskrit texts in Unicode IAST, with no login required and bulk-downloadable via `git clone https://github.com/wujastyk/GRETIL-mirror.git`.

## Repo context
- `tools/research_sources.py` — all source helpers live here; new code follows the existing pattern.
- `search_ebc()` (~line 941) is the direct template: `grep -rn -F --include="*.md"` across a local folder, returning `list[VaultHit]`. `search_sanskrit` mirrors this exactly.
- `skill/vicaya/SKILL.md` already documents angle 7 ("Sanskrit texts, Hindu and other Indian religions") pointing to Calibre + web only. This thread upgrades it with a local search phase.
- `.env.example` documents all `VICAYA_*` env vars.
- Tests in `tests/test_research_sources.py` use skip-if-unconfigured pattern.

## What it should do
1. `search_sanskrit(query, folder, path, limit)` — `grep -rn -F --include="*.txt"` across the GRETIL corpus. Returns `list[VaultHit]`. Silent skip when path unset/absent.
2. CLI subcommand `search-sanskrit --folder --limit`. Prints JSON array.
3. SKILL.md angle 7 updated with `search-sanskrit` command and citation rules (use `Path(path).stem` for text name).
4. New Phase 3b in SKILL.md (conditional on angle 7 applicable): runs after Phase 3, before Phase 4a.
5. `.env.example` updated with `VICAYA_GRETIL_PATH=~/MyFiles/2_Resources/gretil`.
6. Tests: unconfigured-skip + corpus hit test (skipped when absent).
7. README.md: Sources table row + Setup clone step.

## Assumptions & uncertainties
- GRETIL `.txt` files are Unicode IAST (confirmed by INDOLOGY mirror documentation: "all files are Unicode").
- File structure: texts organized in subfolders by tradition. `grep --include="*.txt" -r` catches them all.
- `text_name` derivable by caller as `Path(path).stem` — e.g. `rigveda_shas_u.txt` → `rigveda_shas_u`.
- Corpus cloned to `/home/bodhirasa/MyFiles/2_Resources/gretil` per user specification.

## Constraints
- No new external dependencies.
- Silent skip when path unset or absent (consistent with all other sources).
- Corpus download is a one-time manual step; not automated.
- `.txt` files only — TEI XML excluded (markup noise).
- Returns `list[VaultHit]` — no new dataclass.

## How we'll know it's done
- `uv run tools/research_sources.py search-sanskrit "atman"` returns JSON hits when corpus present.
- Returns `[]` when `VICAYA_GRETIL_PATH` is unset.
- `uv run pytest tests/` all pass.
- SKILL.md Phase 3b documented; angle 7 mentions `search-sanskrit`.
- README Sources table and Setup section updated.

## What's not included
- DCS (morphological annotations).
- Muktabodha, TITUS, Sanskrit Library, Sanskrit Documents.
- Devanagari normalisation, auto-download, per-text verse-citation parsing.
