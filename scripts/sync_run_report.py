"""Synchronize the latest Vicaya run report to the appropriate GitHub branch."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from rich import print as rprint


project_root = Path(__file__).resolve().parent.parent
GitRunner = Callable[[list[str], Path], subprocess.CompletedProcess]


def load_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        values[key] = val
        os.environ.setdefault(key, val)
    return values


def run_git(args: list[str], repo_path: Path) -> subprocess.CompletedProcess:
    cmd = ["git", "-C", str(repo_path)] + args
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def upstream_remote_and_branch(repo_path: Path, runner: GitRunner) -> tuple[str, str] | None:
    try:
        result = runner(
            ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            repo_path,
        )
    except subprocess.CalledProcessError:
        return None

    upstream = result.stdout.strip()
    if "/" not in upstream:
        return None
    remote, branch = upstream.split("/", 1)
    if not remote or not branch:
        return None
    return remote, branch


def target_remote_and_branch(
    user: str, repo_path: Path, runner: GitRunner
) -> tuple[str, str] | None:
    if user == "primary":
        return "origin", "main"
    return upstream_remote_and_branch(repo_path, runner)


def is_dirty_rebase_error(exc: subprocess.CalledProcessError) -> bool:
    text = "\n".join(part for part in (str(exc.stdout), str(exc.stderr)) if part)
    return (
        "cannot pull with rebase" in text
        and "unstaged changes" in text
    )


def pull_rebase(
    repo_path: Path, remote: str, branch: str, runner: GitRunner
) -> None:
    try:
        runner(["pull", "--rebase", remote, branch], repo_path)
    except subprocess.CalledProcessError as exc:
        if is_dirty_rebase_error(exc):
            rprint(
                "[red]Dirty worktree: commit or stash your other changes "
                "before syncing run reports.[/red]"
            )
        raise


def porcelain_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.rsplit(" -> ", 1)[1]
    return path


def uncommitted_today_reports(
    repo_path: Path, runner: GitRunner, today_prefix: str
) -> list[str]:
    status = runner(["status", "--porcelain", "--", "runs"], repo_path)
    reports: list[str] = []
    for raw in status.stdout.splitlines():
        path = porcelain_path(raw)
        name = Path(path).name
        if (
            path.startswith("runs/")
            and name.startswith(today_prefix)
            and name.endswith(".md")
        ):
            reports.append(path)
    return sorted(set(reports))


def sync_latest_report(
    repo_path: Path = project_root,
    run_git: GitRunner = run_git,
    today_prefix: str | None = None,
) -> int:
    env = load_dotenv(repo_path / ".env")
    today = today_prefix or datetime.now().strftime("%Y%m%d")

    user = env.get("VICAYA_USER") or os.environ.get("VICAYA_USER")
    if not user:
        rprint("[red]Error: VICAYA_USER not found in .env[/red]")
        return 1

    target = target_remote_and_branch(user, repo_path, run_git)
    if target is None:
        rprint("[red]Error: No upstream configured for current branch; set one before syncing reports.[/red]")
        return 1

    remote, branch = target

    try:
        rprint("[cyan]Git pull --rebase...[/cyan]", end=" ")
        pull_rebase(repo_path, remote, branch, run_git)
        rprint("[green]ok[/green]")

        report_rels = uncommitted_today_reports(repo_path, run_git, today)
        if not report_rels:
            rprint(f"[yellow]No uncommitted run reports for {today}; no push needed.[/yellow]")
            return 0

        rprint(f"[cyan]Git add {len(report_rels)} run report(s)...[/cyan]", end=" ")
        run_git(["add", *report_rels], repo_path)
        rprint("[green]ok[/green]")

        status = run_git(["status", "--porcelain", "--", *report_rels], repo_path)
        if not status.stdout.strip():
            rprint(f"[yellow]Run reports for {today} already synced; no push needed.[/yellow]")
            return 0

        rprint("[cyan]Git commit...[/cyan]", end=" ")
        run_git(["commit", "-m", f"chore: update runs {user}"], repo_path)
        rprint("[green]ok[/green]")

        rprint(f"[cyan]Git push {remote} HEAD:{branch}...[/cyan]", end=" ")
        run_git(["push", remote, f"HEAD:{branch}"], repo_path)
        rprint("[green]ok[/green]")
        rprint(f"[green]Successfully synced {len(report_rels)} run report(s) for {today}[/green]")
        return 0
    except subprocess.CalledProcessError as exc:
        rprint("[red]failed[/red]")
        rprint(f"[red]Git command failed: git {' '.join(str(part) for part in exc.cmd)}[/red]")
        if exc.stdout:
            print(exc.stdout)
        if exc.stderr:
            print(exc.stderr)
        return exc.returncode


def main() -> None:
    sys.exit(sync_latest_report())


if __name__ == "__main__":
    main()
