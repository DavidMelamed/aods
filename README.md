# Autonomous Opportunity Discovery System (AODS)

This repository provides a minimal reference implementation matching the high-level PRD found in `prd.md`.

## Components

- **Ingestion**: Example `KeywordAPIConnector` that simulates pulling keyword data.
- **Analytics**: Simple anomaly detection and hypothesis generation utilities.
- **Models**: LightGBM-based conversion rate model (falls back to dummy if LightGBM is missing).
- **Portfolio Optimizer**: MILP optimisation using OR-Tools with a greedy fallback.
- **Dashboard**: Small FastAPI app exposing an endpoint for ranked opportunities.
- **Orchestrator**: Airflow DAG skeleton calling the pipeline.
- **Pipeline Runner**: Command line utility in `aods.pipeline` that executes the full pipeline.

## Development

Install dependencies (optional extras used if available):

```bash
pip install -r requirements.txt
```

Run tests with `pytest`:

```bash
pytest
```

Run the demo pipeline:

```bash
PYTHONPATH=src python -m aods.pipeline
```
