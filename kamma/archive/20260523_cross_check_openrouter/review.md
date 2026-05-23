## Thread
- **ID:** 20260523_cross_check_openrouter
- **Objective:** Replace the flaky `gemini` cross-check with a reliable provider that works whenever there's an internet connection.

## Files Changed
- `tools/research_sources.py` — +204 lines: provider chain, key resolution, JSON loader, CLI subcommand
- `data/openrouter_models.json` — new, 10 lines: editable free-model list
- `tests/test_cross_check.py` — new, 22 unit tests with `urlopen` monkey-patched
- `skill/vicaya/SKILL.md` — Phase 6 swap to `cross-check`, `# SELF_REVIEW:` branch, troubleshooting bullet rewritten
- `kamma/tech.md` — cross-check description rewritten
- `.env` — `OPENROUTER_API_KEY` added per user instruction

## Findings

| # | Severity | Location | What | Why | Fix |
|---|----------|----------|------|-----|-----|
| 1 | **major** | `tools/research_sources.py` cross_check chain | The chain has three external providers (OpenRouter, gemini CLI, NVIDIA build). Gemini was the failing tool we're moving AWAY from — keeping it in the chain is half-stepping. NVIDIA build serves the same `nemotron-3-super-120b` that's already at the OpenRouter chain's tail; "different rate-limit pool" is marginal. | Each extra provider doubles auth/config/test surface for diminishing reliability gains. The user explicitly said NVIDIA "very slow…last resort" — but if it's a true last resort over OpenRouter+self-review, it's not earning its keep. | Cut `_try_nvidia` and `_try_gemini_cli` from the chain. Chain becomes `OpenRouter → self-review`. Keep `gemini-cross-check` as a separate opt-in CLI subcommand. Removes ~80 lines + 6 tests. |
| 2 | **major** | `cross_check()` env-pin block | `VICAYA_CROSS_CHECK=openrouter\|nvidia\|gemini\|self` was never requested. Speculative complexity. | Four env-pin branches × test coverage for each. Not solving a real problem the user described. | Cut entirely. Trivial to re-add later if a real need surfaces. |
| 3 | minor | `_OPENROUTER_FALLBACK_CHAIN` constant | Hard-codes a duplicate of the JSON list as a "safety net" if the JSON file breaks. | The fallback rots silently against the JSON. If the JSON breaks, loud failure (return None → self-review sentinel) is better than serving stale models. | Cut the constant; `_load_openrouter_models` returns `[]` on error → OpenRouter request fails → chain falls through. |
| 4 | minor | `VICAYA_OPENROUTER_MODELS_FILE` env override | Never requested. Speculative. | Same as #2. | Cut. |
| 5 | minor | `_OPENCODE_AUTH_PATH` key fallback | Worth keeping — it's small, provides a backup path on machines where someone forgets `.env`. | — | **No change.** |
| 6 | minor (CodeRabbit) | `skill/vicaya/SKILL.md:66` | Helper table row described old provider order. | Stale doc drift. | **Fixed in this review pass.** |
| 7 | minor (CodeRabbit) | `kamma/threads/.../spec.md` | Spec listed old provider order. | Stale doc drift. | **Fixed in this review pass.** |

**Overall assessment:** the user's intuition that this was overcomplicated is correct. ~100 lines and ~6 tests could be deleted with zero loss of real-world reliability. The core insight — OpenRouter `models: [...]` server-side fallback + self-review sentinel — already covers every failure mode that matters. Gemini and NVIDIA branches were defensive scaffolding that hedges against improbable scenarios.

## Fixes Applied
- SKILL.md helper table row updated to match implementation order (CodeRabbit #6).
- spec.md provider list updated (CodeRabbit #7).
- **Findings #1–#4 fixed via simplification** (user approved): `cross_check` is now a single OpenRouter call → `# SELF_REVIEW:` sentinel on any failure. Cut `_try_nvidia`, `_try_gemini_cli`, `VICAYA_CROSS_CHECK` env pin, `VICAYA_OPENROUTER_MODELS_FILE` override, `_OPENROUTER_FALLBACK_CHAIN` constant, NVIDIA URL/model constants, and ~10 corresponding tests. Net change: helper went from 204 added lines to ~85; tests went from 22 to 14.
- **Discovered + fixed during the final live smoke: OpenRouter rejects `models` arrays longer than 3 entries with HTTP 400.** The original 5-entry JSON would have silently failed in production. Trimmed `data/openrouter_models.json` to 3 entries, added `_OPENROUTER_MAX_MODELS = 3` defensive slice in `_load_openrouter_models`, and a test (`test_models_truncates_to_api_cap`) so a future user editing the JSON to >3 entries gets correct behavior instead of a silent fall-through to self-review.

## Test Evidence
- `uv run pytest tests/test_cross_check.py` → **14 passed in 0.04s** (was 22, now leaner)
- `uv run pytest` (full suite) → **44 passed** (pre-existing calibre FTS test now runs without timeout on this pass)
- Live smoke, 3 runs against real OpenRouter:
  - run 1: timed out at the test's 120s cap (would have completed at the helper's default 180s) → correctly returned self-review sentinel
  - run 2: OK, 47.3s, 2384 chars critique
  - run 3: OK, 17.1s, 1938 chars critique
- `coderabbit review --agent` → 2 minor findings, both fixed

## Verdict
**PASSED.**

Final shape is what we'd ship if writing it fresh: a single OpenRouter POST with the model list externalized to `data/openrouter_models.json`, and a `# SELF_REVIEW:` sentinel fallback covering every failure mode (no key, bad JSON, network error, all models rate-limited, response timeout). The legacy `gemini_cross_check` function remains for ad-hoc opt-in but is no longer in any chain.

- Review date: 2026-05-23
- Reviewer: kamma /kamma (inline, Claude Opus 4.7)
