
"""End-to-end pipeline orchestrating ingestion, modelling and optimisation."""

from typing import List, Optional
import logging
import json
from pathlib import Path
try:
    import joblib
except Exception:  # pragma: no cover - optional
    joblib = None
try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover - optional
    pd = None
try:
    from prometheus_client import Counter, Histogram, start_http_server
except Exception:  # pragma: no cover - optional
    Counter = Histogram = start_http_server = None
from .ingestion import (
    KeywordAPIConnector,
    AdAuctionConnector,
    ProductPriceConnector,
    SocialTrendConnector,
    SaaSPricingConnector,
    MarketNewsConnector,
    ResearchPaperConnector,
)
from .analytics.hypothesis import generate_hypotheses
from .analytics.anomaly import detect_anomalies
from .analytics.cleaning import deduplicate_records
from .utils.cleaning import deduplicate, fill_missing
from .models import ConversionModel, ProfitModel, RankModel
from .analytics.roi import compute_scores
from .agents import IdeaAgent
from .optimizer.portfolio import optimise_portfolio
from .feature_store import build_feature_table


logging.basicConfig(level=logging.INFO)


if start_http_server:
    start_http_server(9102)
    RUN_COUNTER = Counter('aods_runs', 'Pipeline runs', ['status'])
    LATENCY = Histogram('aods_run_seconds', 'Runtime')
else:  # pragma: no cover - metrics disabled
    RUN_COUNTER = type('Dummy', (), {'labels': lambda *args, **kw: type('D', (), {'inc': lambda *a, **k: None})()})
    LATENCY = type('Dummy', (), {'time': lambda self: type('N', (), {'__enter__': lambda *a: None, '__exit__': lambda *a: None})()})()


OPPS_PATH = Path("data/opportunities.json")


class Pipeline:
    def __init__(self, budget: float = 100.0, idea_agent: Optional[IdeaAgent] = None, model_dir: Path | None = None):
        self.connectors = [
            KeywordAPIConnector(),
            AdAuctionConnector(),
            ProductPriceConnector(),
            SocialTrendConnector(),
            SaaSPricingConnector(),
            MarketNewsConnector(),
            ResearchPaperConnector(),
        ]
        self.model_dir = Path("models") if model_dir is None else model_dir
        self.model = self._load_or_default(ConversionModel, "conversion_model.pkl")
        self.profit_model = self._load_or_default(ProfitModel, "profit_model.pkl")
        self.rank_model = self._load_or_default(RankModel, "rank_model.pkl")
        self.budget = budget
        self.idea_agent = idea_agent

    def _load_or_default(self, cls, filename):
        path = self.model_dir / filename
        if joblib is not None and path.exists():
            try:
                return joblib.load(path)
            except Exception as exc:  # pragma: no cover - load issues
                logging.error("failed to load %s: %s", path, exc)
        return cls()

    def run(self) -> List[dict]:

        with LATENCY.time():
            try:
                records: List[dict] = []
                for c in self.connectors:
                    raw = c.pull()
                    parsed = c.parse(raw)
                    c.upsert(parsed)
                    records.extend(parsed)
                records = deduplicate_records(records)
                logging.info("pulled %d records", len(records))

                records = deduplicate(records)
                records = fill_missing(records, {"cpc": 1.0, "search_volume": 1000})

                hyps = generate_hypotheses(records)
                logging.info("generated %d hypotheses", len(hyps))

                if self.idea_agent is not None:
                    try:
                        extra = self.idea_agent.generate_ideas(
                            "Suggest new digital arbitrage opportunities as JSON list"
                        )
                        logging.info("LLM ideas: %s", extra)
                    except Exception as exc:  # pragma: no cover - runtime safety
                        logging.warning("idea generation failed: %s", exc)

                metrics = [r.get("cpc", 1.0) for r in records]
                detect_anomalies(metrics)  # side effect only

                try:
                    feature_df = build_feature_table()
                except Exception as exc:  # pragma: no cover - join issues
                    logging.error("feature build failed: %s", exc)
                    feature_df = pd.DataFrame() if pd is not None else []

                if pd is not None and not feature_df.empty:
                    X = feature_df[["search_volume", "avg_cpc"]].values.tolist()
                else:
                    X = [[r.get("search_volume", 1000), r.get("cpc", 1.0)] for r in records]
                preds = self.model.predict(X)
                if pd is not None and not feature_df.empty:
                    profit_features = feature_df[["price", "avg_cpc"]].fillna(1.0).values.tolist() if "price" in feature_df.columns else [[1.0, c] for c in feature_df["avg_cpc"].tolist()]
                else:
                    profit_features = [[r.get("price", 1.0), r.get("cpc", 1.0)] for r in records]
                profit_preds = self.profit_model.predict(profit_features)

                revenues = [p * 10 + prof for p, prof in zip(preds, profit_preds)]
                costs = [r.get("cpc", 1.0) for r in records]
                std_devs = [0.1 for _ in preds]
                scores = compute_scores(preds, revenues, costs, std_devs)

                selected_idx = optimise_portfolio(scores, costs, self.budget)
                opps = [records[i] for i in selected_idx]
                for i, op in zip(selected_idx, opps):
                    op["score"] = scores[i]

                OPPS_PATH.parent.mkdir(parents=True, exist_ok=True)
                with OPPS_PATH.open("w", encoding="utf-8") as fh:
                    json.dump(opps, fh)

                executed = []
                try:
                    from .execution.router import execute
                    executed = [execute(o) for o in opps]
                except Exception as exc:  # pragma: no cover - execution errors
                    logging.error("execution failed: %s", exc)

                RUN_COUNTER.labels('success').inc()
                return executed or opps
            except Exception:
                RUN_COUNTER.labels('failure').inc()
                logging.exception("pipeline failed")
                return []



def main():
    pipe = Pipeline()
    opps = pipe.run()
    for o in opps:
        print(o)


if __name__ == "__main__":
    main()

