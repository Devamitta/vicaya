# Spec — Vicaya Notes: Private GitHub Repository

## Overview
Turn the Obsidian Vicaya research-notes folder into a private GitHub repository
(`bdhrs/vicaya-notes`) so that a collaborator (`devamitta` on GitHub) can sync the
notes into their own Obsidian vault without relying on MEGAsync (which has a known
Mac bug with incoming shared folders).

## Source folder
`~/MyFiles/Obsidian/Vicaya/`
- 42 Markdown research notes (YYYY-MM-DD - slug.md)
- `PDF/` subfolder — 34 generated PDFs (excluded from the repo; the collaborator
  needs only the Markdown files)

## What it should do
1. Initialise a Git repository in `~/MyFiles/Obsidian/Vicaya/`.
2. Add a `.gitignore` that excludes the `PDF/` subfolder and common OS junk.
3. Add a minimal `README.md` identifying the repo.
4. Commit all Markdown notes as the initial commit.
5. Create the private GitHub repo `bdhrs/vicaya-notes` (via `gh repo create`).
6. Push the local repo to `origin`.
7. Add `devamitta` as a collaborator with `push` (write) access via `gh`.
8. Update `SKILL.md` so that after every successful PDF generation, the skill
   automatically `git add`s the new note, commits it, and pushes to `origin` —
   failing silently (logged in the run summary) if git is unavailable or the push fails.

## Assumptions & uncertainties
- The vault path is confirmed: `~/MyFiles/Obsidian/Vicaya/`.
- PDFs are generated artefacts and are excluded to keep the repo small.
- `gh` CLI is authenticated and the user has permission to create repos under `bdhrs/`.
- The collaborator's GitHub handle is exactly `devamitta`.
- The repo name `vicaya-notes` is confirmed by the user.
- The skill auto-push uses the git repo at `$VICAYA_VAULT_PATH/Vicaya/` (derived from
  the existing env var; no new env var needed).
- Auto-push failures are non-fatal — noted in the run summary but never block note delivery.

## Constraints
- NEVER commit without explicit user instruction — the plan will stage and prepare,
  then present the commit command for the user to run (or ask for explicit approval).
- Repo must be private.
- No sensitive data (vault passwords, `.env`) in the folder — confirmed, no such files.
- Do not touch any other folder inside the Obsidian vault.

## How we'll know it's done
- `gh repo view bdhrs/vicaya-notes` returns the repo metadata.
- `git -C ~/MyFiles/Obsidian/Vicaya log --oneline` shows the initial commit.
- `gh api repos/bdhrs/vicaya-notes/collaborators` includes `devamitta`.
- The collaborator can `git clone` the repo and open the notes in Obsidian.
- A test `/vicaya` run results in an automatic commit visible on GitHub.

## What's not included
- Syncing going forward (the collaborator will `git pull`; no automation is set up here).
- CI/CD, GitHub Actions.
- Any changes to the vicaya research-tool project itself.
