"""Tools available to the financial analyst agent."""

from dataclasses import dataclass
from typing import Callable, List

import yfinance as yf


@dataclass
class Tool:
    name: str
    description: str
    runner: Callable[..., str]


def _summarize_market_data(ticker: str) -> str:
    stock = yf.Ticker(ticker)
    info = stock.info or {}
    return (
        "公司基本資訊："
        f"名稱={info.get('shortName')}, "
        f"產業={info.get('industry')}, "
        f"市值={info.get('marketCap')}, "
        f"本益比={info.get('trailingPE')}"
    )


def get_tools(retriever) -> List[Tool]:
    return [
        Tool(
            name="retrieve_documents",
            description="檢索與問題相關的財報或新聞內容",
            runner=lambda query: "\n".join(doc["content"] for doc in retriever(query)),
        ),
        Tool(
            name="fetch_market_data",
            description="查詢公司近期股價與指標",
            runner=_summarize_market_data,
        ),
    ]
