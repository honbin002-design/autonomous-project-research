# 自主研究系統 (Autonomous Research System)

自主研究系統（Autonomous Research System）是一個基於檢查點（Checkpoint-Driven）驅動的自動化研究與實驗開發框架。本系統旨在實現持續研究、實驗紀錄、狀態追蹤與疊代改進。

## 系統架構 (System Architecture)

系統核心由以下元件組成：

1. **`CHECKPOINT.md`**：研究狀態的核心記錄檔。記錄當前研究進度、實驗假設、累積發現與下一步研究計劃。
2. **`src/research_runner.py`**：自動化研究執行器。讀取檢查點狀態、執行指定的檢驗與研究步驟、記錄日誌並更新狀態。
3. **`tests/`**：單元測試與驗證模組。確保研究執行器與工具鏈之穩定性。
4. **`research_logs/`**：研究與實驗執行的詳細日誌輸出目錄。

## 工作流程 (Workflow)

```
[ 讀取 CHECKPOINT.md ] ──> [ 確定下一步任務 ] ──> [ 執行研究 / 實驗步驟 ]
         ▲                                                │
         └─────────────── [ 更新 CHECKPOINT.md ] <────────┘
```

1. **讀取狀態**：讀取 `CHECKPOINT.md` 中尚未完成的最新步驟。
2. **執行研究**：根據任務指示執行分析、代碼實現或數據驗證。
3. **紀錄結果**：將結果寫入研究日誌 (`research_logs/`)。
4. **更新檢查點**：更新 `CHECKPOINT.md` 中的狀態矩陣與實驗發現，並展開下一個研究步驟。

## 使用說明 (Usage)

### 執行研究步驟
```bash
python3 src/research_runner.py --step 1
```

### 執行單元測試
```bash
python3 -m unittest discover tests
```

## 目錄結構 (Directory Structure)
```
.
├── README.md                 # 系統說明文件
├── CHECKPOINT.md             # 研究檢查點與追蹤記錄
├── src/
│   └── research_runner.py    # 研究執行器核心邏輯
├── tests/
│   └── test_research_runner.py # 研究執行器測試用例
└── research_logs/            # 研究執行日誌目錄
```
