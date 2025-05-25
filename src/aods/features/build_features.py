"""Build feature tables using DuckDB joins."""
from __future__ import annotations

from pathlib import Path

try:
    import duckdb
    import pandas as pd
except Exception:  # pragma: no cover - optional deps
    duckdb = None
    pd = None

DB_PATH = Path("data") / "aods.duckdb"
FEATURE_DIR = Path("features")

SQL = """
CREATE OR REPLACE TABLE keyword_features AS
SELECT k.keyword,
       k.search_volume,
       a.avg_cpc,
       t.engagement_rate,
       nv.avg_sentiment
FROM keyword_api_raw k
LEFT JOIN ad_auction_raw a USING(keyword)
LEFT JOIN social_trends_raw t USING(keyword)
LEFT JOIN news_sentiment_view nv USING(keyword);
"""


def build_features() -> Path:
    """Materialise feature table and export to Parquet."""
    if duckdb is None or pd is None:
        raise RuntimeError("duckdb not available")
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))
    con.execute(SQL)
    df = con.execute("SELECT * FROM keyword_features").fetch_df()
    df["ratio_engagement_cpc"] = df["engagement_rate"] / df["avg_cpc"].replace(0, 1)
    df["log_search_volume"] = (df["search_volume"] + 1).apply(lambda x: __import__("math").log(x))
    out_path = FEATURE_DIR / "keyword_features.parquet"
    df.to_parquet(out_path)
    return out_path


if __name__ == "__main__":
    build_features()
