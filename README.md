# Financial AI Agent

本專案是一個金融 AI 助理的範例架構，重點展示資料攝入、RAG/Agent 核心引擎，以及對使用者互動的介面層。目標是提供一個可擴充的模板，方便接入財報、新聞、API 等多元資料源並輸出分析報告。

## 系統架構

系統拆分為三個主要層級：

1. **Data Ingestion（資料攝入）**：負責抓取財報、新聞或 API 數據。
2. **Core Engine（核心引擎）**：包含 RAG（Retrieval）與 Agent（Decision）邏輯。
3. **Interface（介面）**：讓用戶輸入問題並呈現分析報告。

```
financial-ai-agent/
│
├── data/               # 存放原始數據與快取
│   ├── raw_pdfs/       # 存放抓下來的財報 (e.g., TSMC_2025.pdf)
│   └── vector_store/   # 存放向量資料庫的持久化檔案 (ChromaDB/FAISS)
│
├── src/                # 原始程式碼
│   ├── main.py         # 程式進入點 (Streamlit App)
│   │
│   ├── agents/         # AI 決策邏輯
│   │   ├── analyst.py  # 定義分析師的角色 (System Prompt)
│   │   └── tools.py    # 定義 Agent 能使用的工具 (yfinance, search)
│   │
│   ├── engine/         # 核心 RAG 引擎
│   │   ├── retriever.py# 負責檢索 (可放 Reranker)
│   │   └── vector_db.py# 向量資料庫的讀寫操作
│   │
│   └── utils/          # 共用工具
│       ├── finance.py  # 計算 Sharpe Ratio, 波動率等數學公式
│       └── scraper.py  # 爬取金融新聞或 API 的邏輯
│
├── .env                # 存放 API Keys (OPENAI_API_KEY, TAVILY_API_KEY)
├── requirements.txt    # 專案依賴 (langchain, yfinance, streamlit...)
└── README.md           # 專案說明與運行步驟
```

## 快速開始

1. 建立虛擬環境並安裝依賴：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 設定環境變數：

```bash
cp .env.example .env
```

並在 `.env` 中填入 `OPENAI_API_KEY`（向量化與分析需要）。

3. 將財報 PDF 放入 `data/raw_pdfs/`。

4. 啟動應用：

```bash
streamlit run src/main.py
```

## 延伸方向

- 將 `utils/scraper.py` 接入實際的新聞 API 或 RSS。
- 在 `engine/retriever.py` 中加入自訂 reranker 或混合檢索策略。
- 於 `agents/tools.py` 擴充更多工具（例如財報解析、KPI 計算）。
