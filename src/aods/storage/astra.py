"""Astra DB vector embedding storage wrapper."""

import logging

try:
    from astrapy.db import AstraDB
except Exception:  # pragma: no cover - optional
    AstraDB = None
    logging.warning("Astra DB client not available; vector storage disabled")


class AstraVectorStore:
    """Store and query embeddings in Astra DB."""

    def __init__(self, token: str | None = None, api_endpoint: str | None = None, collection="embeddings"):
        self.db = AstraDB(token=token, api_endpoint=api_endpoint) if AstraDB and token and api_endpoint else None
        self.collection = collection

    def upsert(self, items):
        if self.db is None:
            return
        self.db.insert_many(self.collection, items)

    def query(self, embedding, top_k=5):
        if self.db is None:
            return []
        return self.db.vector_find(self.collection, embedding, top_k=top_k)
