/* 全站共用腳本（ES5，無外部依賴）。
   負責：頁首／頁尾、首頁比較表與概念清單、論文頁與概念頁的書目資訊／目錄／交叉連結。
   資料來源只有 data/site.js、data/papers.js、data/concepts.js。 */
(function () {
  "use strict";

  var SITE = window.SITE || {};
  var PAPERS = (window.PAPERS || []).slice().sort(function (a, b) {
    return a.year - b.year || a.slug.localeCompare(b.slug);
  });
  var CONCEPTS = (window.CONCEPTS || []).slice().sort(function (a, b) {
    return b.papers.length - a.papers.length || a.slug.localeCompare(b.slug);
  });
  var body = document.body;
  var root = body.dataset.root || "";
  var page = body.dataset.page || "";

  /* ---------- 小工具 ---------- */
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") node.textContent = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(c); });
    return node;
  }
  function find(list, slug) {
    for (var i = 0; i < list.length; i++) if (list[i].slug === slug) return list[i];
    return null;
  }
  function paperUrl(p) { return root + "papers/" + p.slug + ".html"; }
  function conceptUrl(c) { return root + "concepts/" + c.slug + ".html"; }
  function surname(name) { var parts = name.split(" "); return parts[parts.length - 1]; }
  function initials(name) { return name.slice(0, name.lastIndexOf(" ")); }

  /* 例：Kononov & Lin (2006)、Lee et al. (2014) */
  function label(p) {
    var s = p.authors.map(surname);
    if (s.length === 1) return s[0] + " (" + p.year + ")";
    if (s.length === 2) return s[0] + " & " + s[1] + " (" + p.year + ")";
    return s[0] + " et al. (" + p.year + ")";
  }

  /* 例：Kononov, A.V., & Lin, B.M.T. (2006). Title. Venue, 3(4), 366–381. https://doi.org/… */
  function citation(p) {
    var names = p.authors.map(function (a) { return surname(a) + ", " + initials(a); });
    var who = names.length > 1 ? names.slice(0, -1).join(", ") + ", & " + names[names.length - 1] : names[0];
    return who + " (" + p.year + "). " + p.title + ". " + p.venue + ", " + p.volume + ", " + p.pages + ". https://doi.org/" + p.doi;
  }

  function statusBadge(status) {
    var cls = status === "已確認" ? "status-ok" : status === "初整理" ? "status-draft" : "status-todo";
    return el("span", { "class": "status " + cls, text: status });
  }

  function linkList(items, makeLink) {
    var box = el("span");
    items.forEach(function (it, i) {
      if (i) box.appendChild(document.createTextNode("、"));
      box.appendChild(makeLink(it));
    });
    return box;
  }
  function conceptLinks(slugs) {
    return linkList(slugs.map(function (s) { return find(CONCEPTS, s); }).filter(Boolean), function (c) {
      return el("a", { href: conceptUrl(c), text: c.title });
    });
  }
  function paperLinks(slugs) {
    return linkList(slugs.map(function (s) { return find(PAPERS, s); }).filter(Boolean), function (p) {
      return el("a", { href: paperUrl(p), text: label(p) });
    });
  }

  /* ---------- 頁首／頁尾 ---------- */
  function buildChrome() {
    var nav = el("nav", { "class": "site-nav", "aria-label": "主選單" }, [
      el("a", { href: root + "index.html", text: "文獻與概念" }),
      el("a", { href: root + "about.html", text: "專案規則" })
    ]);
    if (page === "index") nav.firstChild.setAttribute("aria-current", "page");
    if (page === "about") nav.lastChild.setAttribute("aria-current", "page");
    if (SITE.repo) nav.appendChild(el("a", { href: SITE.repo, rel: "noopener", text: "GitHub" }));

    body.insertBefore(el("header", { "class": "site-header" }, [
      el("div", { "class": "inner" }, [el("a", { "class": "brand", href: root + "index.html", text: SITE.title || "文獻庫" }), nav])
    ]), body.firstChild);
    body.appendChild(el("footer", { "class": "site-footer", text: SITE.footer || "" }));

    var links = document.querySelectorAll("a[data-repo]");
    for (var i = 0; i < links.length; i++) {
      links[i].setAttribute("href", (SITE.repo || "#") + "/blob/main/" + links[i].getAttribute("data-repo"));
    }
  }

  /* ---------- 首頁 ---------- */
  function buildIndex() {
    var count = document.querySelector("[data-paper-count]");
    if (count) count.textContent = PAPERS.length;
    var ccount = document.querySelector("[data-concept-count]");
    if (ccount) ccount.textContent = CONCEPTS.length;

    var compare = document.querySelector("[data-compare]");
    var filters = document.querySelector("[data-filters]");
    var active = "全部";

    function renderCompare() {
      compare.innerHTML = "";
      var rows = PAPERS.filter(function (p) { return active === "全部" || p.tags.indexOf(active) > -1; });
      var thead = el("thead", {}, [el("tr", {}, ["論文", "機台", "代理人", "資源", "目標", "主要結果", "狀態"].map(function (h) {
        return el("th", { text: h });
      }))]);
      var tbody = el("tbody");
      rows.forEach(function (p) {
        tbody.appendChild(el("tr", {}, [
          el("td", { "class": "paper" }, [el("a", { href: paperUrl(p), text: label(p) }), el("small", { text: p.title })]),
          el("td", { text: p.machine }),
          el("td", { text: p.agents }),
          el("td", { text: p.resource }),
          el("td", { text: p.objective }),
          el("td", { text: p.result }),
          el("td", {}, [statusBadge(p.status)])
        ]));
      });
      compare.appendChild(el("table", {}, [thead, tbody]));
    }

    function renderFacets() {
      var host = document.querySelector("[data-facets]");
      if (!host) return;
      var cols = [["parallel", "平行機"], ["twoAgent", "雙代理人"], ["resource", "資源限制"]];
      var head = el("tr", {}, [el("th", { text: "論文" })].concat(cols.map(function (c) { return el("th", { "class": "center", text: c[1] }); })));
      var tbody = el("tbody");
      var all = 0;
      PAPERS.forEach(function (p) {
        if (cols.every(function (c) { return p.facets[c[0]]; })) all++;
        tbody.appendChild(el("tr", {}, [el("td", { "class": "paper" }, [el("a", { href: paperUrl(p), text: label(p) })])].concat(
          cols.map(function (c) {
            return el("td", { "class": "center" }, [el("span", { "class": p.facets[c[0]] ? "yes" : "no", text: p.facets[c[0]] ? "✓" : "—" })]);
          })
        )));
      });
      host.innerHTML = "";
      host.appendChild(el("table", {}, [el("thead", {}, [head]), tbody]));
      var note = document.querySelector("[data-facet-summary]");
      if (note) note.textContent = "目前 " + PAPERS.length + " 篇之中，同時涵蓋三個構面的有 " + all + " 篇。";
    }

    function renderConcepts() {
      var host = document.querySelector("[data-concepts]");
      if (!host) return;
      var thead = el("thead", {}, [el("tr", {}, ["概念", "一句話定義", "相關論文", "狀態"].map(function (h) { return el("th", { text: h }); }))]);
      var tbody = el("tbody");
      CONCEPTS.forEach(function (c) {
        tbody.appendChild(el("tr", {}, [
          el("td", { "class": "paper" }, [el("a", { href: conceptUrl(c), text: c.title }), el("small", { text: c.titleEn })]),
          el("td", { text: c.summary }),
          el("td", {}, [paperLinks(c.papers)]),
          el("td", {}, [statusBadge(c.status)])
        ]));
      });
      host.innerHTML = "";
      host.appendChild(el("table", {}, [thead, tbody]));
    }

    if (filters) {
      var tags = ["全部"];
      PAPERS.forEach(function (p) { p.tags.forEach(function (t) { if (tags.indexOf(t) < 0) tags.push(t); }); });
      tags.forEach(function (t) {
        var b = el("button", { "class": "chip", type: "button", "aria-pressed": t === active ? "true" : "false", text: t });
        b.addEventListener("click", function () {
          active = t;
          var chips = filters.querySelectorAll(".chip");
          for (var i = 0; i < chips.length; i++) chips[i].setAttribute("aria-pressed", chips[i] === b ? "true" : "false");
          renderCompare();
        });
        filters.appendChild(b);
      });
    }
    if (compare) renderCompare();
    renderFacets();
    renderConcepts();
  }

  /* ---------- 論文頁與概念頁共用：目錄 ---------- */
  function buildToc() {
    var toc = document.querySelector("[data-toc]");
    if (!toc) return;
    var heads = document.querySelectorAll("article > h2[id]");
    if (!heads.length) return;
    var ol = el("ol");
    for (var i = 0; i < heads.length; i++) {
      ol.appendChild(el("li", {}, [el("a", { href: "#" + heads[i].id, text: heads[i].textContent })]));
    }
    toc.appendChild(el("strong", { text: "本頁目錄" }));
    toc.appendChild(ol);
  }

  function bibRow(bib, dt, node) {
    bib.appendChild(el("dt", { text: dt }));
    bib.appendChild(el("dd", {}, [node]));
  }

  /* ---------- 論文頁 ---------- */
  function buildPaper() {
    var slug = body.dataset.slug;
    var idx = -1;
    PAPERS.forEach(function (p, i) { if (p.slug === slug) idx = i; });
    var p = PAPERS[idx];

    var bib = document.querySelector("[data-bib]");
    if (bib && p) {
      bibRow(bib, "作者", document.createTextNode(p.authors.join(", ")));
      bibRow(bib, "發表", document.createTextNode(p.venue + ", " + p.volume + ", " + p.pages + " (" + p.year + ")"));
      bibRow(bib, "DOI", el("a", { href: "https://doi.org/" + p.doi, rel: "noopener", text: p.doi }));
      var tagBox = el("span");
      p.tags.forEach(function (t) { tagBox.appendChild(el("span", { "class": "tag", text: t })); });
      bibRow(bib, "標籤", tagBox);
      if (p.concepts.length) bibRow(bib, "相關概念", conceptLinks(p.concepts));
      bibRow(bib, "整理狀態", el("span", {}, [statusBadge(p.status), document.createTextNode("　更新於 " + p.date)]));

      var cite = el("code", { "class": "cite-box", text: citation(p) });
      var btn = el("button", { "class": "btn", type: "button", text: "複製引用" });
      btn.addEventListener("click", function () {
        if (!navigator.clipboard) return;
        navigator.clipboard.writeText(citation(p)).then(function () {
          btn.textContent = "已複製";
          setTimeout(function () { btn.textContent = "複製引用"; }, 1500);
        });
      });
      bib.appendChild(el("dt", { text: "引用格式" }));
      bib.appendChild(el("dd", {}, [cite, btn]));
    }

    buildToc();

    var nav = document.querySelector("[data-paper-nav]");
    if (nav && idx > -1) {
      if (PAPERS[idx - 1]) nav.appendChild(el("a", { "class": "prev", href: paperUrl(PAPERS[idx - 1]) }, [el("small", { text: "← 上一篇" }), el("span", { text: label(PAPERS[idx - 1]) })]));
      if (PAPERS[idx + 1]) nav.appendChild(el("a", { "class": "next", href: paperUrl(PAPERS[idx + 1]) }, [el("small", { text: "下一篇 →" }), el("span", { text: label(PAPERS[idx + 1]) })]));
    }
  }

  /* ---------- 概念頁 ---------- */
  function buildConcept() {
    var c = find(CONCEPTS, body.dataset.slug);
    var bib = document.querySelector("[data-bib]");
    if (bib && c) {
      bibRow(bib, "英文名稱", document.createTextNode(c.titleEn));
      bibRow(bib, "一句話定義", document.createTextNode(c.summary));
      bibRow(bib, "相關論文", paperLinks(c.papers));
      if (c.related.length) bibRow(bib, "相關概念", conceptLinks(c.related));
      bibRow(bib, "整理狀態", el("span", {}, [statusBadge(c.status), document.createTextNode("　更新於 " + c.date)]));
    }
    buildToc();
  }

  buildChrome();
  if (page === "index") buildIndex();
  if (page === "paper") buildPaper();
  if (page === "concept") buildConcept();
})();
