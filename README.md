# Autonomous Opportunity Discovery System (AODS)

This repository provides a lightweight reference implementation matching the high-level PRD found in `prd.md`.

## Components

- **Ingestion**: Example connectors for keyword and product price data.
- **Analytics**: Simple anomaly detection and hypothesis generation utilities.
- **Models**: LightGBM-based conversion rate model with a logistic-regression fallback when LightGBM isn't available.
- **Portfolio Optimizer**: MILP optimisation using OR-Tools with a dynamic programming fallback.
- **Dashboard**: FastAPI app exposing an endpoint that runs the pipeline and returns ranked opportunities.
- **Orchestrator**: Airflow DAG skeleton calling the pipeline.

### Running the pipeline

Execute the pipeline directly using Python:

```bash
python -m aods.pipeline
```

## Development

Install dependencies (optional extras used if available):

```bash
pip install -r requirements.txt
```

Run tests with `pytest`:

```bash
pytest
```
