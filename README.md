# Autonomous Opportunity Discovery System (AODS)

This repository provides a minimal reference implementation matching the high-level PRD found in `prd.md`.

## Components

- **Ingestion**: Pluggable connectors for keywords, ad auctions, product prices and social trends.
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

### Environment variables

Set any API tokens required by optional connectors before running the
pipeline. For example, supply your OpenAI key so the ``IdeaAgent`` can
call the API:

```bash
export OPENAI_API_KEY="sk-..."
```

Other connectors use variables such as ``APIFY_TOKEN`` or ``SCRAPEOWL_KEY``.
The pipeline will degrade gracefully if these are unset.

Run tests with `pytest`:

## Usage

Run the pipeline directly:

```bash
PYTHONPATH=src python -m aods.pipeline
```

Train models from existing feature data:

```bash
PYTHONPATH=src python train_models.py
```

Models are saved under `models/` and automatically loaded by the pipeline for scoring.

Start the API (requires `uvicorn`):

```bash
uvicorn aods.dashboard.api:app --reload
```

## Configuration

Set the following environment variables to enable the live connectors:

- `KEYWORD_API_URL` and `KEYWORD_API_TOKEN`
- `AD_AUCTION_API_URL` and `AD_AUCTION_API_TOKEN`
- `PRODUCT_PRICE_API_URL` and `PRODUCT_PRICE_API_TOKEN`
- `SOCIAL_TRENDS_API_URL` and `SOCIAL_TRENDS_API_TOKEN`
- `SAAS_PRICING_API_URL` and `SAAS_PRICING_API_TOKEN`
- `PRICE_API_URL` and `PRICE_API_TOKEN`
- `CRYPTO_EXCHANGE_API_URL`
- `GIFT_CARD_API_URL`
- `APIFY_TOKEN` and `APIFY_ACTOR`
- `SCRAPEOWL_API_KEY`
- `EXA_API_KEY`
- `TAVILY_API_KEY`
- `DATAFORSEO_KEY` and `DATAFORSEO_SECRET`

If any variable is unset, the corresponding connector will simply return no
records. Pulled data is written as JSON lines under `landing_zone/` for
persistence.


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

## Configuration

Several connectors require API keys. Set these via environment variables before
running the pipeline:

```bash
export EXA_API_KEY=<your-exa-key>
export TAVILY_API_KEY=<your-tavily-key>
export APIFY_TOKEN=<your-apify-token>
export ASTRA_TOKEN=<your-astra-token>
export ASTRA_ENDPOINT=<your-astra-endpoint>
```

The `DataForSEO*` connectors accept `API_KEY` and `API_SECRET` arguments or use
`DATAFORSEO_KEY` and `DATAFORSEO_SECRET` environment variables.

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
Start the backend API separately:

```bash
uvicorn aods.dashboard.api:app --reload
```

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

