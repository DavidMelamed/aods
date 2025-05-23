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
