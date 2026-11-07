# 操作紀錄

只增不改。格式與規則見 [CLAUDE.md](CLAUDE.md) §9.4。

## [2026-11-08] schema | 建立 CLAUDE.md（LLM Wiki 模式）與網站骨架
- 新增：CLAUDE.md、README.md、assets/、data/、templates/、scripts/
- 決定：風格為白＋綠；Wiki 頁面直接以 HTML 維護；PDF 不上傳

## [2026-11-08] ingest | kononov-2006-multiple-crews
- 新增：papers/kononov-2006-multiple-crews.html
- 更新：concepts/relocation-problem、parallel-machines、np-hardness、approximation-algorithms、johnsons-rule-flowshop；data/papers.js、data/concepts.js
- 發現：Thm 2 與結論對「非負／正」的用語不一致（待確認）

## [2026-11-08] ingest | cheng-2009-johnson-composite
- 新增：papers/cheng-2009-johnson-composite.html
- 更新：concepts/johnsons-rule-flowshop、relocation-problem
- 發現：原文把 Kononov & Lin (2006) 的卷頁誤寫為 21, 368–381；引用的 submitted 稿件標題與 Kononov & Lin (2010) 不同（待確認）

## [2026-11-08] ingest | kononov-2010-weighted-completion
- 新增：papers/kononov-2010-weighted-completion.html
- 更新：concepts/relocation-problem、np-hardness、approximation-algorithms、johnsons-rule-flowshop
- 發現：PDF 為預印本，無期刊頁碼，卷期頁碼取自 Lin et al. (2016) 的參考文獻（待確認）

## [2026-11-08] ingest | lee-2014-two-agent
- 新增：papers/lee-2014-two-agent.html
- 更新：concepts/two-agent-scheduling、np-hardness、solution-methods
- 發現：參數 P 的指涉前後敘述不一致；表 6 的 CPU 時間與內文「小於 1 秒」不符（待確認）

## [2026-11-08] ingest | lin-2016-fixed-sequences
- 新增：papers/lin-2016-fixed-sequences.html
- 更新：concepts/relocation-problem、parallel-machines、np-hardness、approximation-algorithms、solution-methods、johnsons-rule-flowshop
- 發現：本文把一般兩專用機的 strongly NP-hard 結論由兩篇前作推得（待確認）

## [2026-11-08] fix | 樣式：手機寬度的表格與來源標記溢出、頁首換行
- 更新：assets/css/style.css
- 驗證：14 個頁面在 375px 寬度下無橫向捲軸

## [2026-11-08] update | repo 名稱改為 PaperNote
- 更新：data/site.js（GitHub 連結）、README.md（網站網址）

## [2026-11-08] update | 4 篇論文狀態改為已確認
- 依作者指示：kononov-2006-multiple-crews、cheng-2009-johnson-composite、kononov-2010-weighted-completion、lin-2016-fixed-sequences 改為已確認
- 更新：data/papers.js；移除這 4 篇與 concepts/relocation-problem、np-hardness、approximation-algorithms 中的「待確認」標記與「請對照原文」的備註
- 未變動：lee-2014-two-agent 與所有概念頁仍為初整理，two-agent-scheduling 的待確認標記保留

## [2026-11-08] schema | 新增規則：已確認的頁面不得含待確認標記
- 更新：CLAUDE.md §5、scripts/check.py、about.html

## [2026-11-08] update | 4 個概念頁狀態改為已確認
- 依作者指示：relocation-problem、johnsons-rule-flowshop、approximation-algorithms、parallel-machines 改為已確認（皆只依賴已確認的論文）
- 更新：data/concepts.js、about.html
- 未變動：np-hardness、two-agent-scheduling、solution-methods 仍為初整理（用到 lee-2014-two-agent）
