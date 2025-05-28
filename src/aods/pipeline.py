
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
    def __init__(self, budget: float = 100.0, idea_agent: Optional[IdeaAgent] = None, model_dir: Path | None = None, auto_threshold: float = 1.0):
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
        self.auto_threshold = auto_threshold

    def _load_or_default(self, cls, filename):
        path = self.model_dir / filename
        if joblib is not None and path.exists():
            try:
                return joblib.load(path)
            except Exception as exc:  # pragma: no cover - load issues
                logging.error("failed to load %s: %s", path, exc)
        return cls()

    def ingest(self) -> List[dict]:
        """Fetch raw records from all connectors."""
        records: List[dict] = []
        for c in self.connectors:
            try:
                raw = c.pull()
                parsed = c.parse(raw)
                c.upsert(parsed)
                records.extend(parsed)
            except Exception as exc:  # pragma: no cover - connector failures
                logging.error("connector %s failed: %s", c.__class__.__name__, exc)
        return deduplicate_records(records)

    def preprocess(self, records: List[dict]) -> List[dict]:
        records = deduplicate(records)
        return fill_missing(records, {"cpc": 1.0, "search_volume": 1000})

    def score_records(self, records: List[dict]) -> list[float]:
        if pd is not None:
            try:
                feature_df = build_feature_table()
            except Exception as exc:  # pragma: no cover - join issues
                logging.error("feature build failed: %s", exc)
                feature_df = pd.DataFrame()
            if not feature_df.empty:
                X = feature_df[["search_volume", "avg_cpc"]].values.tolist()
                profit_features = (
                    feature_df[["price", "avg_cpc"]].fillna(1.0).values.tolist()
                    if "price" in feature_df.columns
                    else [[1.0, c] for c in feature_df["avg_cpc"].tolist()]
                )
            else:
                X = [[r.get("search_volume", 1000), r.get("cpc", 1.0)] for r in records]
                profit_features = [[r.get("price", 1.0), r.get("cpc", 1.0)] for r in records]
        else:
            X = [[r.get("search_volume", 1000), r.get("cpc", 1.0)] for r in records]
            profit_features = [[r.get("price", 1.0), r.get("cpc", 1.0)] for r in records]

        preds = self.model.predict(X)
        profit_preds = self.profit_model.predict(profit_features)

        revenues = [p * 10 + prof for p, prof in zip(preds, profit_preds)]
        costs = [r.get("cpc", 1.0) for r in records]
        std_devs = [0.1 for _ in preds]
        scores = compute_scores(preds, revenues, costs, std_devs)
        for rec, sc in zip(records, scores):
            rec["score"] = sc
            rec["auto_exec"] = sc >= self.auto_threshold
        return scores

    def run(self) -> List[dict]:
        with LATENCY.time():
            try:
                records = self.ingest()
                logging.info("pulled %d records", len(records))

                records = self.preprocess(records)

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

                scores = self.score_records(records)

                costs = [r.get("cpc", 1.0) for r in records]
                selected_idx = optimise_portfolio(scores, costs, self.budget)
                opps = [records[i] for i in selected_idx]

                OPPS_PATH.parent.mkdir(parents=True, exist_ok=True)
                with OPPS_PATH.open("w", encoding="utf-8") as fh:
                    json.dump(opps, fh)

                executed = []
                try:
                    from .execution.router import execute
                    executed = [execute(o) for o in opps if o.get("auto_exec")]
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

