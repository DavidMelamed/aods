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


Install dependencies using the provided setup script (optional extras will be
installed if network access is available):

```bash
./setup.sh
```

Run tests with `pytest` after installing dependencies:


```bash
pytest
```

### Frontend with CopilotKit

The optional dashboard is built using **Next.js** with the `copilotkit` library.
Install dependencies inside `frontend/` and start the dev server:

```bash
cd frontend
npm install
npm run dev
```

The app will fetch opportunities from the FastAPI backend at `http://localhost:8000/opportunities`.

Run the demo pipeline:

## Extended Features

- Additional connectors for simulated product pricing and social trends
- ROI utilities implementing expected value and risk-adjusted return
- End-to-end pipeline (`python -m aods.pipeline`) running ingestion,
  anomaly detection, model training, ROI scoring and portfolio optimisation
- Basic matplotlib visualisations for opportunity score vs cost

### Running the Pipeline

Execute the pipeline directly:


```bash
PYTHONPATH=src python -m aods.pipeline
```


### Visualising Results

After running the pipeline you can generate a scatter plot of the
selected opportunities:

```python
from aods.visualization.plots import scatter_roi_vs_cost

scores = [op['score'] for op in ops]
costs = [op['cost'] for op in ops]
plt = scatter_roi_vs_cost(scores, costs)
plt.show()
```

