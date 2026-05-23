# Plan — replace Gemini cross-check with provider chain

## Architecture Decisions

- **Direct HTTP via stdlib `urllib`.** OpenRouter and NVIDIA are both
  OpenAI-compatible; the request body is identical (different URL/key/model).
  Pulling in the `openai` SDK for ~30 lines is the wrong trade — `httpx`,
  `pydantic-core`, `anyio`, `jiter` etc. for streaming/tool features we do
  not use.
- **Server-side fallback at OpenRouter via `models: [...]`.** OpenRouter
  retries across listed free models on rate-limit/error. Our code stays
  single-shot — no per-model retry loop.
- **Provider chain in our code, not retries.** Different providers = different
  rate-limit pools = real reliability. Retrying the same provider does not
  fix a quota error; falling to a different provider does.
- **Self-review sentinel rather than silent skip.** When all external
  providers are down, the helper emits `# SELF_REVIEW:` plus the Phase 6
  checklist text. The agent then runs the checklist on its own synthesis.
  Loses the independent-second-model property but preserves the structured
  critique discipline. Visible in the terminal report, not hidden.
- **Keep `gemini_cross_check` untouched.** Reversible; opt-in via
  `VICAYA_CROSS_CHECK=gemini`.
- **No `openai` SDK dependency.** Decided after confirming OpenRouter has no
  first-party SDK (their docs point to the OpenAI SDK with a swapped base URL)
  and NVIDIA's recommended path is the same.

## Phase 1 — Provider chain helper

- [ ] Add `_load_key(provider: str) -> str | None` that resolves a key for
      `openrouter` / `nvidia` by checking env (`OPENROUTER_API_KEY`,
      `NVIDIA_API_KEY`) then `~/.local/share/opencode/auth.json` →
      `.<provider>.key`.
      → verify: pytest with `monkeypatch.setenv("OPENROUTER_API_KEY", "x")`
        returns `"x"`; with env unset and a tmp HOME containing a fake
        `auth.json`, returns the file value; with neither, returns `None`.

- [ ] Add `_post_openai_compat(url, key, body, timeout) -> str` using
      `urllib.request`. Raises on non-2xx with the response body's `error.message`
      if parseable, else status code.
      → verify: monkeypatch `urllib.request.urlopen` to return a canned JSON
        with `choices[0].message.content == "ok"`; assert helper returns `"ok"`.

- [ ] Add `_try_openrouter(prompt, timeout) -> str | None`. Builds body with
      `models: [...]` set to the five free models from the spec; returns text
      on success, `None` on failure.
      → verify: monkeypatched urlopen returning 200 → returns text;
        urlopen raising HTTPError(429) → returns `None`.

- [ ] Add `_try_nvidia(prompt, timeout) -> str | None`. Same shape, single
      model `nvidia/nemotron-3-super-120b-a12b`, endpoint
      `https://integrate.api.nvidia.com/v1/chat/completions`.
      → verify: monkeypatched urlopen returning 200 → returns text.

- [ ] Add `_try_gemini_cli(prompt, timeout) -> str | None`. Wraps the existing
      `gemini_cross_check`; returns `None` when the result starts with `# ERROR:`.
      → verify: monkeypatch `gemini_cross_check` to return `"# ERROR: x"` →
        `_try_gemini_cli` returns `None`; non-error string → returned verbatim.

- [ ] Add `_self_review_sentinel() -> str` returning a fixed multi-line string
      starting `# SELF_REVIEW:` and listing the Phase 6 five-point checklist
      verbatim (so the agent can execute it without re-reading SKILL.md).
      → verify: returned string starts with `# SELF_REVIEW:` and contains all
        five point labels.

- [ ] Add public `cross_check(prompt, timeout=180) -> str`. Chains providers
      in this order honoring `VICAYA_CROSS_CHECK` env override
      (`openrouter|nvidia|gemini|self`). Falls through to self-review sentinel.
      → verify: monkeypatch all `_try_*` to return `None`; `cross_check("x")`
        returns the sentinel. Monkeypatch `_try_openrouter` to return `"hi"`;
        result is `"hi"`. Set `VICAYA_CROSS_CHECK=nvidia`; OpenRouter is not
        called.

## Phase 2 — CLI subcommand

- [ ] In `_cli()`, register `cross-check` subparser with `--timeout N`,
      reading prompt from stdin and writing result to stdout. Mirror the
      shape of the existing `gemini-cross-check` subparser exactly.
      → verify: `echo "Review: the sky is blue." | uv run tools/research_sources.py cross-check`
        prints non-empty output and exits 0.

## Phase 3 — Wire into SKILL.md + project docs

- [ ] Update `skill/vicaya/SKILL.md` Phase 6:
      - Replace `gemini-cross-check` invocation with `cross-check`.
      - Add a branch: if the helper output begins with `# SELF_REVIEW:`,
        the agent runs the embedded checklist against its own synthesis
        before writing the note, and the Phase 7 footer logs
        `cross-check: self-review` instead of a model name.
      - Update the troubleshooting bullet that mentioned `# ERROR:` from
        Gemini to describe the new chain's error surface
        (`# ERROR: all cross-check providers failed`).
      - Update the `# Tools available` / preflight section's mention of
        `gemini` to reflect the new chain (gemini becomes optional tertiary).
      → verify: `rg "gemini-cross-check" skill/` returns no hits in
        active instructions (historical references in Phase 7 attribution
        are fine if any remain — recheck).

- [ ] Update `kamma/tech.md` cross-check line to read:
      `**Cross-check:** OpenRouter free chain → NVIDIA Nemotron 3 Super →
      gemini CLI → self-review sentinel; stdlib `urllib`, no SDK dep.`
      → verify: `grep -i cross-check kamma/tech.md` shows the new chain.

## Phase 4 — Smoke and verify

- [ ] Run new pytests.
      → verify: `uv run pytest tests/ -k cross_check` green.

- [ ] Run full test suite for regressions.
      → verify: `uv run pytest` green.

- [ ] Live smoke: 5 consecutive cross-checks on a fixed sample synthesis.
      → verify: 5/5 invocations return non-empty, non-`# ERROR:` output.
