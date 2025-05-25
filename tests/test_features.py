import pytest
pytest.importorskip("pandas")
import pandas as pd
import duckdb
from aods.features import build_feature_table


def test_build_feature_table():
    con = duckdb.connect(':memory:')
    con.execute('CREATE TABLE keyword_api_raw(keyword TEXT, search_volume INT)')
    con.execute("INSERT INTO keyword_api_raw VALUES ('k', 100)")
    con.execute('CREATE TABLE ad_auction_raw(keyword TEXT, avg_cpc DOUBLE)')
    con.execute("INSERT INTO ad_auction_raw VALUES ('k', 2.0)")
    con.execute('CREATE TABLE social_trends_raw(keyword TEXT, engagement_rate DOUBLE)')
    con.execute("INSERT INTO social_trends_raw VALUES ('k', 5.0)")
    con.execute('CREATE TABLE news_sentiment_view(keyword TEXT, avg_sentiment DOUBLE)')
    con.execute("INSERT INTO news_sentiment_view VALUES ('k', 0.1)")
    df = build_feature_table(con, persist=False)
    assert isinstance(df, pd.DataFrame)
    assert 'ratio_engagement_cpc' in df.columns
    assert df.loc[0, 'keyword'] == 'k'
