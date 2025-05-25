"""Feature store utilities."""
from __future__ import annotations
from pathlib import Path
from typing import Optional

try:
    import duckdb  # type: ignore
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - optional
    duckdb = None
    pd = None

from .data_io.duck_store import DB_PATH

FEATURE_TABLE = "feature_store"
FEATURE_PATH = Path("features") / "feature_store.parquet"

SQL = """
SELECT k.keyword,
       k.search_volume,
       a.avg_cpc,
       t.engagement_rate,
       nv.avg_sentiment
FROM keyword_api_raw k
LEFT JOIN ad_auction_raw a USING(keyword)
LEFT JOIN social_trends_raw t USING(keyword)
LEFT JOIN news_sentiment_view nv USING(keyword)
"""


def build_feature_table(
    con: Optional["duckdb.DuckDBPyConnection"] = None,
    persist: bool = True,
) -> "pd.DataFrame":
    """Join raw tables into a unified feature table."""
    if duckdb is None or pd is None:
        raise RuntimeError("duckdb and pandas are required")

    if con is None:
        con = duckdb.connect(str(DB_PATH))

    df = con.execute(SQL).df()
    df.fillna({"avg_cpc": 0.0, "engagement_rate": 0.0, "avg_sentiment": 0.0}, inplace=True)
    df["ratio_engagement_cpc"] = df["engagement_rate"] / (df["avg_cpc"] + 1e-6)

    if persist:
        con.execute(f"CREATE OR REPLACE TABLE {FEATURE_TABLE} AS SELECT * FROM df")
        FEATURE_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(FEATURE_PATH)

    return df

