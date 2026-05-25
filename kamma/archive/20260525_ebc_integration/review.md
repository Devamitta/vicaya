## Thread
- **ID:** 20260525_ebc_integration
- **Objective:** Wire the Early Buddhist Connections (EBC) Obsidian vault into vicaya as a first-class read-only evidence source.

## Files Changed
- `.env.example` — added `VICAYA_EBC_VAULT_PATH` documentation
- `.env` — added one line per explicit user permission
- `tools/research_sources.py` — added `EBCOverview` dataclass, `get_ebc_overview()`, `search_ebc()`, supporting helpers (`_normalise_sutta_code`, `_ebc_nikaya_for`, `_find_ebc_overview_path`, `_parse_ebc_yaml`, `_split_parallel_refs`, `_as_list`), `DEFAULT_EBC_VAULT_PATH`, two CLI subcommands
- `skill/vicaya/SKILL.md` — added EBC section (folder map, when-to-reach-for-EBC, citation rules, examples), helper-table rows, return-shape entry, Phase 1 amendment, post-Phase-2 EBC parallel-evidence-pull subsection

## Findings
| # | Severity | Location | What | Why | Fix |
|---|----------|----------|------|-----|-----|
| 1 | nit | `research_sources.py` `_EBC_NIKAYA_PREFIXES` | `T` is a single-letter prefix; could over-match a future code that starts with T but is not Taishō | Theoretical only — Taishō is the only code namespace starting with `T` in EBC | Document if it becomes a real issue. No change. |

No blocking, major, or minor findings.

## Fixes Applied
- During implementation: switched `search_ebc` from `rg` to `grep` after discovering ripgrep wasn't on PATH (the shell `rg` was a Claude Code wrapper function, not a binary). Benchmark confirmed grep at ~40ms is fine for the 22k-file vault.
- Updated the CLI help string for `search-ebc` to match the implementation ("Fixed-string grep" not "Ripgrep").

## Test Evidence
- `uv run tools/research_sources.py --help` → all 11 subcommands listed (9 pre-existing + 2 new). Pass.
- `uv run tools/research_sources.py get-ebc-overview MN10` → `parallels_agama: ["EA12.1", "EA27.1", "MA31", "MA81", "MA98"]`. Pass.
- Normalisation variants (`mn 10`, `mn-10`, `dn22`, `MA98`) all resolve; bogus `ZZ999` exits 1 cleanly. Pass.
- `search-ebc "vedanānupassanā"` → 4 precise hits across Sujato Pāḷi, DeepSeek, Pali-only, and the ATI thematic index. Pass.
- `search-ebc "satipaṭṭhāna" --folder "+Suttas/Overviews Suttas/MN"` → 2 hits in MN10.md only. Folder scoping works. Pass.
- `search-ebc "satipaṭṭhāna" --folder "+Vinaya"` → 0 hits. Confirms folder scope isn't leaking. Pass.
- MA98 Patton file exists at the path documented in SKILL.md. Pass.

## Verdict
PASSED
- Review date: 2026-05-25
- Reviewer: kamma (inline)
