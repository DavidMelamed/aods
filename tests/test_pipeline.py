
import pytest
from aods.pipeline import Pipeline


def test_pipeline_runs():
    pipe = Pipeline()
    opps = pipe.run()
    assert isinstance(opps, list)


def test_model_loading(tmp_path):
    joblib = pytest.importorskip("joblib")
    from aods.models import ConversionModel, ProfitModel, RankModel

    model_dir = tmp_path
    joblib.dump(ConversionModel(), model_dir / "conversion_model.pkl")
    joblib.dump(ProfitModel(), model_dir / "profit_model.pkl")
    joblib.dump(RankModel(), model_dir / "rank_model.pkl")

    pipe = Pipeline(model_dir=model_dir)
    assert pipe.model is not None
