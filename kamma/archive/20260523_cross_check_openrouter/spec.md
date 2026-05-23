# Replace Gemini cross-check with a reliable provider chain

## Overview
The Phase 6 cross-check shells to `gemini -p`. Across `runs/processed/` it
fails on roughly 1 session in 3 due to (a) free-tier quota / `TerminalQuotaError`,
(b) 120 s timeout on large prompts, (c) OAuth refresh hanging in headless or
Flatpak shells. Replace it with a layered provider chain that falls back
across services so a single rate-limit, network error, or auth failure never
takes the whole cross-check down.

## What it should do
A new helper `cross_check(prompt, timeout=180)` in `tools/research_sources.py`
tries providers in order and returns on the first success:

1. **OpenRouter** (free model chain via server-side `models: [...]` fallback).
   Key from `OPENROUTER_API_KEY` env var; if absent, read
   `~/.local/share/opencode/auth.json` → `.openrouter.key`.
2. **`gemini` CLI** — second-tier for users with gemini set up but no OpenRouter.
3. **NVIDIA `integrate.api.nvidia.com`** (`nemotron-3-super-120b-a12b` free
   tier, OpenAI-compatible). Key from `NVIDIA_API_KEY` or
   `~/.local/share/opencode/auth.json` → `.nvidia.key`. Intentionally last:
   serves the same slow ~60s Nemotron that already sits at the OpenRouter
   chain's tail; only kept as a different rate-limit bucket for the rare
   case where both OpenRouter and `gemini` are simultaneously unavailable.
4. **`# SELF_REVIEW:` sentinel** — when no external provider is reachable,
   the helper returns a sentinel line containing the Phase 6 checklist. The
   calling agent runs the checklist on its own synthesis instead.
5. Only if step 4 cannot be produced (it always can) → `# ERROR: …` with a
   setup hint pointing at openrouter.ai/keys.

A new CLI subcommand `cross-check` exposes the chain. `gemini-cross-check`
stays in the code but is no longer wired into Phase 6.

## OpenRouter free model chain (ordered, passed to OpenRouter `models` field)
1. `nvidia/nemotron-3-super-120b-a12b:free`
2. `openai/gpt-oss-120b:free`
3. `qwen/qwen3-next-80b-a3b-instruct:free`
4. `deepseek/deepseek-v3.2-exp:free`
5. `meta-llama/llama-3.3-70b-instruct:free`

OpenRouter routes server-side; rate-limit on one transparently falls to the
next in the same request.

## Assumptions & uncertainties
- The OpenRouter and NVIDIA keys already present in
  `~/.local/share/opencode/auth.json` remain valid.
- Cross-check reviews synthesis **text only** — not URLs. Confirmed with user.
- The free pooled quota (OpenRouter free + NVIDIA build tier) covers
  ≤ ~10 `/vicaya` runs per day comfortably.
- The current `gemini_cross_check` helper's contract (return a string,
  `# ERROR:` on failure) is the right shape; the new helper mirrors it.

## Constraints
- **No new Python dependencies.** Use stdlib `urllib.request`. The project
  has no LLM SDK today and adding `openai` (the only viable shim) would
  bring `httpx`, `pydantic-core`, `anyio`, etc. for ~30 lines of HTTP.
- Keep `gemini_cross_check` callable so a user with `VICAYA_CROSS_CHECK=gemini`
  can opt back in.
- Preserve the existing `# ERROR:` return convention for the Phase 6 caller.

## How we'll know it's done
- `echo "review this text…" | uv run tools/research_sources.py cross-check`
  returns ≥ 1 paragraph of critique against the live API.
- 5 consecutive invocations all return non-error output (no `# ERROR:` lines).
- `uv run pytest` is green, including new tests that monkey-patch
  `urllib.request.urlopen` to cover: OpenRouter happy path, OpenRouter→NVIDIA
  fallback on 429, all-providers-down → `# SELF_REVIEW:` sentinel.
- `skill/vicaya/SKILL.md` Phase 6 calls `cross-check` (not `gemini-cross-check`),
  has a branch for the `# SELF_REVIEW:` sentinel, and the troubleshooting
  bullet is updated.
- `kamma/tech.md` cross-check line names the new chain.

## What's not included
- Migrating to `:online` web-search variants (costs money; cross-check is
  text-only by design).
- Removing or deprecating `gemini_cross_check`.
- Adding the `openai` SDK or any HTTP library beyond stdlib.
- Any change to other vicaya phases.
