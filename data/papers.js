window.PAPERS = [
  {
    "slug": "kononov-2006-multiple-crews",
    "title": "On relocation problems with multiple identical working crews",
    "authors": [
      "A.V. Kononov",
      "B.M.T. Lin"
    ],
    "year": 2006,
    "venue": "Discrete Optimization",
    "volume": "3(4)",
    "pages": "366–381",
    "doi": "10.1016/j.disopt.2006.06.003",
    "summary": "多台相同機的 relocation：兩機 UET strongly NP-hard，2- 與 (3−2/m)-近似。",
    "tags": [
      "relocation",
      "資源限制排程",
      "平行機",
      "複雜度",
      "近似演算法"
    ],
    "concepts": [
      "relocation-problem",
      "parallel-machines",
      "np-hardness",
      "approximation-algorithms",
      "johnsons-rule-flowshop"
    ],
    "machine": "m 台相同平行機（含 m = 2）",
    "agents": "單一",
    "resource": "有（α, β, V₀）",
    "objective": "Cmax",
    "result": "兩機 UET strongly NP-hard；2-近似；(3−2/m)-近似",
    "facets": {
      "parallel": true,
      "twoAgent": false,
      "resource": true
    },
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "cheng-2009-johnson-composite",
    "title": "Johnson's rule, composite jobs and the relocation problem",
    "authors": [
      "T.C.E. Cheng",
      "B.M.T. Lin"
    ],
    "year": 2009,
    "venue": "European Journal of Operational Research",
    "volume": "192(3)",
    "pages": "1008–1013",
    "doi": "10.1016/j.ejor.2007.11.035",
    "summary": "Composite job 加速 flowshop 問題；以 relocation 詮釋 Johnson's rule。",
    "tags": [
      "relocation",
      "flowshop",
      "資源限制排程"
    ],
    "concepts": [
      "johnsons-rule-flowshop",
      "relocation-problem"
    ],
    "machine": "兩機 flowshop（對應單機 relocation）",
    "agents": "單一",
    "resource": "有（a, b, v₀）",
    "objective": "Cmax（F2||Cmax）／最小初始資源",
    "result": "composite job 使數個相關問題的時間複雜度下降；Johnson's rule 的 relocation 詮釋",
    "facets": {
      "parallel": false,
      "twoAgent": false,
      "resource": true
    },
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "kononov-2010-weighted-completion",
    "title": "Minimizing the total weighted completion time in the relocation problem",
    "authors": [
      "A.V. Kononov",
      "B.M.T. Lin"
    ],
    "year": 2010,
    "venue": "Journal of Scheduling",
    "volume": "13(2)",
    "pages": "123–129",
    "doi": "10.1007/s10951-009-0151-7",
    "summary": "單機 relocation 的 ΣwC：四特例 strongly NP-hard，UET 且 δ ≥ 0 時 2-近似。",
    "tags": [
      "relocation",
      "資源限制排程",
      "單機",
      "複雜度",
      "近似演算法"
    ],
    "concepts": [
      "relocation-problem",
      "np-hardness",
      "approximation-algorithms",
      "johnsons-rule-flowshop"
    ],
    "machine": "單機",
    "agents": "單一",
    "resource": "有（α, β, V₀）",
    "objective": "ΣwC",
    "result": "四個特例 strongly NP-hard；UET 與單位權重情形完全等價；2-近似",
    "facets": {
      "parallel": false,
      "twoAgent": false,
      "resource": true
    },
    "status": "已確認",
    "date": "2026-11-08"
  },
  {
    "slug": "lee-2014-two-agent",
    "title": "Single-Machine Scheduling to Minimize Total Completion Time and Tardiness with Two Competing Agents",
    "authors": [
      "W.-C. Lee",
      "Y.-R. Shiau",
      "Y.-H. Chung",
      "L. Ding"
    ],
    "year": 2014,
    "venue": "The Scientific World Journal",
    "volume": "2014",
    "pages": "Article ID 596306 (9 pp.)",
    "doi": "10.1155/2014/596306",
    "summary": "單機兩代理人：在代理人 2 不得有延遲工作的限制下，最小化代理人 1 的總完工時間與總延遲的加權組合。",
    "tags": [
      "兩代理人",
      "單機",
      "分支定界",
      "模擬退火"
    ],
    "concepts": [
      "two-agent-scheduling",
      "np-hardness",
      "solution-methods"
    ],
    "machine": "單機",
    "agents": "兩個（競爭）",
    "resource": "無",
    "objective": "AG1 的 θΣT + (1−θ)ΣC，且 AG2 無延遲工作",
    "result": "分支定界可解至 24 個工作；兩種 SA 的平均誤差皆低於 1%（n ≤ 24）",
    "facets": {
      "parallel": false,
      "twoAgent": true,
      "resource": false
    },
    "status": "初整理",
    "date": "2026-11-08"
  },
  {
    "slug": "lin-2016-fixed-sequences",
    "title": "Relocation scheduling subject to fixed processing sequences",
    "authors": [
      "B.M.T. Lin",
      "F.J. Hwang",
      "A.V. Kononov"
    ],
    "year": 2016,
    "venue": "Journal of Scheduling",
    "volume": "19(2)",
    "pages": "153–163",
    "doi": "10.1007/s10951-015-0455-8",
    "summary": "兩台平行專用機、加工順序已固定的 relocation problem：針對六種目標函數給出複雜度分類與動態規劃演算法。",
    "tags": [
      "relocation",
      "資源限制排程",
      "平行機",
      "動態規劃",
      "複雜度"
    ],
    "concepts": [
      "relocation-problem",
      "parallel-machines",
      "np-hardness",
      "approximation-algorithms",
      "solution-methods",
      "johnsons-rule-flowshop"
    ],
    "machine": "2 台平行專用機（加工順序固定）",
    "agents": "單一",
    "resource": "有（α, β, v₀）",
    "objective": "Cmax、ΣwC、Lmax、ΣwT、ΣwU、ΣU",
    "result": "Cmax／ΣwC／Lmax 與 ΣU 多項式時間可解；ΣwT、ΣwU 為 ordinary NP-hard",
    "facets": {
      "parallel": true,
      "twoAgent": false,
      "resource": true
    },
    "status": "已確認",
    "date": "2026-11-08"
  }
];
