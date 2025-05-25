"""Apify connector for custom scraping actors."""

from __future__ import annotations

import os
import logging
from typing import Iterable

from .base import DataConnector

try:
    from apify_client import ApifyClient
except Exception:  # pragma: no cover - optional
    ApifyClient = None
    logging.warning("apify-client not available; ApifyConnector inactive")


class ApifyConnector(DataConnector):
    """Connector for Apify scraping tasks."""

    def __init__(self, token: str | None = None, actor: str | None = None):
        self.token = token or os.getenv("APIFY_TOKEN")
        self.actor = actor or os.getenv("APIFY_ACTOR")
        self.client = ApifyClient(self.token) if ApifyClient and self.token else None

    def pull(self) -> Iterable:
        if self.client is None or not self.actor:
            return []
        try:
            run = self.client.actor(self.actor).call()
            return run.get("items", [])
        except Exception as exc:  # pragma: no cover - network errors
            logging.error("Apify fetch failed: %s", exc)
            return []

    def parse(self, raw: Iterable) -> list[dict]:
        return [dict(r) for r in raw]
