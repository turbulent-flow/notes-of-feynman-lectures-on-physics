#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

ROOT = Path(".")          # 站点根（仓库根）
TOP_TITLE = "目录"        # 顶层首页标题，需要与根 index.md 的 title 一致

def slug_to_title(slug: str) -> str:
    small = {"a","an","and","the","of","to","in","on","for","with","as","at","by","from","or"}
    parts = [p for p in slug.replace("_","-").split("-") if p]
    out = []
    for i, w in enumerate(parts):
        lw = w.lower()
        out.append(lw if (i != 0 and lw in small) else (lw[:1].upper() + lw[1:]))
    return " ".join(out)

def ensure_text(path: Path, content: str):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"+ create {path}")

def build_fm(fields: dict) -> str:
    order = ["layout","title","parent","nav_order","has_children"]
    lines = ["---"]
    for k in order:
        if k in fields:
            lines.append(f"{k}: {fields[k]}")
    for k, v in fields.items():
        if k not in order:
            lines.append(f"{k}: {v}")
    lines.append("---\n")
    return "\n".join(lines)

def split_fm(text: str):
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            fm_raw = text[4:end]
            body = text[end+5:]
            fm = {}
            for line in fm_raw.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
            return fm, body
    return None, text

def upsert_fm(md: Path, new_fields: dict):
    txt = md.read_text(encoding="utf-8") if md.exists() else ""
    fm, body = split_fm(txt) if txt else (None, "")
    if fm is None:
        md.write_text(build_fm(new_fields) + (txt or ""), encoding="utf-8")
        print(f"+ add FM {md}")
    else:
        changed = False
        for k, v in new_fields.items():
            if k not in fm:
                fm[k] = v
                changed = True
        if changed:
            md.write_text(build_fm(fm) + body, encoding="utf-8")
            print(f"* update FM {md}")

def ensure_root_config_and_home():
    cfg = ROOT / "_config.yml"
    ensure_text(cfg, """title: Notes of Feynman Lectures on Physics
description: 读书笔记
remote_theme: just-the-docs/just-the-docs
search_enabled: true
heading_anchors: true

url: https://turbulent-flow.github.io
baseurl: /notes-of-feynman-lectures-on-physics

exclude:
  - prepare_page.py
  - prepare_pages.py
  - README.md
  - LICENSE

kramdown:
  input: GFM
  math_engine: mathjax
""")
    home = ROOT / "index.md"
    ensure_text(home, f"""---
layout: default
title: {TOP_TITLE}
nav_order: 1
has_children: true
---

# Notes of Feynman Lectures on Physics
这里是总目录与说明。
""")

def parse_chapter_dir(name: str):
    if "-" not in name: return None
    num, rest = name.split("-", 1)
    return (int(num), rest) if num.isdigit() else None

def parse_section_file(stem: str):
    parts = stem.split("-")
    if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
        n1, n2 = int(parts[0]), int(parts[1])
        rest = "-".join(parts[2:])
        return n1, n2, rest
    return None

def group_dirs():
    groups = []
    for d in ROOT.iterdir():
        if not d.is_dir(): 
            continue
        if d.name.startswith("_") or d.name in {"assets", ".git", ".github"}:
            continue
        # 认为包含至少一个“章目录”的，就是分卷目录（如 volume-1）
        has_chapter = any(parse_chapter_dir(p.name) for p in d.iterdir() if p.is_dir())
        if has_chapter:
            # 计算排序：优先提取名称中的数字（如 volume-1 -> 1）
            parts = d.name.replace("_","-").split("-")
            order = None
            for w in parts:
                if w.isdigit():
                    order = int(w); break
            if order is None: order = 999
            groups.append((order, d))
    groups.sort(key=lambda x: (x[0], x[1].name))
    return [g for _, g in groups]

def ensure_group_index(gdir: Path, order: int, title: str):
    gindex = gdir / "index.md"
    # 若已存在，则补齐必需字段；否则创建
    if gindex.exists():
        upsert_fm(gindex, {
            "layout": "default",
            "title": title,
            "parent": TOP_TITLE,
            "has_children": "true",
            "nav_order": order
        })
    else:
        ensure_text(gindex, build_fm({
            "layout": "default",
            "title": title,
            "parent": TOP_TITLE,
            "has_children": "true",
            "nav_order": order
        }) + f"# {title}\n\n")

def main():
    ensure_root_config_and_home()

    # 遍历所有“分卷”（如 volume-1）
    for gi, gdir in enumerate(group_dirs(), start=1):
        gtitle = slug_to_title(gdir.name)      # volume-1 -> "Volume 1"
        ensure_group_index(gdir, gi, gtitle)

        # 遍历分卷中的“章目录”
        chapters = []
        for p in gdir.iterdir():
            if p.is_dir():
                parsed = parse_chapter_dir(p.name)
                if parsed:
                    chapters.append((parsed[0], parsed[1], p))
        chapters.sort(key=lambda x: x[0])

        for chap_no, chap_slug, chap_dir in chapters:
            chap_title = f"{chap_no}. {slug_to_title(chap_slug)}"
            # 章 index.md
            cidx = chap_dir / "index.md"
            if cidx.exists():
                upsert_fm(cidx, {
                    "layout": "default",
                    "title": chap_title,
                    "parent": gtitle,
                    "has_children": "true",
                    "nav_order": chap_no
                })
            else:
                ensure_text(cidx, build_fm({
                    "layout": "default",
                    "title": chap_title,
                    "parent": gtitle,
                    "has_children": "true",
                    "nav_order": chap_no
                }) + f"# {chap_title}\n\n")

            # 小节 .md
            for f in sorted(chap_dir.glob("*.md")):
                if f.name.lower() == "index.md":
                    continue
                parsed = parse_section_file(f.stem)
                if parsed:
                    sec_no = parsed[1]
                    sec_title = f"{parsed[0]}-{parsed[1]} {slug_to_title(parsed[2])}"
                    order = sec_no
                else:
                    sec_title = slug_to_title(f.stem)
                    order = 999
                upsert_fm(f, {
                    "layout": "default",
                    "title": sec_title,
                    "parent": chap_title,
                    "nav_order": order
                })

if __name__ == "__main__":
    main()