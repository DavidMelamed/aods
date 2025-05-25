import pytest
pytest.importorskip("pandas")
import pandas as pd
from aods.data_io import validation


def test_validate_no_ge(monkeypatch):
    monkeypatch.setattr(validation, 'ge', None)
    df = pd.DataFrame({'cpc': [1.0]})
    assert validation.validate('dummy', df)
