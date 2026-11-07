#!/usr/bin/env python3
"""建立新概念頁並寫入登錄表（data/concepts.js）。

用法：
    python scripts/new_concept.py relocation-problem \
        --title "Relocation problem 與資源回收模型" \
        --title-en "Relocation problem"

規則見 CLAUDE.md §5、§6.2、§9.1。只使用 Python 標準函式庫。
"""
import argparse
import datetime
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONCEPTS_JS = ROOT / "data" / "concepts.js"
TEMPLATE = ROOT / "templates" / "concept.html"
CONCEPTS_DIR = ROOT / "concepts"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PREFIX = "window.CONCEPTS = "


def load_concepts():
    text = CONCEPTS_JS.read_text(encoding="utf-8").strip()
    if not text.startswith(PREFIX) or not text.endswith(";"):
        sys.exit("錯誤：data/concepts.js 格式不是 'window.CONCEPTS = [...];'")
    return json.loads(text[len(PREFIX):-1])


def main():
    ap = argparse.ArgumentParser(description="建立新概念頁")
    ap.add_argument("slug", help="例如 approximation-algorithms")
    ap.add_argument("--title", required=True, help="中文名稱（保留英文專有名詞）")
    ap.add_argument("--title-en", required=True, help="英文名稱")
    args = ap.parse_args()

    if not SLUG_RE.match(args.slug):
        sys.exit("錯誤：slug 只能含 a-z 0-9 -")

    concepts = load_concepts()
    if any(c["slug"] == args.slug for c in concepts):
        sys.exit(f"錯誤：登錄表已有 {args.slug}")
    page_path = CONCEPTS_DIR / f"{args.slug}.html"
    if page_path.exists():
        sys.exit(f"錯誤：{page_path} 已存在，不會覆蓋")

    text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in {
        "{{SLUG}}": args.slug,
        "{{TITLE}}": html.escape(args.title),
        "{{TITLE_EN}}": html.escape(args.title_en),
        "{{SUMMARY}}": "TODO 一句話定義",
    }.items():
        text = text.replace(key, value)
    CONCEPTS_DIR.mkdir(exist_ok=True)
    page_path.write_text(text, encoding="utf-8")

    concepts.append({
        "slug": args.slug,
        "title": args.title,
        "titleEn": args.title_en,
        "summary": "TODO",
        "papers": [],
        "related": [],
        "status": "待讀",
        "date": datetime.date.today().isoformat(),
    })
    CONCEPTS_JS.write_text(PREFIX + json.dumps(concepts, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")

    print(f"已建立 {page_path.relative_to(ROOT)}")
    print("已寫入 data/concepts.js（status = 待讀）")
    print("下一步：填寫五個區塊、在 data/concepts.js 填 papers／related、同步更新各論文的 concepts 欄位 → python scripts/check.py")


if __name__ == "__main__":
    main()
