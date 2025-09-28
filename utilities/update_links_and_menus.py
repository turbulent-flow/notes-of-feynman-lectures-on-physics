#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix absolute links to Jekyll-relative Liquid URLs, generate missing chapter index.md,
and (only when missing) generate front matter/heading. Respect existing front matter.

Highlights:
- Convert /docs/assets/... -> {{ "/assets/..." | relative_url }}
- Convert /docs/volume-.../*.md[#anchor] -> {{ "/volume-.../*.html[#anchor]" | relative_url }}
- Skip fenced code blocks (``` or ~~~)  
- Existing front matter (FM): do NOT modify any keys (including title casing)  
- Missing FM: generate minimal FM for index.md and section md  
- For index.md body: insert H2 only if there is NO H2 at all  
- Auto-create missing index.md under docs/volume-*/<N-chapter-slug>/ with proper FM and H2  
- Idempotent  

Assumptions:  
- Docs under <repo_root>/docs (override via --docs-dir)  
- Volume path: docs/volume-<X>/  
- Chapter path: docs/volume-<X>/<N-<chapter-slug>>/  
- Section file: docs/volume-<X>/<chapter-dir>/<N-M-<section-slug>>.md  
"""  

from pathlib import Path  
import argparse  
import re  
import sys  
import os  
from typing import Tuple, Optional, List  

# ---------- Fence (code block) detection ----------  
FENCE_PATTERN = re.compile(r'^\s*(?:`{3,}|~{3,})')  

def split_lines_keepends(text: str) -> List[str]:  
    return text.splitlines(keepends=True)  

# ---------- Link rewriting ----------  

# Basic markdown link/image: !?[alt](dest)  
LINK_PATTERN = re.compile(r'(!?)\[(.*?)\]\(([^)\r\n]+?)\)')  

def _split_dest_and_title(dest: str) -> Tuple[str, Optional[str]]:  
    """  
    Split '(url [title])' into url and optional title (keep original title formatting).  
    """  
    s = dest.strip()  
    if s.startswith('<') and s.endswith('>'):  
        s = s[1:-1].strip()  
    if s.startswith('{{'):  
        return s, None  

    url = []  
    title = None  
    in_single = False  
    in_double = False  
    i = 0  
    while i < len(s):  
        ch = s[i]  
        if ch == "'" and not in_double:  
            in_single = not in_single  
        elif ch == '"' and not in_single:  
            in_double = not in_double  
        if not in_single and not in_double and ch.isspace():  
            break  
        url.append(ch)  
        i += 1  

    url_str = ''.join(url).strip()  
    rest = s[i:].strip()  
    if rest:  
        title = rest  
    return url_str, title  

def _recompose_dest(liquid_expr: str, original_title: Optional[str]) -> str:  
    if original_title:  
        return f'{liquid_expr} {original_title}'  
    return liquid_expr  

def is_docs_asset_path(url: str) -> bool:  
    return url.startswith('/docs/assets/')  

def is_assets_path(url: str) -> bool:  
    return url.startswith('/assets/')  

def is_docs_volume_md(url: str) -> bool:  
    return url.startswith('/docs/volume-') and (url.endswith('.md') or '.md#' in url)  

def to_liquid_relative(path: str) -> str:  
    return f'{{{{ "{path}" | relative_url }}}}'  

def rewrite_one_link(is_image: bool, alt: str, dest: str) -> Tuple[bool, Optional[str]]:  
    url, title = _split_dest_and_title(dest)  

    # Already liquid or external  
    if url.startswith('{{') or '://' in url:  
        return False, None  

    # 1) Assets  
    if is_docs_asset_path(url):  
        new_url = url[len('/docs'):]  # => /assets/...  
        liquid = to_liquid_relative(new_url)  
        new_dest = _recompose_dest(liquid, title)  
        return True, f'{"!" if is_image else ""}[{alt}]({new_dest})'  

    if is_assets_path(url):  
        liquid = to_liquid_relative(url)  
        new_dest = _recompose_dest(liquid, title)  
        return True, f'{"!" if is_image else ""}[{alt}]({new_dest})'  

    # 2) Doc pages (.md -> .html)  
    if is_docs_volume_md(url):  
        path = url[len('/docs'):]  # starts with /volume-...  
        if '.md#' in path:  
            base, anchor = path.split('.md#', 1)  
            new_path = f'{base}.html#{anchor}'  
        elif path.endswith('.md'):  
            new_path = path[:-3] + '.html'  
        else:  
            new_path = path  
        liquid = to_liquid_relative(new_path)  
        new_dest = _recompose_dest(liquid, title)  
        return True, f'{"!" if is_image else ""}[{alt}]({new_dest})'  

    return False, None  

def rewrite_links_in_text(text: str) -> Tuple[str, bool]:  
    lines = split_lines_keepends(text)  
    out = []  
    in_fence = False  
    changed_any = False  

    for ln in lines:  
        if FENCE_PATTERN.match(ln):  
            in_fence = not in_fence  
            out.append(ln)  
            continue  
        if in_fence:  
            out.append(ln)  
            continue  

        def _repl(m):  
            nonlocal changed_any  
            bang, alt, dest = m.group(1), m.group(2), m.group(3)  
            is_image = (bang == '!')  
            changed, replaced = rewrite_one_link(is_image, alt, dest)  
            if changed:  
                changed_any = True  
                return replaced  
            return m.group(0)  

        new_ln = LINK_PATTERN.sub(_repl, ln)  
        out.append(new_ln if new_ln is not None else ln)  

    return ''.join(out), changed_any  

# ---------- Front matter parsing ----------  
FRONT_MATTER_BOUND = re.compile(r'^---\s*')  

def parse_front_matter(text: str) -> Tuple[dict, str, str]:  
    """  
    Return (data, body, fm_text). If no front matter, data={}, body=text, fm_text=''  
    """  
    lines = split_lines_keepends(text)  
    if not lines or not FRONT_MATTER_BOUND.match(lines[0]):  
        return {}, text, ''  

    fm_lines = []  
    i = 1  
    while i < len(lines) and not FRONT_MATTER_BOUND.match(lines[i]):  
        fm_lines.append(lines[i])  
        i += 1  
    if i == len(lines):  
        # Unmatched start '---'  
        return {}, text, ''  

    body = ''.join(lines[i+1:])  
    fm_text = ''.join(fm_lines)  
    data = {}  

    # Simple key: value parser (top-level)  
    for raw in fm_lines:  
        s = raw.strip()  
        if not s or s.startswith('#') or ':' not in s:  
            continue  
        key, val = s.split(':', 1)  
        key = key.strip()  
        val = val.strip()  
        if val.lower() in ('true', 'false'):  
            data[key] = (val.lower() == 'true')  
        else:  
            if val.isdigit():  
                data[key] = int(val)  
            else:  
                data[key] = val  
    return data, body, fm_text  

def compose_front_matter(data: dict) -> str:  
    ordered_keys = ['layout', 'title', 'parent', 'nav_order', 'has_children']  
    keys = ordered_keys + [k for k in data.keys() if k not in ordered_keys]  
    lines = ['---\n']  
    for k in keys:  
        if k in data:  
            v = data[k]  
            if isinstance(v, bool):  
                v = 'true' if v else 'false'  
            lines.append(f'{k}: {v}\n')  
    lines.append('---\n')  
    return ''.join(lines)  

# ---------- Title generation (when FM missing) ----------  

SMALL_WORDS = {  
    'a','an','and','as','at','but','by','for','in','nor','of',  
    'on','or','the','to','vs','via','with','from','over','into','onto','per'  
}  

def smart_title_from_slug(slug: str) -> str:  
    """  
    'the-special-theory-of-relativity' -> 'The Special Theory of Relativity'  
    Keeps small words in lowercase unless they are the first token.  
    """  
    parts = [w for w in re.split(r'[-_ ]+', slug) if w]  
    words = []  
    for idx, w in enumerate(parts):  
        wl = w.lower()  
        if idx > 0 and wl in SMALL_WORDS:  
            words.append(wl)  
        else:  
            words.append(wl[:1].upper() + wl[1:])  
    return ' '.join(words)  

# ---------- Heading checks for index.md ----------  

H2_PATTERN = re.compile(r'^\s*##\s+(.+?)\s*(?:#+\s*)?', re.MULTILINE)  

def body_has_any_h2(body: str) -> bool:  
    return bool(H2_PATTERN.search(body))  

def ensure_h2_if_absent(body: str, title: str) -> Tuple[str, bool]:  
    """  
    Insert '## <title>' at the top only if there is NO H2 at all in body.  
    """  
    if body_has_any_h2(body):  
        return body, False  
    insertion = f'## {title}\n\n'  
    return insertion + body.lstrip(), True  

# ---------- Path detection ----------  

def detect_volume_chapter(path: Path, docs_dir: Path) -> Optional[Tuple[int, int, str]]:  
    """  
    docs/volume-1/15-the-special-theory-of-relativity/index.md  
    -> (1, 15, 'The Special Theory of Relativity')  
    """  
    try:  
        rel = path.resolve().relative_to(docs_dir.resolve())  
    except Exception:  
        return None  
    parts = rel.parts  
    if len(parts) < 3:  
        return None  
    volume_part = parts[0]  # 'volume-1'  
    if not volume_part.startswith('volume-'):  
        return None  
    try:  
        volume_num = int(volume_part.split('-', 1)[1])  
    except Exception:  
        return None  

    chapter_dir = parts[1]  # '15-the-special-theory-of-relativity'  
    m = re.match(r'(\d+)-(.+)', chapter_dir)  
    if not m:  
        return None  
    chapter_num = int(m.group(1))  
    chapter_title = smart_title_from_slug(m.group(2))  
    return volume_num, chapter_num, chapter_title  

def detect_section_numbers(filename: str) -> Optional[Tuple[int, int, str]]:  
    """  
    15-1-the-principle-of-relativity.md -> (15, 1, 'The Principle of Relativity')  
    """  
    m = re.match(r'(\d+)-(\d+)-(.+)\.md', filename)  
    if not m:  
        return None  
    chapter_num = int(m.group(1))  
    section_num = int(m.group(2))  
    section_title = smart_title_from_slug(m.group(3))  
    return chapter_num, section_num, section_title  

# ---------- Ensure missing index.md ----------  

def chapter_dirs(docs_dir: Path, only_volume: Optional[str]) -> List[Tuple[int, str, Path]]:  
    """  
    Return list of (volume_num, volume_dirname, chapter_dir_path)  
    """  
    volumes = []  
    base = docs_dir.resolve()  
    if only_volume:  
        vol_path = (base / only_volume).resolve()  
        if vol_path.is_dir():  
            volumes.append(vol_path)  
    else:  
        volumes = [p.resolve() for p in base.glob('volume-*') if p.is_dir()]  

    result = []  
    for vol in volumes:  
        m = re.match(r'volume-(\d+)', vol.name)  
        if not m:  
            continue  
        vnum = int(m.group(1))  
        for ch in vol.iterdir():  
            if ch.is_dir() and re.match(r'\d+-', ch.name):  
                result.append((vnum, vol.name, ch.resolve()))  
    return result  

def ensure_missing_indexes(docs_dir: Path, only_volume: Optional[str], dry_run: bool=False) -> List[Path]:  
    """  
    Create index.md for any chapter dir missing it.  
    Returns list of created file paths.  
    """  
    created = []  
    base = docs_dir.resolve()  
    for vnum, vname, ch_dir in chapter_dirs(base, only_volume):  
        m = re.match(r'(\d+)-(.+)', ch_dir.name)  
        if not m:  
            continue  
        ch_num = int(m.group(1))  
        ch_title = smart_title_from_slug(m.group(2))  
        idx = (ch_dir / 'index.md').resolve()  
        if not idx.exists():  
            fm = compose_front_matter({  
                'layout': 'default',  
                'title': f'{ch_num}. {ch_title}',  
                'parent': f'Volume {vnum}',  
                'nav_order': ch_num,  
                'has_children': True  
            })  
            body = f'## {ch_num}. {ch_title}\n'  
            content = fm + body + '\n'  
            if not dry_run:  
                idx.write_text(content, encoding='utf-8')  
            created.append(idx)  
    return created  

# ---------- File processing ----------  

def rewrite_body_with_h2_if_needed(full_content: str, body: str, title: str) -> Tuple[str, bool]:  
    """  
    Replace only the body part by inserting H2 if there is NO H2 at all.  
    We compute the prefix length as len(full_content) - len(body).  
    """  
    new_body, changed = ensure_h2_if_absent(body, title)  
    if not changed:  
        return full_content, False  
    prefix_len = len(full_content) - len(body)  
    return full_content[:prefix_len] + new_body, True  

def process_file(path: Path, docs_dir: Path) -> Tuple[bool, str]:  
    """  
    Process links and (only when FM missing) front matter/heading for a single .md file.  
    Returns (changed, new_content)  
    """  
    p = path.resolve()  
    try:  
        original = p.read_text(encoding='utf-8')  
    except UnicodeDecodeError:  
        original = p.read_text(encoding='utf-8', errors='ignore')  

    # 1) Links  
    content, changed_links = rewrite_links_in_text(original)  

    # 2) Front matter and headings  
    meta = detect_volume_chapter(p, docs_dir)  
    changed_fm_or_heading = False  

    if meta:  
        volume_num, chapter_num, chapter_title_from_path = meta  
        data, body, fm_text = parse_front_matter(content)  

        if fm_text:  
            # FM exists: do NOT modify FM; for index.md only, ensure a H2 exists  
            if p.name == 'index.md':  
                fm_title = str(data.get('title', f'{chapter_num}. {chapter_title_from_path}'))  
                content, ch = rewrite_body_with_h2_if_needed(content, body, fm_title)  
                if ch:  
                    changed_fm_or_heading = True  
        else:  
            # No FM: generate minimal FM  
            if p.name == 'index.md':  
                new_data = {  
                    'layout': 'default',  
                    'title': f'{chapter_num}. {chapter_title_from_path}',  
                    'parent': f'Volume {volume_num}',  
                    'nav_order': chapter_num,  
                    'has_children': True  
                }  
                fm = compose_front_matter(new_data)  
                new_body, _ = ensure_h2_if_absent(body, new_data['title'])  
                content = fm + new_body  
                changed_fm_or_heading = True  
            else:  
                sec = detect_section_numbers(p.name)  
                if sec:  
                    fn_chapter_num, section_num, section_title = sec  
                    new_data = {  
                        'layout': 'default',  
                        'title': f'{chapter_num}-{section_num} {section_title}',  
                        'parent': f'{chapter_num}. {chapter_title_from_path}',  
                        'nav_order': section_num  
                    }  
                    fm = compose_front_matter(new_data)  
                    content = fm + body  
                    changed_fm_or_heading = True  

    changed = changed_links or changed_fm_or_heading  
    return changed, content  

# ---------- Utilities ----------  

def iter_target_files(docs_dir: Path, volume: Optional[str], only_files: Optional[List[Path]]) -> List[Path]:  
    """  
    Return a list of absolute Path objects for md files to process.  
    """  
    base = docs_dir.resolve()  
    if only_files:  
        out = []  
        for f in only_files:  
            p = Path(f)  
            p = p.resolve() if p.is_absolute() else (Path.cwd() / p).resolve()  
            if str(p).endswith('.md') and p.exists() and p.is_file():  
                out.append(p)  
        return out  
    if volume:  
        base = (base / volume).resolve()  
    return sorted([p.resolve() for p in base.rglob('*.md') if p.is_file()])  

def pretty_rel(p: Path, root: Path) -> str:  
    """  
    Robust relative path printer: always return path relative to root using os.path.relpath.  
    Works even if p is not a strict subpath of root per pathlib's relative_to.  
    """  
    try:  
        return os.path.relpath(str(p.resolve()), start=str(root.resolve()))  
    except Exception:  
        # Fallback to string if something odd happens  
        return str(p)  

# ---------- CLI main ----------  

def main():  
    ap = argparse.ArgumentParser(description="Fix links, generate missing index.md, and (when missing) FM/heading.")  
    ap.add_argument("--docs-dir", default=None, help="Path to docs dir (default: <repo_root>/docs)")  
    ap.add_argument("--volume", default=None, help="Limit to specific volume directory, e.g., volume-1")  
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")  
    ap.add_argument("--paths", nargs='*', help="Only process specific files (space-separated list)")  
    args = ap.parse_args()  

    # Resolve repo_root and docs_dir to absolute paths  
    repo_root = Path(__file__).resolve().parents[1]  
    docs_dir = Path(args.docs_dir).resolve() if args.docs_dir else (repo_root / "docs").resolve()  
    if not docs_dir.exists():  
        print(f"[ERROR] docs dir not found: {docs_dir}", file=sys.stderr)  
        sys.exit(1)  

    # Normalize only_files to absolute paths (relative to repo_root if needed)  
    only_files_abs: Optional[List[Path]] = None  
    if args.paths:  
        only_files_abs = []  
        for f in args.paths:  
            p = Path(f)  
            if not p.is_absolute():  
                p = (repo_root / p).resolve()  
            else:  
                p = p.resolve()  
            only_files_abs.append(p)  

    # 0) Ensure missing index.md first  
    created_indexes = ensure_missing_indexes(docs_dir, args.volume, dry_run=args.dry_run)  

    # 1) Process files (links + missing FM)  
    files = iter_target_files(docs_dir, args.volume, only_files_abs)  
    if not files and not created_indexes:  
        print("[INFO] No markdown files to process.")  
        return  

    changed_count = 0  
    for p in files:  
        changed, new_content = process_file(p, docs_dir)  
        if changed:  
            print(f"[CHANGE] {pretty_rel(p, repo_root)}")  
            if not args.dry_run:  
                p.write_text(new_content, encoding='utf-8')  
            changed_count += 1  

    # Print index creations  
    if created_indexes:  
        for idx in created_indexes:  
            tag = "[CREATE]" if args.dry_run else "[NEW]"  
            print(f"{tag} {pretty_rel(idx, repo_root)}")  

    if args.dry_run:  
        print(f"[DRY-RUN] modified files: {changed_count}, indexes to create: {len(created_indexes)}")  
    else:  
        print(f"[DONE] modified files: {changed_count}, new indexes: {len(created_indexes)}")  

if __name__ == "__main__":  
    main()
