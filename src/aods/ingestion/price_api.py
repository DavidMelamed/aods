"""Generic price API connector."""

from __future__ import annotations

import os
import logging
from typing import Iterable

from .base import DataConnector

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None
    logging.warning("requests not available; PriceAPIConnector disabled")

class PriceAPIConnector(DataConnector):
    """Connector for external pricing APIs."""

    def __init__(self, url: str | None = None, token: str | None = None):
        self.url = url or os.getenv("PRICE_API_URL")
        self.token = token or os.getenv("PRICE_API_TOKEN")

    def pull(self) -> Iterable:
        if requests is None or not self.url:
            logging.error("Price API not configured")
            return []
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            resp = requests.get(self.url, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("Price API fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]

