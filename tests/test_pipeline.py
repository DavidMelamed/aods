from aods.pipeline import Pipeline


def test_pipeline_runs():
    pipe = Pipeline()
    opps = pipe.run()
    assert isinstance(opps, list)
