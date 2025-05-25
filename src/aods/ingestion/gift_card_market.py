"""Connector for gift card market prices."""

from __future__ import annotations

import os
import logging
from typing import Iterable

from .base import DataConnector

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None
    logging.warning("requests not available; GiftCardMarketConnector disabled")

class GiftCardMarketConnector(DataConnector):
    def __init__(self, url: str | None = None):
        self.url = url or os.getenv("GIFT_CARD_API_URL")

    def pull(self) -> Iterable:
        if requests is None or not self.url:
            logging.error("Gift card market API not configured")
            return []
        try:
            resp = requests.get(self.url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("Gift card API fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]
