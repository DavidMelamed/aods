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
