from .conversion_model import ConversionModel
from .profit_model import ProfitModel

def train(X, y):
    conv = ConversionModel().fit(X, y)
    prof = ProfitModel().fit(X, y)
    return conv, prof

def predict(model, X):
    return model.predict(X)
__all__ = [
    "ConversionModel",
    "ProfitModel",
    "train",
    "predict",
]
