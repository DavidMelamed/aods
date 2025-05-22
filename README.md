# Autonomous Opportunity Discovery System (AODS)

This repository implements a lightweight reference implementation of the AODS design described in `prd.md`.  It provides sample connectors, analytics utilities, a simple predictive model, portfolio optimiser, API and an orchestration script.

## Components

- **Ingestion**: Multiple simulated connectors (`KeywordAPIConnector`, `AdAuctionConnector`, `ProductPriceConnector`, `SocialTrendConnector`, `SaaSPricingConnector`).
- **Analytics**: Anomaly detection (`pyod` if installed, otherwise z-score fallback), rule based hypothesis generation and ROI utilities.
- **Models**: `ConversionRateModel` using LightGBM when available.
- **Portfolio Optimiser**: MILP via OR-Tools with greedy fallback.
- **Dashboard**: FastAPI application exposing REST and optional GraphQL endpoints.
- **Orchestrator**: Airflow DAG skeleton and a standalone `Pipeline` runner.

## Usage

Run the pipeline directly:

```bash
PYTHONPATH=src python -m aods.pipeline
```

Start the API (requires `uvicorn`):

```bash
uvicorn aods.dashboard.api:app --reload
```

## Development

Install dependencies (optional extras used if available):

```bash
pip install -r requirements.txt
```

Run tests with `pytest`:

```bash
python -m pytest -q
```
