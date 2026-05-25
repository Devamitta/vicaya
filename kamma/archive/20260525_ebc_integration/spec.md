# Spec — Integrate Early Buddhist Connections (EBC) vault into vicaya

## Overview
A second Obsidian vault at `~/MyFiles/2_Resources/Early Buddhist Connections/` ("EBC") contains ~22k sutta files and ~1.5k Vinaya files curated by the Dhamma Vinaya Connections project. It supplies three capabilities vicaya currently lacks: per-sutta Chinese-Āgama parallel metadata, multiple parallel English translations of the same text, and actual Chinese-Āgama translations (Patton, BDK). This thread wires EBC into the vicaya skill as a first-class read-only evidence source.

## What it should do
- Expose two new helpers in `tools/research_sources.py` + matching CLI subcommands:
  - `get-ebc-overview <SUTTA_CODE>` — parse the per-sutta YAML overview card and return structured fields (titles, themes, training, formula, named Āgama parallels, partial parallels, summary, similes).
  - `search-ebc <QUERY>` — ripgrep across the EBC vault, returning `VaultHit`-shaped results. Independent of the Obsidian CLI.
- Document the EBC folder layout in SKILL.md so the agent can `Read` translator files and Vinaya commentary directly without bespoke helpers.
- Wire EBC into the existing phase flow: Phase 1 seeds parallels from the overview card; Phase 3 quotes named Āgama parallels via `Read`; `search-ebc` is the generic discovery tool.

## Assumptions & uncertainties
- Sutta-code conventions across EBC are consistent: overview cards live at `+Suttas/Overviews Suttas/<NIK>/<RANGE>/<CODE>.md` where `<NIK>` is `MN`/`DN`/`SN`/etc. and `<CODE>` matches the YAML `sutta_code` field. Confirmed for MN10; assumed for all nikāyas. Will spot-check during implementation.
- Translator filenames follow `<nik>-<translator>[-pali]/<code>-<translator>[-pali].md`. Variations exist across translators; we will not enumerate them — agents resolve via `find`/`rg`.
- YAML frontmatter is well-formed enough that a small parser (no PyYAML dependency) handles it. If we hit malformed files we fall back to returning the raw text section.
- The EBC vault is read-only reference material. Vicaya does not write to it.
- Single env var `VICAYA_EBC_VAULT_PATH` is enough; no per-translator config.

## Constraints
- Per global rules: do not modify the user's `.env`. Update `.env.example` only and tell the user.
- No new third-party Python dependencies. Use stdlib only (the existing pattern in `research_sources.py`).
- Helpers must work whether or not Obsidian is running.
- Existing helpers and tests must not regress.

## How we'll know it's done
- `uv run tools/research_sources.py get-ebc-overview MN10` prints JSON with `parallels_agama` containing `MA98`, `EA12.1`, etc.
- `uv run tools/research_sources.py search-ebc "vedanānupassanā"` returns ≥3 relevant `.md` paths.
- SKILL.md has a new EBC section that lists the helpers, the folder layout, and references to `get-ebc-overview` / `search-ebc` from Phase 1 and Phase 3.
- `.env.example` has `VICAYA_EBC_VAULT_PATH` documented.
- Existing test suite (if any) still passes.

## What's not included
- A `search-ebc-catalogue` helper for the TSV — single-file ripgrep is enough.
- `get-ebc-translation` / `get-ebc-vinaya` helpers — folder map in SKILL.md is enough; agent uses `Read`.
- Merging EBC overview with canon SQLite into a unified per-sutta object.
- Auto-syncing EBC from upstream GitHub.
- Modifying the user's `.env` file.
