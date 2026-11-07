# 我的論文文獻庫

碩士論文「雙平行機環境下的雙代理人資源分配排程」的參考文獻整理網站。每篇論文一頁、依固定欄位整理，首頁提供跨論文比較表與研究構面覆蓋表。

- 網站：https://jason01302003.github.io/PaperNote/
- 規則文件（給 AI 讀）：[CLAUDE.md](CLAUDE.md)

## 這個專案的重點

這不是一次性做出一個網頁，而是建立一套規則，讓 AI 之後能依同一套方式持續新增論文頁：

1. `CLAUDE.md` 定義目的、結構、命名、頁面格式、寫作風格、誠信與版權規則。
2. `data/papers.js` 是單一事實來源，首頁、導覽、書目與引用格式都由它產生。
3. `scripts/new_paper.py` 從模板建立新頁；`scripts/check.py` 自動驗證規則。

## 新增一篇論文

```bash
python scripts/new_paper.py kononov-2006-multiple-crews \
  --title "On relocation problems with multiple identical working crews" \
  --authors "A.V. Kononov" "B.M.T. Lin" \
  --year 2006 --venue "Discrete Optimization" \
  --volume "3(4)" --pages "366–381" --doi "10.1016/j.disopt.2006.06.003"

# 填寫頁面內容與 data/papers.js 的欄位後：
python scripts/check.py
```

## 本機預覽

純靜態網站，直接用瀏覽器開啟 `index.html` 即可，或：

```bash
python -m http.server 8000
```

## 版權與隱私

論文原文 PDF 有版權，放在 `參考文獻/`（已被 `.gitignore` 排除，不會上傳）。網站只放作者自己的整理與 DOI 連結。
