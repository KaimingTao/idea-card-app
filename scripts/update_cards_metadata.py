#!/usr/bin/env python3
"""Update src/cards-metadata.js with the latest timestamp from data/cards.md."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys


def run_git_timestamp(target: Path, cwd: Path) -> datetime | None:
    """Return the latest commit timestamp for *target* as a datetime in UTC."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cI', '--', str(target)],
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    value = result.stdout.strip()
    if not value:
        return None

    # Python's fromisoformat doesn't accept trailing Z, so normalize first.
    normalized = value[:-1] + '+00:00' if value.endswith('Z') else value
    try:
        return datetime.fromisoformat(normalized).astimezone(timezone.utc)
    except ValueError:
        return None


def filesystem_timestamp(target: Path) -> datetime:
    """Return the filesystem mtime of *target* as a datetime in UTC."""
    return datetime.fromtimestamp(target.stat().st_mtime, tz=timezone.utc)


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def update_metadata(cards_path: Path, metadata_path: Path, repo_root: Path) -> tuple[bool, str]:
    timestamp = run_git_timestamp(cards_path, repo_root)
    if timestamp is None:
        timestamp = filesystem_timestamp(cards_path)

    formatted = format_timestamp(timestamp)
    desired_content = f"export const cardsLastModified = '{formatted}';\n"

    current_content = metadata_path.read_text(encoding='utf-8') if metadata_path.exists() else ''
    if current_content == desired_content:
        return False, formatted

    metadata_path.write_text(desired_content, encoding='utf-8')
    return True, formatted


def main() -> int:
    app_dir = Path(__file__).resolve().parents[1]
    cards_path = (app_dir / '../data/cards.md').resolve()
    metadata_path = app_dir / 'src/cards-metadata.js'

    if not cards_path.exists():
        print(f'cards file not found: {cards_path}', file=sys.stderr)
        return 1

    changed, formatted = update_metadata(cards_path, metadata_path, app_dir)
    prefix = 'Updated' if changed else 'Already current'
    print(f'{prefix} cardsLastModified -> {formatted}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
