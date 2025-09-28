#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rewrite image and intra-volume links in docs/volume-1/*.md to use Jekyll relative_url.

- Images:
  ![alt](/docs/assets/volume-1/xxx.png)
  ![alt](/notes-of-feynman-lectures-on-physics/assets/volume-1/xxx.png)
  => ![alt]({{"/assets/volume-1/xxx.png"|relative_url}})

- Paragraph links:
  [Fig](/docs/volume-1/path/file.md#anchor)
  [Fig](/notes-of-feynman-lectures-on-physics/volume-1/path/file.html#anchor)
  => [Fig]({{"/volume-1/path/file.html#anchor"|relative_url}})

Safeguards:
- Skips fenced code blocks (``` or ~~~).  
- Idempotent: only matches legacy prefixes (/docs, /notes-of-feynman-lectures-on-physics).  
"""  

from pathlib import Path  
import argparse  
import re  
import sys  

# Fenced code blocks  
FENCE_PATTERN = re.compile(r'^\s*(?:`{3,}|~{3,})')  

# Image links with old prefixes  
IMG_PATTERN = re.compile(  
    r'!\[([^\]]*)\]\('  
    r'\s*(?:/docs|/notes-of-feynman-lectures-on-physics)/assets/'  
    r'(volume-1/[^\s)"]+)'  
    r'(?:\s+"[^"]*")?\s*\)'  
)  

# Paragraph links with old prefixes (normalize extension to .html, keep anchor)  
LINK_PATTERN = re.compile(  
    r'\[([^\]]+)\]\('  
    r'\s*(?:/docs|/notes-of-feynman-lectures-on-physics)/volume-1/'  
    r'([^)#\s]+?)'  
    r'\.(?:md|markdown|html)'  
    r'(#[^) \t]+)?'  
    r'\s*\)'  
)  

def rewrite_line(line: str) -> tuple[str, bool]:  
    changed = False  

    def repl_img(m: re.Match) -> str:  
        nonlocal changed  
        alt = m.group(1)  
        path = m.group(2)  # volume-1/...  
        changed = True  
        # 用拼接直接写入 {{ ... }}，避免被格式化压扁  
        return f'![{alt}]('+'{{"/assets/'+path+'"|relative_url}}'+')'  

    def repl_link(m: re.Match) -> str:  
        nonlocal changed  
        label = m.group(1)  
        path_no_ext = m.group(2)  
        anchor = m.group(3) or ''  
        changed = True  
        inner = path_no_ext + '.html' + anchor  
        return f'[{label}]('+'{{"/volume-1/'+inner+'"|relative_url}}'+')'  

    new_line = IMG_PATTERN.sub(repl_img, line)  
    if new_line != line:  
        line = new_line  

    new_line = LINK_PATTERN.sub(repl_link, line)  
    if new_line != line:  
        line = new_line  

    return line, changed  

def transform_text(text: str) -> tuple[str, bool]:  
    lines = text.splitlines(keepends=True)  
    out = []  
    in_fence = False  
    any_change = False  

    for ln in lines:  
        if FENCE_PATTERN.match(ln):  
            in_fence = not in_fence  
            out.append(ln)  
            continue  

        if in_fence:  
            out.append(ln)  
            continue  

        new_ln, changed = rewrite_line(ln)  
        if changed:  
            any_change = True  
        out.append(new_ln)  

    return ''.join(out), any_change  

def main():  
    ap = argparse.ArgumentParser(description="Fix image and paragraph links in docs/volume-1/*.md")  
    ap.add_argument("--docs-dir", default=None, help="Path to docs directory (default: <repo_root>/docs)")  
    ap.add_argument("--volume", default="volume-1", help="Volume subdirectory under docs (default: volume-1)")  
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")  
    args = ap.parse_args()  

    repo_root = Path(__file__).resolve().parents[1]  
    docs_dir = Path(args.docs_dir) if args.docs_dir else repo_root / "docs"  
    target_dir = docs_dir / args.volume  

    if not target_dir.exists():  
        print(f"[ERROR] target directory not found: {target_dir}", file=sys.stderr)  
        sys.exit(1)  

    md_files = sorted(target_dir.rglob("*.md"))  
    if not md_files:  
        print(f"[INFO] No markdown files found under {target_dir}")  
        return  

    modified = 0  
    for p in md_files:  
        try:  
            original = p.read_text(encoding="utf-8")  
        except UnicodeDecodeError:  
            original = p.read_text(encoding="utf-8", errors="ignore")  

        updated, changed = transform_text(original)  
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
    