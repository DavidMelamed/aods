from aods.models.conversion_model import ConversionModel
from aods.models.profit_model import ProfitModel


def test_model_predict():
    X = [[1, 2], [3, 4]]
    y = [0, 1]
    conv = ConversionModel().fit(X, y)
    pred = conv.predict(X)[0]
    prof = ProfitModel().fit(X, y)
    out = prof.predict(X)[0]
    assert isinstance(pred, float)
    assert isinstance(out, float)
