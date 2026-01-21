"""News scraping utilities."""

from typing import List

import yfinance as yf


def fetch_latest_news(ticker: str, limit: int = 5) -> List[str]:
    news_items = yf.Ticker(ticker).news or []
    headlines = []
    for item in news_items[:limit]:
        title = item.get("title")
        link = item.get("link")
        if title and link:
            headlines.append(f"{title} ({link})")
        elif title:
            headlines.append(title)
    return headlines
