# Autonomous Opportunity Discovery System (AODS)

This repository provides a minimal reference implementation matching the high-level PRD found in `prd.md`.

## Components

- **Ingestion**: Example `KeywordAPIConnector` that simulates pulling keyword data.
- **Analytics**: Simple anomaly detection and hypothesis generation utilities.
- **Models**: LightGBM-based conversion rate model (falls back to dummy if LightGBM is missing).
- **Portfolio Optimizer**: MILP optimisation using OR-Tools with a greedy fallback.
- **Dashboard**: Small FastAPI app exposing an endpoint for ranked opportunities.
- **Orchestrator**: Airflow DAG skeleton calling the pipeline.

## Development

Install dependencies (optional extras used if available):

```bash
pip install -r requirements.txt
```

Run tests with `pytest`:

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

## Additional Connectors

The ingestion layer now includes optional connectors for external data services:

- `ExaAIConnector` (exa.ai search)
- `TavilyConnector` (Tavily trends)
- `ApifyConnector` for running Apify actors
- `ScrapeOwlConnector` for simple web scraping

These connectors are loaded only if their respective libraries are installed.

## Vector Storage

Embeddings can be stored in **Astra DB** using the `AstraVectorStore` wrapper. Configure it with your Astra token and API endpoint to enable vector similarity queries.

## MCP Chat Server

A lightweight websocket server (`mcp_server.py`) exposes pipeline results over an experimental MCP-compatible protocol. This allows AI chat tools supporting MCP to request the latest opportunities.

Run the server:

```bash
python -m aods.dashboard.mcp_server
```

## Frontend

The FastAPI dashboard can be served with uvicorn and now supports basic opportunity listing and MCP endpoint.

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

