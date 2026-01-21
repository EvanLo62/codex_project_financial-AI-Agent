"""Retriever logic for the RAG pipeline."""

from typing import Callable, List, Dict


def build_retriever(vector_db) -> Callable[[str], List[Dict[str, str]]]:
    def retrieve(query: str) -> List[Dict[str, str]]:
        documents = vector_db.search(query)
        return documents

    return retrieve
