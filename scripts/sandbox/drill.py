#!/usr/bin/env python3
"""CLI wrapper for sandbox breach drill automation."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from tools.sandbox.drill import main


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
