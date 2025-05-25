from aods.models import ConversionModel, ProfitModel


def test_conversion_predict():
    model = ConversionModel()
    model.fit([[1, 1]], [0])
    preds = model.predict([[1, 1]])
    assert isinstance(preds[0], float)


def test_profit_predict():
    model = ProfitModel()
    model.fit([[1, 1]], [1.0])
    preds = model.predict([[1, 1]])
    assert isinstance(preds[0], float)
