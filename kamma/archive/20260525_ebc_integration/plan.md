# Plan — EBC integration

## Architecture Decisions
- **No PyYAML dependency.** Parse the overview-card frontmatter with a small hand-rolled reader (the format is consistent: scalar strings and one-level lists). Matches the rest of `research_sources.py` which is stdlib-only.
- **Read files directly off disk.** No Obsidian CLI for EBC — it is a static reference vault. Works whether or not Obsidian is running.
- **`search_ebc` uses ripgrep.** Already a project standard (per global rules); fast on 22k files.
- **No catalogue/translation/vinaya helpers.** Path patterns documented in SKILL.md; agent uses `Read`/`rg`. Keeps surface area minimal.
- **Don't modify `.env`.** Update `.env.example` only; tell the user. Global rule: never modify .env files.
- **EBC code-to-path resolution** uses the YAML `sutta_code` as the canonical key. Folder layout is `+Suttas/Overviews Suttas/<NIK>/<RANGE>/<CODE>.md`. Normalisation: uppercase the input, strip spaces and hyphens (`mn 10`, `MN-10`, `mn10` → `MN10`).

## Phase A — Config + dataclass
- [ ] A1. Add `VICAYA_EBC_VAULT_PATH=~/MyFiles/2_Resources/Early Buddhist Connections` to `.env.example` with a brief comment.
  → verify: `grep VICAYA_EBC .env.example` returns the line.
- [ ] A2. In `tools/research_sources.py`, add `DEFAULT_EBC_VAULT_PATH = _env_path("VICAYA_EBC_VAULT_PATH", "~/MyFiles/2_Resources/Early Buddhist Connections")` near the other `DEFAULT_*` paths. Add an `EBCOverview` dataclass with fields: `code`, `pts`, `titles` (list), `nikaya` (list), `chapter` (list), `themes` (list), `topics` (list), `training` (list), `formula` (list), `audience` (list), `teacher` (list), `parallels_agama` (list), `parallels_partial` (list), `path` (str).
  → verify: `uv run -c "from tools.research_sources import EBCOverview, DEFAULT_EBC_VAULT_PATH; print(DEFAULT_EBC_VAULT_PATH)"` prints the path.

## Phase B — get_ebc_overview
- [ ] B1. Add `_normalise_sutta_code(s)` helper: uppercase, strip whitespace and hyphens (`mn 10` → `MN10`). Return as-is when no match pattern detected.
  → verify: included in CLI smoke test in Phase D.
- [ ] B2. Add `_find_overview_path(code, vault)` — walks `+Suttas/Overviews Suttas/<NIK>/`. Determines nikāya from the code prefix (`MN`, `DN`, `SN`, `AN`, `DHP`, `UD`, `ITI`, `SNP`, `THAG`, `THIG`, `DA`, `MA`, `EA`, `SA`, `T`, `PDHP`). Walks the nikāya dir and uses `Path.rglob(f"{CODE}.md")` to find the file. Returns `Path` or `None`.
  → verify: included in CLI smoke test.
- [ ] B3. Add `_parse_overview_yaml(text)` — reads the leading `---\n...\n---` block, parses scalars (`key: "value"`) and one-level lists (`key:\n  - "a"\n  - "b"`). Returns `dict[str, str | list[str]]`. Strips surrounding quotes.
  → verify: included in CLI smoke test.
- [ ] B4. Add `get_ebc_overview(code, vault=DEFAULT_EBC_VAULT_PATH) -> EBCOverview | None`. Normalises code, resolves path, parses YAML, maps fields. Splits the `parallels_agama` / `parallels_partilal` (sic) strings on `;` and `,` and extracts the codes from any `[[...]]` wikilinks. Returns `None` if file missing.
  → verify: included in CLI smoke test.

## Phase C — search_ebc
- [ ] C1. Add `search_ebc(query, folder=None, vault=DEFAULT_EBC_VAULT_PATH, limit=20) -> list[VaultHit]`. Invokes `rg --type md -n --no-heading -F <query> <vault-or-subdir>`. Parses `path:line:text` output into `VaultHit(path, snippet, line)`. Truncates snippet to ~300 chars.
  → verify: included in CLI smoke test.

## Phase D — CLI + smoke tests
- [ ] D1. In `_cli()`, register `get-ebc-overview <code>` subcommand → calls helper, dumps JSON dict via `dataclasses.asdict`.
  → verify: `uv run tools/research_sources.py get-ebc-overview MN10 | jq .parallels_agama` lists `MA98`, `EA12.1`, `EA27.1`, `MA31`, `MA81`.
- [ ] D2. Register `search-ebc <query> [--folder PATH] [--limit N]` subcommand.
  → verify: `uv run tools/research_sources.py search-ebc "vedanānupassanā" --limit 5 | jq '. | length'` ≥ 3.
- [ ] D3. Spot-check normalisation: `get-ebc-overview "mn 10"`, `get-ebc-overview mn-10`, `get-ebc-overview dn22`, `get-ebc-overview MA98` all return populated objects.
  → verify: each command returns JSON with a non-empty `code` and `titles`.

## Phase E — SKILL.md wiring
- [ ] E1. Add a new top-level section "EBC (Early Buddhist Connections) vault" after the "Setup — paths and tools" section. Document: env var, folder map (overviews, sutta texts by translator with path pattern, Vinaya by source, Catalogue TSV path), translator list, evidence-tier mapping (Pāḷi mūla and Patton/BDK Āgamas = T1 for the text they quote; bmc1 / Ñāṇatusita / overview-card editorial = T2; cite the underlying translator, never EBC itself).
  → verify: read SKILL.md; section present, all helpers listed, folder map readable.
- [ ] E2. Add `get-ebc-overview` and `search-ebc` to the helper subcommand table in the "Calling the helpers" section.
  → verify: table contains both rows.
- [ ] E3. Add `EBCOverview` to the "Helper return shapes" section.
  → verify: dataclass shape documented.
- [ ] E4. Amend Phase 1 (Reconnaissance): "If the question is sutta-anchored, run `get-ebc-overview <code>` to seed parallels and themes into the perspective map." Amend Phase 3 (Commentary / parallels): "For named Āgama parallels from `get-ebc-overview`, `Read` the corresponding `+Suttas/Sutta Texts/Agamas Dhamma pearls/<nik>-patton/<code>-patton.md` or `Agamas BDK/<nik>-bdk/<code>-bdk.md` and quote verbatim." Add `search-ebc` as a discovery tool throughout.
  → verify: both phase blocks reference EBC helpers.

## Phase F — End-to-end smoke
- [ ] F1. From the project root, run the full smoke sequence: `get-ebc-overview MN10` → pick MA98 from output → `Read` `+Suttas/Sutta Texts/Agamas Dhamma pearls/ma-patton/ma98-patton.md` → confirm it opens. `search-ebc "satipaṭṭhāna" --limit 5` → confirm relevant hits.
  → verify: all three commands return real data; no exceptions or empty results.

## Non-regression
- [ ] G1. After all changes, run `uv run tools/research_sources.py --help` and confirm existing subcommands still appear.
  → verify: `search-vault`, `search-canon`, `resolve-citation`, `search-calibre`, `lookup-book`, `cross-check`, `gemini-cross-check` all still listed.
