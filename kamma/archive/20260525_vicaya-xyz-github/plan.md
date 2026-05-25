# Plan — Vicaya Notes: Private GitHub Repository

## Architecture Decisions
- **Repo location:** init git directly in `~/MyFiles/Obsidian/Vicaya/` (not a clone
  elsewhere), so the working tree IS the vault subfolder — no extra sync step needed.
- **PDFs excluded:** `PDF/` is in `.gitignore`; generated files add no value for the
  collaborator and would inflate the repo.
- **Collaborator access:** `push` (write) rather than `pull` (read) so the collaborator
  can eventually contribute notes back if desired. Downgrade to read-only if preferred.
- **No automation:** `git pull` on the collaborator's side is manual; this keeps the
  setup simple and avoids cron/webhook complexity.

## Phase 1 — Prepare the local repo

- [ ] Create `~/MyFiles/Obsidian/Vicaya/.gitignore` with `PDF/` and OS junk entries
  → verify: file exists, contains `PDF/`

- [ ] Create `~/MyFiles/Obsidian/Vicaya/README.md` (minimal — one paragraph)
  → verify: file exists and is valid Markdown

- [ ] `git init` in `~/MyFiles/Obsidian/Vicaya/`
  → verify: `git -C ~/MyFiles/Obsidian/Vicaya status` shows untracked files, no error

- [ ] Stage all Markdown files and the two new files
  → verify: `git -C ~/MyFiles/Obsidian/Vicaya status` shows 44 files staged, PDF/ absent

- [ ] **Phase 1 verification:** `git -C ~/MyFiles/Obsidian/Vicaya diff --cached --stat`
  shows only `.md` files (no PDFs)

## Phase 2 — Create the GitHub repo and push

- [ ] `gh repo create bdhrs/vicaya-notes --private --source=~/MyFiles/Obsidian/Vicaya --remote=origin`
  → verify: `gh repo view bdhrs/vicaya-notes` returns repo metadata

- [ ] Make the initial commit (user approval required — present commit command, do not run)
  → verify: user runs the commit; `git -C ~/MyFiles/Obsidian/Vicaya log --oneline` shows 1 commit

- [ ] `git -C ~/MyFiles/Obsidian/Vicaya push -u origin main`
  → verify: `gh repo view bdhrs/vicaya-notes --json pushedAt` shows a recent timestamp

## Phase 3 — Add collaborator

- [ ] `gh api repos/bdhrs/vicaya-notes/collaborators/devamitta -X PUT -f permission=push`
  → verify: `gh api repos/bdhrs/vicaya-notes/collaborators` includes `devamitta`

- [ ] **Phase 3 verification:** Confirm collaborator invite was sent

## Phase 4 — Update SKILL.md to auto-push after PDF generation

Insertion point: `skill/vicaya/SKILL.md`, immediately after the `PDF generation` section
(after "Include the PDF path in the Section 1 run summary if generation succeeded."),
before `## Final report to the user`.

- [ ] Add a `### GitHub push (run after successful PDF generation)` section to SKILL.md
  The section instructs the skill to:
  1. Derive the notes repo path: `Path(vault_path).expanduser() / "Vicaya"` where
     `vault_path` comes from `VICAYA_VAULT_PATH` (already loaded in the PDF script env).
  2. Run the following shell commands via `subprocess` (or as Bash steps):
     ```
     git -C <notes_repo> add "<today> - <slug>.md"
     git -C <notes_repo> commit -m "note: <today> - <slug>"
     git -C <notes_repo> push origin HEAD
     ```
  3. If any command fails (non-zero exit), log `GitHub push skipped: <error>` in the
     Section 1 run summary. Never raise or abort.
  → verify: section is present in SKILL.md, insertion point is correct, logic is sound

## Phase 5 — Handoff instructions

- [ ] Draft clone instructions for `devamitta` to share (SSH and HTTPS variants)
  → verify: instructions are correct and complete
