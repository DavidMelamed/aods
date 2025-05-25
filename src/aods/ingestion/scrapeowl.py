"""ScrapeOwl connector."""

from __future__ import annotations

import os
import logging
from typing import Iterable

from .base import DataConnector

try:
    import scrapeowl
except Exception:  # pragma: no cover - optional
    scrapeowl = None
    logging.warning("scrapeowl not available; ScrapeOwlConnector inactive")


class ScrapeOwlConnector(DataConnector):
    """Connector for ScrapeOwl scraping API."""

    def __init__(self, api_key: str | None = None, url: str | None = None):
        self.api_key = api_key or os.getenv("SCRAPEOWL_API_KEY")
        self.url = url or os.getenv("SCRAPEOWL_URL", "https://example.com")

    def pull(self) -> Iterable:
        if scrapeowl is None or not self.api_key:
            return []
        try:
            return scrapeowl.get(self.url, self.api_key)
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("ScrapeOwl fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(raw)] if isinstance(raw, dict) else list(raw)
