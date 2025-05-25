"""Connector for template marketplace pricing data."""

import logging
from .base import DataConnector

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None


class TemplateMarketplaceConnector(DataConnector):
    """Pull listing data from a template marketplace API."""

    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def pull(self):
        if requests is None:
            raise RuntimeError("requests package is required")
        url = f"{self.base_url}/templates"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def parse(self, raw):
        items = []
        for item in raw:
            items.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "price": float(item.get("price", 0)),
                "rating": float(item.get("rating", 0)),
            })
        return items
