"""Feature builder using DuckDB."""
from __future__ import annotations

import duckdb
import pandas as pd
import numpy as np
from pathlib import Path

from ..data_io.duck_store import DB_PATH

FEATURE_PATH = Path('features') / 'keyword_features.parquet'

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

def build() -> None:
    con = duckdb.connect(str(DB_PATH))
    con.execute(SQL)
    df = con.execute('SELECT * FROM keyword_features').df()
    df['ratio_engagement_cpc'] = df['engagement_rate'] / (df['avg_cpc'] + 1e-6)
    df['log_search_volume'] = np.log(df['search_volume'] + 1)
    FEATURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(FEATURE_PATH)

if __name__ == '__main__':
    build()
