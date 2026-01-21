"""Vector database access layer."""

from typing import List, Dict


class VectorDatabase:
    def __init__(self, persist_path: str = "data/vector_store") -> None:
        self.persist_path = persist_path

    def search(self, query: str) -> List[Dict[str, str]]:
        return [
            {
                "content": f"Stub vector search result for: {query}",
                "source": "vector_db",
            }
        ]
