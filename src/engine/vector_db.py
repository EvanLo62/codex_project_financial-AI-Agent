"""Vector database access layer."""

from typing import Iterable, List, Dict

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


class VectorDatabase:
    def __init__(self, persist_path: str = "data/vector_store") -> None:
        self.persist_path = persist_path
        self.embeddings = OpenAIEmbeddings()
        self._store = Chroma(
            persist_directory=self.persist_path,
            embedding_function=self.embeddings,
        )

    def ingest_documents(self, documents: Iterable[Document]) -> int:
        docs = list(documents)
        if not docs:
            return 0
        self._store.add_documents(docs)
        self._store.persist()
        return len(docs)

    def search(self, query: str, k: int = 4) -> List[Dict[str, str]]:
        results = self._store.similarity_search(query, k=k)
        return [
            {"content": doc.page_content, "source": doc.metadata.get("source", "unknown")}
            for doc in results
        ]
