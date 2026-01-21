"""Streamlit entry point for the Financial AI Agent."""

import os
from pathlib import Path
from typing import List

import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agents.analyst import ANALYST_PROMPT, build_analysis_prompt
from agents.tools import get_tools
from engine.retriever import build_retriever
from engine.vector_db import VectorDatabase
from utils.scraper import fetch_latest_news


def load_pdfs(pdf_dir: Path) -> List[Document]:
    documents: List[Document] = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        documents.extend(splitter.split_documents(pages))
    return documents


def main() -> None:
    load_dotenv()
    st.set_page_config(page_title="Financial AI Agent", layout="wide")
    st.title("Financial AI Agent")

    st.sidebar.header("資料來源")
    company = st.sidebar.text_input("公司代號", value="TSM")
    question = st.text_area("輸入你的問題", placeholder="請問這家公司近期的財報亮點是什麼？")
    pdf_dir = Path("data/raw_pdfs")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        st.sidebar.warning("尚未設定 OPENAI_API_KEY，請先更新 .env。")
        vector_db = None
        retriever = None
        tools = []
    else:
        vector_db = VectorDatabase()
        retriever = build_retriever(vector_db)
        tools = get_tools(retriever)

    if st.sidebar.button("重新匯入 PDF"):
        if vector_db is None:
            st.sidebar.error("請先設定 OPENAI_API_KEY。")
            return
        if not pdf_dir.exists():
            st.sidebar.warning("尚未找到 data/raw_pdfs 目錄。")
        else:
            docs = load_pdfs(pdf_dir)
            ingested = vector_db.ingest_documents(docs)
            st.sidebar.success(f"已匯入 {ingested} 份文件頁面。")

    if st.button("開始分析"):
        if vector_db is None or retriever is None:
            st.error("請先在 .env 設定 OPENAI_API_KEY。")
            return

        st.info("正在整理資料與分析...")
        news = fetch_latest_news(company)
        retrieved_docs = retriever(question)
        context = "\n".join(doc["content"] for doc in retrieved_docs)
        analysis_prompt = build_analysis_prompt(question, context)

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        response = llm.invoke(analysis_prompt)

        st.subheader("分析師設定")
        st.code(ANALYST_PROMPT)

        st.subheader("資料摘要")
        st.write({"company": company, "news": news, "tools": [tool.name for tool in tools]})

        st.subheader("分析結果")
        st.write(response.content)


if __name__ == "__main__":
    main()
