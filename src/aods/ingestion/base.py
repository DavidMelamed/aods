"""Base interfaces for data connectors."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Iterable, List

from ..data_io import duck_store


class DataConnector:
    """Base class for ingestion connectors."""

    landing_dir = Path("landing_zone")

    def pull(self) -> Iterable:
        """Retrieve raw data from the source."""
        raise NotImplementedError

    def parse(self, raw: Iterable) -> List[dict]:
        """Parse raw payload into structured records."""
        raise NotImplementedError

    def landing_file(self) -> Path:
        """Return the landing-zone file path for this connector."""
        self.landing_dir.mkdir(parents=True, exist_ok=True)
        return self.landing_dir / f"{self.__class__.__name__}.jsonl"

    def upsert(self, records: List[dict]) -> List[dict]:
        """Persist records to DuckDB if available."""
        table = f"{self.__class__.__name__.lower()}_raw"
        try:
            import pandas as pd  # local optional dep
            duck_store.append(table, pd.DataFrame(records))
        except Exception as exc:  # pragma: no cover - optional deps
            logging.error("Failed to append to %s: %s", table, exc)
            path = self.landing_file()
            try:
                with path.open("a", encoding="utf-8") as fh:
                    for rec in records:
                        fh.write(json.dumps(rec) + "\n")
            except Exception as write_exc:  # pragma: no cover - file issues
                logging.error("Fallback write failed: %s", write_exc)
        return records
