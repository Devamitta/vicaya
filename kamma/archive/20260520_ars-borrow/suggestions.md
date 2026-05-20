# Vicaya improvement suggestions — drawn from academic-research-skills

Repo studied: `Imbad0202/academic-research-skills` (v3.9.4.2) at
`/home/bodhirasa/MyFiles/2_Resources/Code/academic-research-skills`.
Focus: `deep-research/` skill, plus `shared/` patterns and POSITIONING.

Verdict legend: **adopt** = lift more or less as-is, **adapt** = take the
idea but rewrite for Pāḷi/canon context, **skip** = already covered or not
a fit.

Items are ordered by expected impact on vicaya note quality.

---

## 1. Pre-draft "Devil's Advocate" pass (checklist, not agent)
- **Source:** `deep-research/agents/devils_advocate_agent.md`, "Three
  Mandatory Checkpoints" — runs at Phase 1 (scoping), Phase 3 (after
  analysis), Phase 5 (final vulnerability scan).
- **Why it helps:** Vicaya already has counter-perspective *search*. What it
  lacks is a structured *attack* on the synthesis before writing — cherry-
  picking checks, "what evidence wasn't found and does its absence matter",
  alternative explanations, strongest counter-argument. The cross-check in
  Phase 6 is downstream of the draft; a Phase 5 self-attack would catch
  framing errors earlier.
- **Lands in vicaya:** New short subsection inside Phase 5 — "Devil's
  Advocate checklist" with ~6 explicit questions to answer in the scratchpad
  before drafting. Not an agent — a checklist the same agent walks.
- **Effort:** ~30 lines added to SKILL.md.
- **Verdict:** **adopt** (as a checklist).

## 2. Severity tiers for issues / gaps
- **Source:** ARS uses `blocking / major / minor / nit` across review
  agents, and `Mandatory / Highly Recommended / Recommended / Optional` in
  PRISMA-trAIce. Devil's Advocate has explicit `Critical` severity that
  blocks pipeline progression.
- **Why it helps:** Vicaya's `Critical Gaps` section is currently
  free-form prose. Tagging each gap with severity (e.g. `blocker` =
  invalidates a load-bearing claim, `gap` = missing perspective,
  `nit` = minor) lets the user prioritise follow-up and lets a future
  agent decide whether to loop back vs. ship.
- **Lands in vicaya:** Reformat `Critical Gaps` template (Phase 7) as a
  small table: `Severity | Claim/perspective | What would close it`.
- **Effort:** small (template + ~5 lines of guidance).
- **Verdict:** **adapt**.

## 3. Anti-patterns table (vicaya-flavoured)
- **Source:** `deep-research/SKILL.md` § "Anti-Patterns" — 7 explicit
  prohibitions with "why it fails / correct behavior" columns
  (confirmation bias, cherry-picking, vibe citing, source-tier inflation,
  etc.). "Vibe citing" — mixing elements from real papers into a
  fabricated reference — is the standout warning.
- **Why it helps:** Vicaya's hard rules cover *spelling* hazards well but
  do not enumerate *scholarship* hazards. Run-log lessons that have already
  been caught (e.g. paraphrasing canon when verbatim was available, citing
  auto-captions, guessing sutta numbers from names — Rule F2 actually
  flags this) deserve a unified Anti-Patterns table near the top of the
  skill, distinct from Hard Rules.
- **Lands in vicaya:** New section "Anti-patterns" between Hard Rules and
  Inputs. 5–7 rows; each row = pattern, why it fails, correct behavior.
- **Effort:** ~40 lines.
- **Verdict:** **adopt** (with Pāḷi-specific patterns: vibe-citing a sutta
  number, paraphrasing when verbatim is available, treating commentary as
  canon, treating a dhamma-talk as primary, citing PED definitions as if
  canonical, etc.).

## 4. Multi-mode dispatch (quick vs. full vs. fact-check vs. lit-review)
- **Source:** ARS `MODE_REGISTRY.md` — 7 deep-research modes with explicit
  word-count targets, agent subsets, and oversight levels. `mode_spectrum.md`
  splits them along Fidelity ↔ Originality.
- **Why it helps:** Vicaya is currently one-size = ~3,500 words. Some real
  user questions only need a fact-check ("Is *X* actually in MN 60?") or a
  quick brief ("Five suttas on metta") — running the full 7-phase pipeline
  is over-investment. A `quick` mode (skip Phase 4b YouTube, skip Phase 6
  cross-check, target ~1,000 words) and a `fact-check` mode (Phase 2 only,
  with `resolve-citation`) would cover the cheap end.
- **Lands in vicaya:** New section "Modes" between Setup and Phases.
  Default = `full` (current behavior). Define `quick`, `fact-check`,
  `lit-review` (existing vault notes only) in 3–4 lines each, naming which
  phases to run and which to skip.
- **Effort:** medium. Mostly documentation; the phases themselves don't
  change.
- **Verdict:** **adapt** — but only if the user actually has different
  use-cases. **Discuss before committing**, since a single mode is much
  simpler to maintain.

## 5. Socratic mode (when the user's question is vague)
- **Source:** `deep-research/agents/socratic_mentor_agent.md` + 5-layer
  dialogue (Clarification → Assumption Probing → Evidence → Viewpoint →
  Implication). Default rule: "When intent is ambiguous between socratic
  and full, prefer socratic."
- **Why it helps:** Many `/vicaya <question>` invocations are
  under-specified (e.g. "research on rebirth"). Currently vicaya plunges
  into a 7-phase run; a 2-3 question clarification pass at the top would
  prevent expensive miscalibrated runs.
- **Lands in vicaya:** New short phase "Phase 0 — Scope check". *Only*
  triggered when the question is single-noun or single-verb. If specific
  (sutta name, technical term, perspective dispute), skip straight to
  Phase 1.
- **Effort:** small. ~15 lines, plus a trigger heuristic.
- **Verdict:** **adapt** (lightweight — one round of clarifying
  questions, not 5 layers of Socratic dialogue).

## 6. Source quality tiers explicit to Pāḷi research
- **Source:** `deep-research/references/source_quality_hierarchy.md` —
  formal 7-level evidence pyramid; `source_verification_agent.md` grades
  every source.
- **Why it helps:** Vicaya implicitly weights canon > commentary > modern
  scholarship > Dhamma talk > YouTube auto-caption, but never says so. A
  reader of the vault note cannot tell whether a claim rests on
  Buddhaghosa or on a 3-minute YouTube clip without reading the citation.
- **Lands in vicaya:** New "Evidence tiers" table in SKILL.md, plus a
  one-letter tier marker in the Evidence section headings (e.g. "Canon
  Evidence (T1)", "Commentary (T2)", "Modern scholarship (T3)",
  "Teacher talks (T4)").
- **Effort:** ~20 lines + minor template change.
- **Verdict:** **adapt**. The Theravāda hierarchy is non-trivial (e.g.
  Theras vs. Buddhaghosa vs. Ñāṇavīra) — write it explicitly so the agent
  doesn't have to invent it each run.

## 7. Footnote / locator anchor for every claim ("claim-faithfulness gate")
- **Source:** `POSITIONING.md` §"L3 claim-faithfulness gate" — every cited
  source must carry a per-citation locator anchor; opt-in audit verifies
  the source actually supports the claim made of it.
- **Why it helps:** Vicaya already requires citations (Hard Rule 6) and
  inline footnote markers. What ARS adds is the *audit pass*: a second
  walk where each footnote is re-opened and the claim it supports is
  re-checked against the source text. This is the single highest-leverage
  hallucination defense in ARS.
- **Lands in vicaya:** Phase 6 (currently Gemini cross-check) gains a
  step: before piping to Gemini, walk every `[^*]` footnote in the draft;
  for each, run `resolve-citation` (canon), grep the Calibre snippet, or
  re-read the cached YouTube transcript and confirm the claim is
  supported. Log mismatches in scratchpad and either fix or move to
  Critical Gaps.
- **Effort:** medium. Adds ~25 lines to Phase 6 and probably 2–5 minutes
  per run.
- **Verdict:** **adopt**. This is the most concretely valuable lift.

## 8. Cross-model verification: keep, but improve the prompt
- **Source:** `shared/cross_model_verification.md` — Claude (primary) +
  GPT-5.4 Pro or Gemini 3.1 Pro (verifier). Notes that 31% of citations
  failed when checked across models vs. same-model checks. Explicitly
  warns the protocol cannot solve frame-lock or sycophancy.
- **Why it helps:** Vicaya already does Gemini cross-check in Phase 6;
  the *idea* is validated. ARS's lift is the per-claim style of review
  rather than free-form. A more pointed prompt — "for each footnote
  marker, name one alternative interpretation OR one factual concern OR
  pass" — would yield more actionable feedback than the current
  freeform "identify any factual errors".
- **Lands in vicaya:** Rewrite the Phase 6 cross-check prompt template
  in SKILL.md to walk the footnotes structurally.
- **Effort:** small (~10 lines).
- **Verdict:** **adapt**.

## 9. "Handoff schema" for downstream use of the vault note
- **Source:** `shared/handoff_schemas.md` — every artifact passed between
  pipeline stages has a named schema with required + optional fields.
- **Why it helps:** Vicaya notes are read by future vicaya runs (Phase 1
  vault search) and by the user. The current frontmatter is good
  (`canon_refs`, `library_refs`, `web_refs`) but doesn't capture
  `perspective_map`, `angles_pursued`, `angles_not_pursued`,
  `critical_gaps_count`, `tier_distribution`. Surfacing these in
  frontmatter would let future searches filter ("notes that already cover
  the cessationist position", "notes where the archaeology angle was
  pursued").
- **Lands in vicaya:** Extend frontmatter spec in Phase 7. Add fields
  `perspectives`, `angles`, `gaps_count`.
- **Effort:** small. Frontmatter rules already exist; this adds 3 more
  fields with the same quoting conventions.
- **Verdict:** **adopt**.

## 10. Reflection → lessons.md → SKILL.md improvement loop is *almost* identical to ARS — but ARS publishes the lessons
- **Source:** ARS doesn't have an exact match, but `CHANGELOG.md` and
  per-skill `references/changelog.md` are pulled from accumulated
  reflections. ARS surfaces lessons publicly; vicaya keeps them in
  `kamma/runs/*.md` per-run.
- **Why it helps:** Vicaya already has the reflection forcing function.
  What's missing is a *periodic distillation* — every ~10 runs, walk
  `kamma/runs/` and promote recurring lessons into SKILL.md or
  `tools/research_sources.py`. ARS does this manually; for vicaya it
  could be a separate slash command (`/vicaya-distill`) that reads the
  last 10 reflections and proposes hard-rule additions.
- **Lands in vicaya:** Either a new section in SKILL.md ("Distillation
  cadence: every ~10 runs") or a new sibling skill/command. Not in
  per-run SKILL.md execution path.
- **Effort:** medium if you want the command; small if just a
  cadence note.
- **Verdict:** **adapt** (cadence note now; command later if useful).

## 11. Failure-paths table
- **Source:** `deep-research/references/failure_paths.md` — 12 scenarios
  with trigger condition + recovery strategy in one table.
- **Why it helps:** Vicaya already has a "When something fails" section,
  but it's a flat list. A table with `Failure | Trigger | Recovery` lets
  the agent grep faster mid-run. Also, vicaya's coverage is mostly
  tool-level (helper crashes, Obsidian missing); ARS-style failure paths
  also cover *research-level* failures (insufficient sources, perspective
  unverifiable, only one school represented). Vicaya could add the
  research-level ones.
- **Lands in vicaya:** Reformat "When something fails" as a table; add
  4–6 research-level rows (e.g. "Only one perspective surfaced after
  counter-search → flag in Critical Gaps as `unverified`, do not write the
  note as if balanced").
- **Effort:** small.
- **Verdict:** **adopt**.

## 12. Style profile (your voice)
- **Source:** `academic-paper`'s Style Calibration — extract sentence
  length, paragraph length, idiom usage from past papers and apply as
  soft guide for new writing. ARS's `style_calibration_protocol.md`.
- **Why it helps:** Vicaya notes currently have one voice — the agent's
  default register. If the user wants the vault to read consistently
  across years, calibrating against past notes would help. But this is
  expensive to do well and easy to do badly.
- **Lands in vicaya:** Optional Phase 5b — read 3–5 recent vault notes
  before drafting and mirror sentence length, blockquote-to-prose ratio,
  formality level.
- **Effort:** medium.
- **Verdict:** **skip for now**. The note structure is already
  templated; voice consistency is a smaller win than the citation-audit
  gate (item 7) or the anti-patterns table (item 3). Revisit if the user
  reports tone drift across notes.

## 13. RAISE 4 principles as "operating principles" preamble
- **Source:** `shared/raise_framework.md` — Human oversight, Transparency,
  Reproducibility, Fit-for-purpose.
- **Why it helps:** Vicaya's `agent` frontmatter and footer line cover
  *transparency* and *reproducibility* (model identity). It does not
  cover *human oversight* (the user is reading the note, not approving
  it mid-flow) or *fit-for-purpose* (no per-tool justification).
- **Lands in vicaya:** N/A — RAISE is biomedical evidence synthesis. The
  underlying *principles* are already implicit in Hard Rules 1, 2, 6.
- **Verdict:** **skip**. Too biomedical-flavored; over-engineering for a
  single-agent scholarship workflow.

## 14. Phase-boundary blocks for the agent ("you may not write Phase N+1 deliverables")
- **Source:** Every ARS agent has a `Phase Boundary (v3.9.2)` block:
  "you MUST NOT write files in `phase{M}_*/` directories where M ≠ N".
- **Why it helps:** Marginally — vicaya's phases are sequential within
  one agent, not parallel across agents, so cross-phase leakage isn't
  the same risk. But the *pattern* of "after each phase, write the
  deliverable to disk before moving on" already exists in the
  scratchpad. Worth reinforcing: each `→ Scratch — append Phase N
  results` line could be promoted to a hard rule ("Phase N is not done
  until the scratchpad append is written").
- **Lands in vicaya:** One sentence added to the scratchpad section.
- **Effort:** tiny.
- **Verdict:** **adapt** (tighten existing guidance, don't add
  machinery).

## 15. PRISMA-style flow diagram for canon search
- **Source:** PRISMA 2020 flow diagram — Identified → Screened →
  Eligible → Included, with reasons for exclusion at each step.
- **Why it helps:** When Phase 2 yields 50 canon hits and the final
  note cites 12, the other 38 currently live in `## Sources
  Investigated, Not Used` (which is good). A counts-only flow at the
  top of that section ("50 hits → 22 deduped → 18 in-scope → 12 cited")
  would let the reader see how aggressive the filtering was at a
  glance.
- **Lands in vicaya:** Add 1 line of counts to the top of `## Sources
  Investigated, Not Used`.
- **Effort:** tiny.
- **Verdict:** **adopt** (cheapest possible win; pure documentation).

## 16. "Iron rule" terminology + visual marker
- **Source:** ARS uses `⚠️ IRON RULE:` as an unmissable inline marker
  for unbreakable constraints (every claim cited, gray-zone = FAIL,
  ethics can halt, never give direct answers in Socratic mode).
- **Why it helps:** Vicaya numbers Hard Rules 1–10. ARS's IRON RULE
  notation flags *the most important rules across the body of the
  skill* — not just the top section. Useful when later phases restate
  a constraint (e.g. Phase 7's "no AI/model attribution in scholarship
  body" is a restatement of Hard Rule 1).
- **Lands in vicaya:** Adopt the `⚠️ IRON RULE:` prefix in 4–5 places
  where the existing prose restates a Hard Rule.
- **Effort:** tiny.
- **Verdict:** **adopt**.

---

## Items considered and rejected

- **Multi-agent orchestration** (13 agents, parallel review). Skip — vicaya
  is single-agent by design, and the portability constraint (Claude /
  Codex / Gemini) makes multi-agent infra a bad fit.
- **FINER scoring of the research question**. Skip — FINER is biomedical;
  the equivalent for Pāḷi is "is the term well-defined, are the texts
  available, is the perspective dispute live, is the question doctrinal
  or hermeneutical." Item 5 (lightweight scope check) covers the same
  ground without the formalism.
- **PRISMA-trAIce 17-item checklist, RoB 2, GRADE, meta-analysis**. Skip
  — biomedical evidence machinery; no Pāḷi analogue.
- **Ethics review agent** (AI disclosure, dual-use, IRB). Skip — vicaya
  already discloses agent identity in frontmatter; dual-use and IRB are
  not relevant to canonical research.
- **`compliance_agent` with override ladder**. Skip — gating mechanism
  needs an institutional context; vicaya's user is the only stakeholder.
- **Material Passport / cross-session resume**. Skip — vicaya runs are
  single-session by design; the scratchpad already covers compaction
  rescue.
- **`pipeline_orchestrator_agent`**. Skip — same reason as multi-agent.
