#!/usr/bin/env python3
"""建立新論文頁並寫入登錄表（data/papers.js）。

用法：
    python scripts/new_paper.py kononov-2006-multiple-crews \
        --title "On relocation problems with multiple identical working crews" \
        --authors "A.V. Kononov" "B.M.T. Lin" \
        --year 2006 --venue "Discrete Optimization" \
        --volume "3(4)" --pages "366–381" --doi "10.1016/j.disopt.2006.06.003"

規則見 CLAUDE.md §4、§8。只使用 Python 標準函式庫。
"""
import argparse
import datetime
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_JS = ROOT / "data" / "papers.js"
TEMPLATE = ROOT / "templates" / "paper.html"
PAPERS_DIR = ROOT / "papers"
SLUG_RE = re.compile(r"^[a-z]+-\d{4}-[a-z0-9]+(-[a-z0-9]+)*$")
PREFIX = "window.PAPERS = "


def load_papers():
    text = PAPERS_JS.read_text(encoding="utf-8").strip()
    if not text.startswith(PREFIX) or not text.endswith(";"):
        sys.exit("錯誤：data/papers.js 格式不是 'window.PAPERS = [...];'")
    return json.loads(text[len(PREFIX):-1])


def save_papers(papers):
    body = json.dumps(papers, ensure_ascii=False, indent=2)
    PAPERS_JS.write_text(PREFIX + body + ";\n", encoding="utf-8")


def surname(name):
    return name.split(" ")[-1]


def label(authors, year):
    s = [surname(a) for a in authors]
    if len(s) == 1:
        return f"{s[0]} ({year})"
    if len(s) == 2:
        return f"{s[0]} & {s[1]} ({year})"
    return f"{s[0]} et al. ({year})"


def main():
    ap = argparse.ArgumentParser(description="建立新論文頁")
    ap.add_argument("slug", help="例如 kononov-2006-multiple-crews")
    ap.add_argument("--title", required=True, help="原文標題（英文）")
    ap.add_argument("--authors", nargs="+", required=True, help='例如 "A.V. Kononov" "B.M.T. Lin"')
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--venue", required=True)
    ap.add_argument("--volume", default="原文未說明")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--doi", required=True, help="不含網址，例如 10.1016/j.disopt.2006.06.003")
    args = ap.parse_args()

    if not SLUG_RE.match(args.slug):
        sys.exit("錯誤：slug 格式應為 第一作者姓氏-年份-關鍵字，只含 a-z 0-9 -")
    if not args.doi.startswith("10."):
        sys.exit("錯誤：doi 請填不含網址的 DOI（以 10. 開頭）")

    papers = load_papers()
    if any(p["slug"] == args.slug for p in papers):
        sys.exit(f"錯誤：登錄表已有 {args.slug}")
    page_path = PAPERS_DIR / f"{args.slug}.html"
    if page_path.exists():
        sys.exit(f"錯誤：{page_path} 已存在，不會覆蓋")

    html_text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in {
        "{{SLUG}}": args.slug,
        "{{TITLE}}": html.escape(args.title),
        "{{LABEL}}": html.escape(label(args.authors, args.year)),
        "{{SUMMARY}}": "TODO 一句話摘要",
    }.items():
        html_text = html_text.replace(key, value)
    PAPERS_DIR.mkdir(exist_ok=True)
    page_path.write_text(html_text, encoding="utf-8")

    papers.append({
        "slug": args.slug,
        "title": args.title,
        "authors": args.authors,
        "year": args.year,
        "venue": args.venue,
        "volume": args.volume,
        "pages": args.pages,
        "doi": args.doi,
        "summary": "TODO",
        "tags": [],
        "concepts": [],
        "machine": "TODO",
        "agents": "TODO",
        "resource": "TODO",
        "objective": "TODO",
        "result": "TODO",
        "facets": {"parallel": False, "twoAgent": False, "resource": False},
        "status": "待讀",
        "date": datetime.date.today().isoformat(),
    })
    save_papers(papers)

    print(f"已建立 {page_path.relative_to(ROOT)}")
    print("已寫入 data/papers.js（status = 待讀）")
    print("下一步：完整讀完 PDF → 填寫七個區塊與登錄表欄位 → 更新相關概念頁 → python scripts/check.py → 寫入 log.md")


if __name__ == "__main__":
    main()
