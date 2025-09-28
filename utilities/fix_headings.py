#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demote the first H1 (# ) to H2 (## ) in every docs/**/index.md.
- Skips YAML front matter.
- Skips fenced code blocks.
- Only changes the first H1 after front matter.
- Idempotent.
"""

from pathlib import Path
import re
import argparse
import sys

H1_PATTERN = re.compile(r'^(\s*)#(?!#)\s+([^\r\n]*\S[^\r\n]*)(\r?\n)?')
FENCE_PATTERN = re.compile(r'^\s*(?:`{3,}|~{3,})')

def demote_first_h1(text: str) -> tuple[str, bool]:
    lines = text.splitlines(keepends=True)
    i = 0
    n = len(lines)

    # Skip YAML front matter
    if n > 0 and lines[0].lstrip().startswith('---'):
        i = 1
        while i < n:
            if lines[i].lstrip().startswith('---'):
                i += 1
                break
            i += 1

    changed = False
    in_fence = False

    while i < n:
        line = lines[i]

        if FENCE_PATTERN.match(line):
            in_fence = not in_fence
            i += 1
            continue

        if not in_fence:
            m = H1_PATTERN.match(line)
            if m:
                indent, heading_text, nl = m.groups()
                nl = nl if nl is not None else '\n'
                lines[i] = f"{indent}## {heading_text}{nl}"
                changed = True
                break

        i += 1

    return ("".join(lines), changed)

def main():
    parser = argparse.ArgumentParser(
        description="Demote the first H1 to H2 in docs/**/index.md",
    )
    parser.add_argument("--docs-dir", default=None,
                        help="Path to docs directory (default: <repo_root>/docs)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would change but do not write files")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    docs_dir = Path(args.docs_dir) if args.docs_dir else repo_root / "docs"

    if not docs_dir.exists():
        print(f"[ERROR] docs directory not found: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    targets = sorted(docs_dir.rglob("index.md"))
    if not targets:
        print("[INFO] No index.md files found under", docs_dir)
        return

    modified = 0
    for p in targets:
        try:
            original = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            original = p.read_text(encoding="utf-8", errors="ignore")

        updated, changed = demote_first_h1(original)
        if changed:
            print(f"[CHANGE] {p.relative_to(repo_root)}")
            if not args.dry_run:
                p.write_text(updated, encoding="utf-8")
            modified += 1

    if args.dry_run:
        print(f"[DRY-RUN] files to be modified: {modified}")
    else:
        print(f"[DONE] modified files: {modified}")

if __name__ == "__main__":
    main()