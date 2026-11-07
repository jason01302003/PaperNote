window.CONCEPTS = [
  {
    "slug": "relocation-problem",
    "title": "Relocation problem 與資源回收模型",
    "titleEn": "Relocation problem",
    "summary": "工作開始時消耗 α 單位資源、完成時歸還 β 單位（β 可大於、等於或小於 α）的資源限制排程。",
    "papers": [
      "kononov-2006-multiple-crews",
      "cheng-2009-johnson-composite",
      "kononov-2010-weighted-completion",
      "lin-2016-fixed-sequences"
    ],
    "related": [
      "johnsons-rule-flowshop",
      "parallel-machines",
      "np-hardness"
    ],
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "johnsons-rule-flowshop",
    "title": "兩機 flowshop 與 Johnson's rule",
    "titleEn": "Two-machine flowshop and Johnson's rule",
    "summary": "F2||Cmax 的經典最佳排序規則，及其與單機 relocation problem 的等價關係。",
    "papers": [
      "cheng-2009-johnson-composite",
      "kononov-2006-multiple-crews",
      "kononov-2010-weighted-completion",
      "lin-2016-fixed-sequences"
    ],
    "related": [
      "relocation-problem"
    ],
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "np-hardness",
    "title": "計算複雜度：strongly NP-hard 與 ordinary NP-hard",
    "titleEn": "NP-hardness",
    "summary": "整理各文獻對問題難度的分類：strongly NP-hard、ordinary NP-hard、擬多項式與多項式可解。",
    "papers": [
      "kononov-2006-multiple-crews",
      "kononov-2010-weighted-completion",
      "lin-2016-fixed-sequences",
      "lee-2014-two-agent"
    ],
    "related": [
      "approximation-algorithms",
      "solution-methods",
      "relocation-problem"
    ],
    "status": "初整理",
    "date": "2026-11-08"
  },
  {
    "slug": "approximation-algorithms",
    "title": "近似演算法與近似比",
    "titleEn": "Approximation algorithms",
    "summary": "多項式時間演算法對任何實例保證解不超過最佳值的 ρ 倍，以及相關的不可近似性結果。",
    "papers": [
      "kononov-2006-multiple-crews",
      "kononov-2010-weighted-completion",
      "lin-2016-fixed-sequences"
    ],
    "related": [
      "np-hardness",
      "relocation-problem"
    ],
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "parallel-machines",
    "title": "平行機與專用機",
    "titleEn": "Parallel and dedicated machines",
    "summary": "多台機器同時加工；區分工作可用任一台的相同機，與工作事先指定機台的專用機。",
    "papers": [
      "kononov-2006-multiple-crews",
      "lin-2016-fixed-sequences"
    ],
    "related": [
      "relocation-problem",
      "solution-methods"
    ],
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "two-agent-scheduling",
    "title": "雙代理人排程",
    "titleEn": "Two-agent scheduling",
    "summary": "兩個代理人各擁有一組工作與各自的目標函數，競爭同一組機器。",
    "papers": [
      "lee-2014-two-agent"
    ],
    "related": [
      "solution-methods",
      "np-hardness"
    ],
    "status": "初整理",
    "date": "2026-11-08"
  },
  {
    "slug": "solution-methods",
    "title": "精確法與啟發式：動態規劃、分支定界、模擬退火",
    "titleEn": "Exact and heuristic methods",
    "summary": "本庫文獻用到的求解方法：動態規劃、分支定界與模擬退火，及其適用情境。",
    "papers": [
      "lin-2016-fixed-sequences",
      "lee-2014-two-agent"
    ],
    "related": [
      "np-hardness",
      "two-agent-scheduling",
      "parallel-machines"
    ],
    "status": "初整理",
    "date": "2026-11-08"
  }
];
