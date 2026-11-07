#!/usr/bin/env python3
"""驗證網站內容是否符合 CLAUDE.md 規則。零錯誤才算完成。

用法：python scripts/check.py
只使用 Python 標準函式庫。
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
PAPER_SLUG_RE = re.compile(r"^[a-z]+-\d{4}-[a-z0-9]+(-[a-z0-9]+)*$")
CONCEPT_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
STATUSES = {"待讀", "初整理", "已確認"}
PAPER_KEYS = {
    "slug": str, "title": str, "authors": list, "year": int, "venue": str, "volume": str,
    "pages": str, "doi": str, "summary": str, "tags": list, "concepts": list, "machine": str,
    "agents": str, "resource": str, "objective": str, "result": str, "facets": dict,
    "status": str, "date": str,
}
CONCEPT_KEYS = {
    "slug": str, "title": str, "titleEn": str, "summary": str, "papers": list,
    "related": list, "status": str, "date": str,
}
PAPER_SECTIONS = ["summary", "problem", "method", "results", "limitations", "relevance", "notes"]
CONCEPT_SECTIONS = ["definition", "variants", "literature", "disagreements", "open-questions"]
LOG_TYPES = ("ingest", "query", "lint", "update", "fix", "schema")
LOG_RE = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] (" + "|".join(LOG_TYPES) + r") \| .+")

errors = []
warnings = []


def err(where, msg):
    errors.append(f"[錯誤] {where}: {msg}")


def warn(where, msg):
    warnings.append(f"[警告] {where}: {msg}")


class PageParser(HTMLParser):
    """蒐集頁面結構：h1 文字、h2 id、class、連結、inline style 等。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = ""
        self.h2_ids = []
        self.h2_without_id = 0
        self.classes = []
        self.links = []
        self.external_assets = []
        self.inline_styles = 0
        self.imgs_without_alt = 0
        self.data_attrs = {}
        self.body_attrs = {}
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "body":
            self.body_attrs = a
        if tag == "h1":
            self._in_h1 = True
        if tag == "h2":
            if a.get("id"):
                self.h2_ids.append(a["id"])
            else:
                self.h2_without_id += 1
        if "class" in a:
            self.classes.extend(a["class"].split())
        if "style" in a:
            self.inline_styles += 1
        for k in a:
            if k.startswith("data-"):
                self.data_attrs[k] = a[k]
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img") and a.get("src"):
            self.links.append(a["src"])
            if re.match(r"^(https?:)?//", a["src"]):
                self.external_assets.append(a["src"])
        if tag == "link" and a.get("href"):
            self.links.append(a["href"])
            if re.match(r"^(https?:)?//", a["href"]):
                self.external_assets.append(a["href"])
        if tag == "img" and not a.get("alt"):
            self.imgs_without_alt += 1

    def handle_endtag(self, tag):
        if tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_h1:
            self.h1 += data


def parse_html(path):
    p = PageParser()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def check_link(base_file, url, where):
    if re.match(r"^(https?:|mailto:|#|tel:)", url) or url.startswith("//"):
        return
    target = urlparse(url).path
    if not target:
        return
    if not (base_file.parent / target).resolve().exists():
        err(where, f"連結不存在：{url}")


def load_registry(filename, var):
    prefix = f"window.{var} = "
    path = ROOT / "data" / filename
    if not path.exists():
        err(f"data/{filename}", "檔案不存在")
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text.startswith(prefix) or not text.endswith(";"):
        err(f"data/{filename}", f"格式必須是 '{prefix}[ ... ];'")
        return []
    try:
        return json.loads(text[len(prefix):-1])
    except json.JSONDecodeError as e:
        err(f"data/{filename}", f"不是合法 JSON（需雙引號、無註解、無結尾逗號）：{e}")
        return []


def check_types(where, item, spec):
    for key, typ in spec.items():
        if key not in item:
            err(where, f"缺少欄位 {key}")
        elif not isinstance(item[key], typ) or (typ is int and isinstance(item[key], bool)):
            err(where, f"欄位 {key} 型別應為 {typ.__name__}")


def check_common(where, item, label_fields):
    if item.get("status") not in STATUSES:
        err(where, f"status 只能是 {sorted(STATUSES)}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(item.get("date", ""))):
        err(where, "date 格式應為 YYYY-MM-DD")
    if isinstance(item.get("summary"), str) and len(item["summary"]) > 60:
        warn(where, f"summary 超過 60 字（{len(item['summary'])}）")
    if item.get("status") != "待讀":
        for key in label_fields:
            if "TODO" in str(item.get(key, "")):
                err(where, f"status 為 {item['status']} 但 {key} 仍含 TODO")


def check_registries(papers, concepts):
    paper_slugs = [p.get("slug") for p in papers if isinstance(p, dict)]
    concept_slugs = [c.get("slug") for c in concepts if isinstance(c, dict)]
    paper_by = {p["slug"]: p for p in papers if isinstance(p, dict) and "slug" in p}
    concept_by = {c["slug"]: c for c in concepts if isinstance(c, dict) and "slug" in c}

    seen = set()
    for i, p in enumerate(papers):
        where = f"data/papers.js:{p.get('slug', i)}"
        if not isinstance(p, dict):
            err(where, "每筆必須是物件")
            continue
        check_types(where, p, PAPER_KEYS)
        slug = p.get("slug", "")
        if slug in seen:
            err(where, "slug 重複")
        seen.add(slug)
        if slug and not PAPER_SLUG_RE.match(slug):
            err(where, "slug 格式應為 第一作者姓氏-年份-關鍵字（a-z 0-9 -）")
        elif slug and str(p.get("year")) not in slug:
            err(where, "slug 中的年份與 year 不一致")
        if not str(p.get("doi", "")).startswith("10."):
            err(where, "doi 應為不含網址、以 10. 開頭")
        facets = p.get("facets", {})
        if isinstance(facets, dict) and (set(facets) != {"parallel", "twoAgent", "resource"} or not all(isinstance(v, bool) for v in facets.values())):
            err(where, "facets 必須剛好含 parallel、twoAgent、resource 三個布林值")
        check_common(where, p, ("summary", "machine", "agents", "resource", "objective", "result"))
        if p.get("status") != "待讀":
            if not p.get("tags"):
                err(where, "status 不是待讀時 tags 不可為空")
            if not p.get("concepts"):
                warn(where, "沒有任何相關概念（孤立）")
        for c in p.get("concepts", []):
            if c not in concept_by:
                err(where, f"concepts 含不存在的概念：{c}")
            elif slug not in concept_by[c].get("papers", []):
                err(where, f"與概念 {c} 沒有雙向對應（該概念的 papers 沒有 {slug}）")

    seen = set()
    for i, c in enumerate(concepts):
        where = f"data/concepts.js:{c.get('slug', i)}"
        if not isinstance(c, dict):
            err(where, "每筆必須是物件")
            continue
        check_types(where, c, CONCEPT_KEYS)
        slug = c.get("slug", "")
        if slug in seen:
            err(where, "slug 重複")
        seen.add(slug)
        if slug and not CONCEPT_SLUG_RE.match(slug):
            err(where, "slug 只能含 a-z 0-9 -")
        check_common(where, c, ("summary",))
        if c.get("status") != "待讀" and not c.get("papers"):
            err(where, "概念沒有任何相關論文（孤立）")
        for ps in c.get("papers", []):
            if ps not in paper_by:
                err(where, f"papers 含不存在的論文：{ps}")
            elif slug not in paper_by[ps].get("concepts", []):
                err(where, f"與論文 {ps} 沒有雙向對應（該論文的 concepts 沒有 {slug}）")
        for r in c.get("related", []):
            if r not in concept_by:
                err(where, f"related 含不存在的概念：{r}")
            elif r == slug:
                err(where, "related 不可包含自己")
    return paper_by, concept_by


def common_page_checks(rel, path, page, raw):
    if page.inline_styles:
        err(rel, f"不得使用 inline style（{page.inline_styles} 處）")
    if page.external_assets:
        err(rel, f"不得載入外部資源：{page.external_assets}")
    if page.imgs_without_alt:
        err(rel, "<img> 必須有 alt")
    if page.h2_without_id:
        err(rel, f"有 {page.h2_without_id} 個 <h2> 沒有 id")
    for url in page.links:
        check_link(path, url, rel)


def check_pages(kind, registry, sections, extra_scripts):
    folder = ROOT / ("papers" if kind == "paper" else "concepts")
    files = {f.stem: f for f in folder.glob("*.html")} if folder.exists() else {}
    for slug in registry:
        if slug not in files:
            err(f"{folder.name}/{slug}.html", "登錄表有此項目但頁面不存在")
    for stem in files:
        if stem not in registry:
            err(f"{folder.name}/{stem}.html", "頁面存在但登錄表沒有對應項目")

    for slug, path in files.items():
        if slug not in registry:
            continue
        rel = f"{folder.name}/{slug}.html"
        meta = registry[slug]
        page = parse_html(path)
        raw = path.read_text(encoding="utf-8")
        common_page_checks(rel, path, page, raw)

        if page.body_attrs.get("data-slug") != slug:
            err(rel, "<body data-slug> 必須等於檔名 slug")
        if page.body_attrs.get("data-page") != kind:
            err(rel, f'<body data-page="{kind}"> 缺少或錯誤')
        if page.h1.strip() != meta.get("title"):
            err(rel, f"<h1> 必須與登錄表 title 完全相同（目前：{page.h1.strip()[:40]}）")
        if page.h2_ids != sections:
            err(rel, f"<h2> id 必須依序為 {sections}，目前為 {page.h2_ids}")
        for attr in ("data-bib", "data-toc") + (("data-paper-nav",) if kind == "paper" else ()):
            if attr not in page.data_attrs:
                err(rel, f"缺少 {attr} 容器")
        for script in extra_scripts:
            if f'src="{script}"' not in raw:
                err(rel, f'缺少 <script src="{script}">')

        if meta.get("status") != "待讀":
            if "TODO" in raw:
                err(rel, "status 不是待讀，但頁面仍有 TODO")
            if page.classes.count("src") < 2:
                err(rel, "至少需要 2 個來源標記 <span class=\"src\">")

        if kind == "paper":
            if meta.get("status") != "待讀":
                res = re.search(r'<h2 id="results">(.*?)<h2 id="limitations">', raw, re.S)
                if res:
                    items = re.findall(r"<li>(.*?)</li>", res.group(1), re.S)
                    if not items:
                        err(rel, "「主要結果」沒有條列項目")
                    missing = [i for i in items if 'class="src"' not in i]
                    if missing:
                        err(rel, f"「主要結果」有 {len(missing)} 條缺少來源標記")
            for c in meta.get("concepts", []):
                if f"../concepts/{c}.html" not in raw:
                    err(rel, f"頁面內沒有連到相關概念 {c}（CLAUDE.md §6.5）")
        else:
            lit = re.search(r'<h2 id="literature">(.*?)<h2 id="disagreements">', raw, re.S)
            if lit and meta.get("status") != "待讀":
                body = lit.group(1)
                for ps in meta.get("papers", []):
                    if f"../papers/{ps}.html" not in body:
                        err(rel, f"「文獻怎麼說」沒有連到論文 {ps}")
                rows = [r for r in re.findall(r"<tr>(.*?)</tr>", body, re.S) if "<th" not in r]
                if not rows:
                    err(rel, "「文獻怎麼說」沒有任何資料列")
                for r in rows:
                    if 'class="src"' not in r:
                        err(rel, "「文獻怎麼說」有資料列缺少來源標記")
                        break


def check_other_pages():
    for name in ("index.html", "about.html"):
        path = ROOT / name
        if not path.exists():
            err(name, "檔案不存在")
            continue
        page = parse_html(path)
        raw = path.read_text(encoding="utf-8")
        common_page_checks(name, path, page, raw)
        for script in ("data/papers.js", "data/concepts.js"):
            if script not in raw:
                err(name, f"缺少 {script} 腳本")


def check_log(papers):
    path = ROOT / "log.md"
    if not path.exists():
        err("log.md", "檔案不存在")
        return
    text = path.read_text(encoding="utf-8")
    last = ""
    count = 0
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("## ["):
            count += 1
            m = LOG_RE.match(line)
            if not m:
                err(f"log.md:{n}", f"格式應為 '## [YYYY-MM-DD] 類型 | 對象'，類型限 {LOG_TYPES}")
                continue
            if m.group(1) < last:
                err(f"log.md:{n}", "日期必須依時間順序（只增不改）")
            last = m.group(1)
    if not count:
        err("log.md", "沒有任何紀錄")
    for p in papers:
        if isinstance(p, dict) and p.get("status") != "待讀" and f"ingest | {p.get('slug')}" not in text:
            err("log.md", f"缺少 {p.get('slug')} 的 ingest 紀錄")


def check_repo_rules():
    gi = ROOT / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if "參考文獻/" not in text:
        err(".gitignore", "必須排除 參考文獻/")
    if "*.pdf" not in text:
        err(".gitignore", "必須排除 *.pdf")
    for pdf in ROOT.rglob("*.pdf"):
        if not set(pdf.relative_to(ROOT).parts) & {"參考文獻", ".git"}:
            err(str(pdf.relative_to(ROOT)), "repo 內不得放 PDF（版權）")
    for needed in ("CLAUDE.md", "README.md", "log.md", ".nojekyll", "assets/css/style.css", "assets/js/site.js",
                   "templates/paper.html", "templates/concept.html", "scripts/new_paper.py", "scripts/new_concept.py"):
        if not (ROOT / needed).exists():
            err(needed, "必要檔案不存在")
    css = ROOT / "assets" / "css" / "style.css"
    if css.exists():
        txt = css.read_text(encoding="utf-8")
        if re.search(r"https?://", txt) or "@import" in txt:
            err("assets/css/style.css", "不得有外部 URL 或 @import")
    for js in (ROOT / "assets" / "js").glob("*.js"):
        if re.search(r"""(src|href)\s*=\s*["']https?://""", js.read_text(encoding="utf-8")):
            err(str(js.relative_to(ROOT)), "不得動態載入外部資源")


def main():
    papers = load_registry("papers.js", "PAPERS")
    concepts = load_registry("concepts.js", "CONCEPTS")
    paper_by, concept_by = check_registries(papers, concepts)
    check_pages("paper", paper_by, PAPER_SECTIONS, ("../data/site.js", "../data/papers.js", "../data/concepts.js", "../assets/js/site.js"))
    check_pages("concept", concept_by, CONCEPT_SECTIONS, ("../data/site.js", "../data/papers.js", "../data/concepts.js", "../assets/js/site.js"))
    check_other_pages()
    check_log(papers)
    check_repo_rules()

    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    print(f"\n檢查完成：{len(papers)} 篇論文、{len(concepts)} 個概念，{len(errors)} 個錯誤，{len(warnings)} 個警告。")
    if errors:
        sys.exit(1)
    print("全部通過。")


if __name__ == "__main__":
    main()
