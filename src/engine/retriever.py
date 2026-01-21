"""Retriever logic for the RAG pipeline."""

from typing import Callable, List, Dict


def build_retriever(vector_db, k: int = 4) -> Callable[[str], List[Dict[str, str]]]:
    def retrieve(query: str) -> List[Dict[str, str]]:
        return vector_db.search(query, k=k)

    return retrieve
