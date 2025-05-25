"""FastAPI endpoints for opportunity review."""
from __future__ import annotations

import os
import json
from pathlib import Path
from typing import List

try:
    from fastapi import FastAPI, WebSocket, Depends, HTTPException, Header
    from fastapi.middleware.cors import CORSMiddleware
except Exception:  # pragma: no cover - optional dependency
    FastAPI = None
    WebSocket = None

from ..pipeline import OPPS_PATH
from ..execution.router import execute

if FastAPI:
    app = FastAPI(title="AODS")
    API_KEY = os.getenv("AODS_API_KEY", "testkey")

    def load_opportunities() -> List[dict]:
        if OPPS_PATH.exists():
            with OPPS_PATH.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        return []

    def fetch_opportunities() -> List[dict]:
        return load_opportunities()

    def check_key(api_key: str = Header(..., alias="X-API-Key")) -> str:
        if api_key != API_KEY:
            raise HTTPException(status_code=401, detail="invalid api key")
        return api_key

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/opportunities")
    def opportunities(_: str = Depends(check_key)):
        return load_opportunities()

    @app.post("/opportunities/{idx}/approve")
    def approve(idx: int, _: str = Depends(check_key)):
        ops = load_opportunities()
        if idx < 0 or idx >= len(ops):
            raise HTTPException(status_code=404, detail="not found")
        opp = ops[idx]
        if opp.get("status") != "pending":
            raise HTTPException(status_code=400, detail="already processed")
        result = execute(opp)
        opp.update(result)
        with OPPS_PATH.open("w", encoding="utf-8") as fh:
            json.dump(ops, fh)
        return opp

    @app.websocket("/mcp")
    async def mcp_endpoint(ws: WebSocket):
        await ws.accept()
        await ws.send_json(load_opportunities())
        await ws.close()
else:  # pragma: no cover - fastapi unavailable
    app = None
    def fetch_opportunities() -> List[dict]:
        return []
