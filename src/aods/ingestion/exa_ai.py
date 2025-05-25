"""Exa.ai search connector."""

from __future__ import annotations

import os
import logging
from typing import Iterable

from .base import DataConnector

try:
    import exa_py
except Exception:  # pragma: no cover - optional
    exa_py = None
    logging.warning("exa.ai SDK not available; ExaAIConnector is inactive")


class ExaAIConnector(DataConnector):
    """Connector for the Exa.ai search API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("EXA_API_KEY")

    def pull(self) -> Iterable:
        if exa_py is None or not self.api_key:
            return []
        try:
            client = exa_py.Exa(self.api_key)
            return client.search("arbitrage opportunities")
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("Exa API fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]
