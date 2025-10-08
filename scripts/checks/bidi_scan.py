#!/usr/bin/env python3
import sys
from pathlib import Path

BIDI_CHARS = [
    "\u202A", "\u202B", "\u202C", "\u202D", "\u202E",
    "\u2066", "\u2067", "\u2068", "\u2069",
]

def check_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for ch in BIDI_CHARS:
        if ch in text:
            print(f"BIDI control character {ord(ch):04x} found in {path}")
            return 1
    return 0

def main():
    paths = sys.argv[1:] or ["."]
    rc = 0
    for p in paths:
        for path in Path(p).rglob("*"):
            if path.is_file():
                rc |= check_file(path)
    sys.exit(rc)

if __name__ == "__main__":
    main()
