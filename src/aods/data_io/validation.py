"""Great Expectations validation helper."""
from __future__ import annotations

from pathlib import Path
import json
import logging
from typing import Any

try:
    import great_expectations as ge
except Exception:  # pragma: no cover - optional
    ge = None

EXPECTATIONS_DIR = Path("data/expectations")


def validate(table: str, df: 'Any') -> bool:
    """Validate dataframe using an expectation suite if available."""
    if ge is None:
        return True
    suite_path = EXPECTATIONS_DIR / f"{table}.json"
    if not suite_path.exists():
        return True
    EXPECTATIONS_DIR.mkdir(parents=True, exist_ok=True)
    ge_df = ge.from_pandas(df)
    try:
        with suite_path.open("r", encoding="utf-8") as fh:
            suite_dict = json.load(fh)
        suite = ge.core.ExpectationSuite(**suite_dict)
    except Exception as exc:  # pragma: no cover - suite issues
        logging.error("failed to load expectation suite %s: %s", suite_path, exc)
        return True
    result = ge_df.validate(expectation_suite=suite)
    if not result.success:
        logging.error("validation failed for %s", table)
    return result.success
