"""Lightweight DuckDB table appender."""
from __future__ import annotations

import pathlib
import logging
from typing import Optional

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

try:
    import great_expectations as ge
except Exception:  # pragma: no cover - optional
    ge = None

EXPECT_PATH = pathlib.Path("data") / "expectations"

def _validate(table: str, df: 'pd.DataFrame') -> bool:
    """Validate dataframe against expectation suite if available."""
    if ge is None:
        return True
    suite_path = EXPECT_PATH / f"{table}.json"
    if not suite_path.exists():
        return True
    try:
        context = ge.get_context(context_root_dir=str(EXPECT_PATH.parent))
        suite = context.get_expectation_suite(str(suite_path))
        batch = ge.dataset.PandasDataset(df)
        res = batch.validate(expectation_suite=suite)
        return res.success
    except Exception as exc:  # pragma: no cover - ge issues
        logging.error("validation error for %s: %s", table, exc)
        return False


def append(table: str, df: 'pd.DataFrame') -> None:
    """Append dataframe to a DuckDB table if possible."""
    if duckdb is None or pd is None or DB is None:
        return
    if not _validate(table, df):
        logging.critical("validation failed for %s", table)
        return
    DB.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM df")
    DB.append(table, df)
