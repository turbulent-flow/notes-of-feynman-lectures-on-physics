#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unify referenced section headings (fig-/table-/eq-) to H3 in docs/volume-1/*.md.

- 将任意级别的 ATX 标题 (#...######) 中，以 fig/table/eq 开头的引用类标题统一改为 H3（###）。
- 保留原始标题文字与可选的结尾关闭井号（如 "### 标题 ###"）。
- 兼容无空格写法（如 "#####table-3-3"）。
- 跳过代码围栏块（``` 或 ~~~）中的内容。  
"""  

from pathlib import Path  
import argparse  
import re  
import sys  

# 进入/退出代码围栏：以 ``` 或 ~~~ 开头（忽略语言标注）
FENCE_PATTERN = re.compile(r'^\s*(?:`{3,}|~{3,})')

# 前缀匹配：fig/table/eq（不区分大小写），后接若干空格或常见分隔符，然后通常跟数字
# 允许的分隔符集合：- – — . : ：（可自行扩展）
PREFIX_RE = re.compile(r'^(fig|table|eq)\s*[-–—\.\:\： ]*\d', re.IGNORECASE)

def is_target_heading_text(text: str) -> bool:
    t = text.strip()
    return bool(PREFIX_RE.match(t))

def parse_atx_heading(line: str):
    """
    解析 ATX 标题。若是标题，返回 (indent, level, core_text, closing_hashes, newline)
    否则返回 None。
    - indent: 行首空白
    - level: 井号数量（1..6）
    - core_text: 标题文本（不含行尾关闭井号）
    - closing_hashes: 行尾关闭井号（含其前的空格），或空字符串
    - newline: 原始换行符
    """
    # 保留换行
    nl = ''
    if line.endswith('\r\n'):
        nl = '\r\n'
        content = line[:-2]
    elif line.endswith('\n'):
        nl = '\n'
        content = line[:-1]
    else:
        content = line

    i = 0
    # 缩进空白
    while i < len(content) and content[i] in (' ', '\t'):
        i += 1
    indent = content[:i]

    # 计数井号
    j = i
    while j < len(content) and content[j] == '#':
        j += 1
    level = j - i
    if level < 1 or level > 6:
        return None

    # 井号后可有可无空格
    k = j
    while k < len(content) and content[k] in (' ', '\t'):
        k += 1

    # 剩余为标题+可选结尾关闭井号
    rest = content[k:]

    # 检测尾部关闭井号：形如 " ...  ###   "
    # 找到末尾的连续 #，且它们前面至少有一个空格
    closing_hashes = ''
    if rest:
        # 去掉末尾空格后检查 #
        r = rest.rstrip()
        # 末尾有 #，则视为关闭井号
        end = len(r)
        h = end
        while h > 0 and r[h-1] == '#':
            h -= 1
        if h < end:
            # r[h:end] 是连续的 #；要求其前面有空格以视为“关闭井号”
            if h > 0 and r[h-1] in (' ', '\t'):
                closing_hashes = r[h:end] + rest[len(r):]  # 保留原始空白
                core_text = r[:h-1]  # 去掉空格与关闭井号
            else:
                core_text = rest
        else:
            core_text = rest
    else:
        core_text = ''

    return indent, level, core_text, closing_hashes, nl

def rewrite_heading_line(line: str):
    """
    若是目标标题（fig/table/eq 开头），将级别统一为 H3，返回 (new_line, changed)。
    否则返回 (line, False)。
    """
    parsed = parse_atx_heading(line)
    if not parsed:
        return line, False

    indent, level, core_text, closing_hashes, nl = parsed

    if not is_target_heading_text(core_text):
        return line, False

    new_text = core_text.strip()
    new_line = f"{indent}### {new_text}{(' ' if closing_hashes and not closing_hashes.startswith(' ') else '')}{closing_hashes}{nl}"
    if new_line != line:
        return new_line, True
    return line, False

def transform_text(text: str):
    lines = text.splitlines(keepends=True)
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

        new_ln, changed = rewrite_heading_line(ln)
        if changed:
            changed_any = True
        out.append(new_ln)

    return ''.join(out), changed_any

def main():
    ap = argparse.ArgumentParser(description="Unify fig-/table-/eq- headings to H3 in docs/<volume>/*.md")
    ap.add_argument("--docs-dir", default=None, help="Path to docs directory (default: <repo_root>/docs)")
    ap.add_argument("--volume", default="volume-1", help="Volume subdirectory under docs (default: volume-1)")
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    ap.add_argument("--debug", action="store_true", help="Print sample candidates if no change")
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
        elif args.debug:
            # 打印首个疑似候选，帮助诊断
            for i, ln in enumerate(original.splitlines()):
                if ln.lstrip().startswith('#'):
                    # 粗略展示
                    sample = ln.strip()
                    if sample:
                        print(f"[DEBUG] candidate {p.relative_to(repo_root)}:{i+1}: {sample}")
                        break

    if args.dry_run:
        print(f"[DRY-RUN] files to be modified: {modified}")
    else:
        print(f"[DONE] modified files: {modified}")

if __name__ == "__main__":
    main()
