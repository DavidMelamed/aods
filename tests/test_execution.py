import os
from aods.execution.router import execute


def test_execute_dry_run(monkeypatch):
    monkeypatch.setenv("EXECUTION_MODE", "DRY")
    result = execute({"type": "keyword", "keyword": "x"})
    assert result["status"] == "dry-run"
