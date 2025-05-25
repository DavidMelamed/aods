"""Great Expectations validation helper."""
from __future__ import annotations

from pathlib import Path
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
    suite = ge.core.ExpectationSuite(expectation_suite_name=table)
    # simple expectation example
    if "cpc" in df.columns:
        suite.add_expectation(
            expectation_type="expect_column_values_to_be_between",
            kwargs={"column": "cpc", "min_value": 0, "max_value": 1000},
        )
    result = ge_df.validate(expectation_suite=suite)
    return result.success
