"""Tools available to the financial analyst agent."""

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Tool:
    name: str
    description: str
    runner: Callable[..., str]


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
            runner=lambda ticker: f"Stub: fetch market data for {ticker}",
        ),
    ]
