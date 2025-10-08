#!/usr/bin/env python3
"""Simple doc-sync checker: verifies referenced paths in README exist.

This is intentionally small: it scans README.md for backticked paths and verifies they exist.
"""
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
paths = re.findall(r"`([^`]+)`", text)
missing = []
for p in set(paths):
    if p.startswith("http"):
        continue
    candidate = ROOT / p
    if not candidate.exists():
        missing.append(p)

if missing:
    print("Doc-sync check failed. Missing paths:")
    for m in missing:
        print(" - ", m)
    sys.exit(2)
print("Doc-sync check passed")
