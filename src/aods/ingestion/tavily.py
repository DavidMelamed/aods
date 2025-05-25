"""Tavily trend data connector."""

from __future__ import annotations

import os
import logging
from typing import Iterable

from .base import DataConnector

try:
    import tavily
except Exception:  # pragma: no cover - optional
    tavily = None
    logging.warning("tavily library not available; TavilyConnector inactive")


class TavilyConnector(DataConnector):
    """Connector for the Tavily data API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def pull(self) -> Iterable:
        if tavily is None or not self.api_key:
            return []
        try:
            client = tavily.Client(self.api_key)
            return client.get_trending()
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("Tavily API fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]
