# Plan — vicaya skill improvements

## Architecture decisions
- Reuse existing helpers (`_append_under_phase`, `_gate_marker`, `_PHASE_INDEX`,
  `search_calibre`). No new subcommands beyond a `--class` flag.
- State file is a tiny JSON at `data/scratch/.active`; all reads/writes swallow
  errors (never break a search), mirroring `_maybe_autolog`'s defensiveness.

## Phase 1 — Fix B: scratch state file
- [ ] Add `_STATE_FILE`, `_read_state()`, `_write_state(scratch, phase)`.
- [ ] `_scratch_path`: env → state → slug → error.
- [ ] `scratch_init`: `_write_state(path, "0")`.
- [ ] `scratch_gate`: on success, advance state phase to the next phase id.
- [ ] `_maybe_autolog`: resolve scratch+phase from env-or-state.
  → verify: pytest new state-file test passes.

## Phase 2 — Fix A: thematic auto-skip
- [ ] `_AUTO_SKIP_PHASES`, `_run_class(text)` helper.
- [ ] `scratch_init(slug, run_class=...)` writes `**Run class:**` header line.
- [ ] `scratch_gate`: for thematic runs, auto-write 2.5/3b skip gates before the
  prior-gate check.
- [ ] CLI: `scratch-init --class {sutta-anchored,thematic}`.
  → verify: pytest thematic auto-skip test passes.

## Phase 3 — Fix C: honest calibre-check
- [ ] `calibre_library_available`: probe via `search_calibre("dhamma", limit=1)`.
- [ ] `search-calibre` CLI: try/except `CalibreUnavailable` → structured sentinel, exit 1.
  → verify: pytest calibre agreement test passes.

## Phase 4 — Docs + TODO
- [ ] Trim SKILL.md scratch quick-start (drop per-call export instructions);
  note `--class thematic` and the calibre sentinel.
- [ ] Mark issues addressed in `runs/TODO.md`.
  → verify: `uv run -m pytest` fully green; `git diff` review.
