"""Validate a final Vicaya note before publication."""

from __future__ import annotations

import argparse
import importlib.util
import os
import sys
from pathlib import Path

try:
    from tools import note_checks
except ModuleNotFoundError:
    spec = importlib.util.spec_from_file_location(
        "note_checks",
        Path(__file__).resolve().parents[1] / "tools" / "note_checks.py",
    )
    if spec is None or spec.loader is None:
        raise
    note_checks = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = note_checks
    spec.loader.exec_module(note_checks)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("note", help="Note path or Vicaya-relative note path")
    args = parser.parse_args(argv)

    env = {**note_checks.load_dotenv(Path(".env")), **os.environ}
    note_arg = str(args.note)
    try:
        note_path = _resolve_note_arg(note_arg, env)
        issues = note_checks.validate_note_file(note_path)
    except OSError as exc:
        print(f"{note_arg}: error: {exc}")
        return 2
    except ValueError as exc:
        print(f"{note_arg}: error: {exc}")
        return 2

    for issue in issues:
        print(f"{note_path}:{issue.line}: {issue.code}: {issue.message}")
    return 1 if issues else 0


def _resolve_note_arg(note_arg: str, env: dict[str, str]) -> Path:
    raw_path = Path(note_arg).expanduser()
    if raw_path.is_absolute():
        note_path = raw_path
    else:
        vault_path = env.get("VICAYA_VAULT_PATH", "").strip()
        if not vault_path:
            raise ValueError("VICAYA_VAULT_PATH is required for relative note paths")
        note_path = note_checks.resolve_note_path(note_arg, Path(vault_path))
    if not note_path.exists():
        raise OSError(f"note not found: {note_path}")
    return note_path


if __name__ == "__main__":
    raise SystemExit(main())
