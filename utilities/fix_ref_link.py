#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Batch-fix Markdown links to .html by adding the site base path
(e.g., '/notes-of-feynman-lectures-on-physics').

Run from anywhere; paths are resolved relative to this script file by default.
"""

from __future__ import annotations
import argparse
import posixpath
import re
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse, urlunparse, ParseResult

# ========= 可配置区域 =========
# 需要批量更改的文件根目录（相对本脚本或绝对路径）
TARGET_DIR = "../docs"
# 链接需要加的站点前缀
BASE_PREFIX = "/notes-of-feynman-lectures-on-physics"
# 要处理的文件扩展名
FILE_EXTS = (".md",)
# =============================

EXTERNAL_SCHEMES = ("http://", "https://", "mailto:", "tel:")

# Markdown 行内链接（非图片）
RE_INLINE = re.compile(
    r'(?<!\!)'          # not an image
    r'(\]\()\s*'        # 1: prefix ' ]('
    r'([^\s\)]+)'       # 2: url
    r'([^)]*)'          # 3: optional title/attrs
    r'\)'
)

# Markdown 引用式链接定义行：[id]: url "title"
RE_REFDEF = re.compile(r'^(\s*\[[^\]]+\]:\s+)(\S+)(.*)', re.MULTILINE)

# HTML <a href="...">
RE_HTML_HREF = re.compile(r'(<a\b[^>]*?\bhref=["\'])([^"\']+)(["\'])', re.IGNORECASE)


def resolve_to_docs_abs(md_file: Path, url: str, docs_dir: Path) -> str:
    """将（可能相对的）URL 解析为以 docs 根为准的绝对路径，并加上 BASE_PREFIX。"""
    if url.startswith(EXTERNAL_SCHEMES) or url.startswith("#"):
        return url

    pr: ParseResult = urlparse(url)
    path = pr.path or ""
    if ".html" not in path:
        return url

    # 已有前缀则不重复
    if path.startswith(BASE_PREFIX + "/") or path == BASE_PREFIX:
        return url

    # 计算以 docs 为根的绝对路径（以 / 开头）
    if path.startswith("/"):
        abs_path = path
    else:
        rel_dir_posix = md_file.parent.relative_to(docs_dir).as_posix()
        joined = posixpath.join("/", rel_dir_posix, path)
        abs_path = posixpath.normpath(joined)
        if not abs_path.startswith("/"):
            abs_path = "/" + abs_path

    new_path = f"{BASE_PREFIX}{abs_path}"
    new_pr = ParseResult(
        scheme=pr.scheme,
        netloc=pr.netloc,
        path=new_path,
        params=pr.params,
        query=pr.query,
        fragment=pr.fragment,
    )
    return urlunparse(new_pr)


def make_replacers(md_file: Path, docs_dir: Path, counter: dict) -> tuple[Callable[[re.Match], str], ...]:
    def repl_inline(m: re.Match) -> str:
        pre, url, rest = m.group(1), m.group(2), m.group(3) or ""
        if ".html" not in url:
            return m.group(0)
        new_url = resolve_to_docs_abs(md_file, url, docs_dir)
        if new_url != url:
            counter["n"] += 1
        return f"{pre}{new_url}{rest})"

    def repl_refdef(m: re.Match) -> str:
        prefix, url, rest = m.group(1), m.group(2), m.group(3) or ""
        if ".html" not in url:
            return m.group(0)
        new_url = resolve_to_docs_abs(md_file, url, docs_dir)
        if new_url != url:
            counter["n"] += 1
        return f"{prefix}{new_url}{rest}"

    def repl_html_href(m: re.Match) -> str:
        pre, url, post = m.group(1), m.group(2), m.group(3)
        if ".html" not in url:
            return m.group(0)
        new_url = resolve_to_docs_abs(md_file, url, docs_dir)
        if new_url != url:
            counter["n"] += 1
        return f"{pre}{new_url}{post}"

    return repl_inline, repl_refdef, repl_html_href


def transform_markdown(text: str, md_file: Path, docs_dir: Path) -> tuple[str, int]:
    counter = {"n": 0}
    repl_inline, repl_refdef, repl_html_href = make_replacers(md_file, docs_dir, counter)
    text = RE_INLINE.sub(repl_inline, text)
    text = RE_REFDEF.sub(repl_refdef, text)
    text = RE_HTML_HREF.sub(repl_html_href, text)
    return text, counter["n"]


def process_file(md_file: Path, docs_dir: Path, dry_run: bool, verbose: bool) -> int:
    original = md_file.read_text(encoding="utf-8")
    new_text, changed_links = transform_markdown(original, md_file, docs_dir)
    if changed_links and not dry_run:
        md_file.write_text(new_text, encoding="utf-8")
    if verbose and changed_links:
        print(f"[MODIFIED] {md_file} (+{changed_links} links)")
    return changed_links


def main():
    parser = argparse.ArgumentParser(description="Prefix .html links in Markdown with a site base path.")
    parser.add_argument("--dir", help="Override TARGET_DIR (path to process).")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not write files.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output.")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    raw_dir = args.dir if args.dir else TARGET_DIR
    content_root = Path(raw_dir)
    if not content_root.is_absolute():
        content_root = (script_dir / content_root).resolve()

    if not content_root.exists() or not content_root.is_dir():
        raise SystemExit(f"Directory not found: {content_root}")

    md_files = [p for p in content_root.rglob("*") if p.suffix.lower() in FILE_EXTS]
    if args.verbose:
        print(f"Scanning {len(md_files)} files under: {content_root}")

    total_links = 0
    for p in md_files:
        total_links += process_file(p, content_root, dry_run=args.dry_run, verbose=args.verbose)

    print(f"Done. Files scanned: {len(md_files)}; links updated: {total_links}.")
    if args.dry_run:
        print("Dry-run mode: no files were written.")


if __name__ == "__main__":
    main()
    