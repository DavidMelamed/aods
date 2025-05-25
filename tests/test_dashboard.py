import json
import os

import pytest

api = pytest.importorskip("fastapi")
from aods.dashboard import api as dashboard
from fastapi.testclient import TestClient


def test_opportunities_endpoint(tmp_path, monkeypatch):
    data = [{"keyword": "k", "score": 1.0}]
    path = tmp_path / "ops.json"
    path.write_text(json.dumps(data))
    monkeypatch.setattr(dashboard, "OPPS_PATH", path)
    client = TestClient(dashboard.app)
    resp = client.get("/opportunities", headers={"X-API-Key": "testkey"})
    assert resp.status_code == 200
    assert resp.json() == data

