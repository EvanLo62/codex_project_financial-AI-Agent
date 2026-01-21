"""Streamlit entry point for the Financial AI Agent."""

import streamlit as st

from agents.analyst import ANALYST_PROMPT
from agents.tools import get_tools
from engine.retriever import build_retriever
from engine.vector_db import VectorDatabase
from utils.scraper import fetch_latest_news


def main() -> None:
    st.set_page_config(page_title="Financial AI Agent", layout="wide")
    st.title("Financial AI Agent")

    st.sidebar.header("資料來源")
    company = st.sidebar.text_input("公司代號", value="TSM")
    question = st.text_area("輸入你的問題", placeholder="請問這家公司近期的財報亮點是什麼？")

    if st.button("開始分析"):
        st.info("正在整理資料與分析...")
        news = fetch_latest_news(company)
        vector_db = VectorDatabase()
        retriever = build_retriever(vector_db)

        tools = get_tools(retriever)
        st.subheader("分析師設定")
        st.code(ANALYST_PROMPT)

        st.subheader("資料摘要")
        st.write({"company": company, "news": news, "tools": [tool.name for tool in tools]})

        st.success("分析完成（示範輸出）。")


if __name__ == "__main__":
    main()
