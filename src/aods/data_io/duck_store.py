"""Lightweight DuckDB table appender."""
from __future__ import annotations

import pathlib
from typing import Optional

from .validation import validate

try:
    import duckdb
    import pandas as pd
except Exception:  # pragma: no cover - optional deps
    duckdb = None
    pd = None

DB_PATH = pathlib.Path("data") / "aods.duckdb"

if duckdb is not None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DB = duckdb.connect(str(DB_PATH))
else:  # pragma: no cover - offline mode
    DB = None

def append(table: str, df: 'pd.DataFrame') -> None:
    """Validate and append dataframe to DuckDB."""
    if duckdb is None or pd is None or DB is None:
        return
    if not validate(table, df):
        raise ValueError(f"validation failed for {table}")
    DB.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df")
    DB.append(table, df)
