# Phase 1 - Data Engineering Backbone


DuckDB and Parquet storage replaced JSONL landing files. Connectors now write
raw records via `duck_store.append()` which also performs Great Expectations
validation when available.

