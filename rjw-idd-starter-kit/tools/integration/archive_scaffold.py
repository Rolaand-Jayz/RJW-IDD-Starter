"""Scaffold integration transcript archive directories."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

TEMPLATE_CONTEXT = """# Integration Context\n\n- **Services:**\n- **Contracts:**\n- **Environments:**\n- **Linked IDs:** <add IDs here>\n"""

TEMPLATE_VERIFICATION = """# Verification\n\n- Contract tests: \n- Manual sign-off: \n- Observability snapshot: \n"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "task_slug",
        help="Task slug appended to today's date (e.g. payments-sync)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root (default: project root)",
    )
    return parser.parse_args()


def scaffold(root: Path, slug: str) -> Path:
    archive_root = root / "artifacts" / "integration" / "transcript-archive"
    archive_root.mkdir(parents=True, exist_ok=True)
    directory_name = f"{date.today()}-{slug}"
    target_dir = archive_root / directory_name
    target_dir.mkdir(exist_ok=True)

    context_file = target_dir / "context.md"
    if not context_file.exists():
        context_file.write_text(TEMPLATE_CONTEXT, encoding="utf-8")

    prompts_file = target_dir / "prompts.log"
    prompts_file.touch()

    diffs_dir = target_dir / "diffs"
    diffs_dir.mkdir(exist_ok=True)

    verification_file = target_dir / "verification.md"
    if not verification_file.exists():
        verification_file.write_text(TEMPLATE_VERIFICATION, encoding="utf-8")

    return target_dir


def main() -> int:
    args = parse_args()
    target = scaffold(args.root.resolve(), args.task_slug)
    print(target)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
