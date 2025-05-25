"""Simple websocket server exposing MCP interface."""

import asyncio

try:
    from fastapi import FastAPI
    from fastapi.websockets import WebSocket
    from fastapi.responses import HTMLResponse
    import uvicorn
except Exception:  # pragma: no cover - optional dependency
    FastAPI = None
    WebSocket = None
    HTMLResponse = None
    uvicorn = None

from .api import fetch_opportunities

app = FastAPI() if FastAPI else None

if app:
    @app.websocket("/mcp")
    async def mcp(ws: WebSocket):
        await ws.accept()
        await ws.send_json(fetch_opportunities())
        await ws.close()

HTML = """
<!DOCTYPE html>
<html><body><script>
var ws = new WebSocket('ws://' + location.host + '/mcp');
ws.onmessage = (ev) => { console.log(ev.data); };
</script></body></html>
"""

if app:
    @app.get("/")
    async def root():
        return HTMLResponse(HTML)

if __name__ == "__main__" and uvicorn is not None and app is not None:
    uvicorn.run(app, host="0.0.0.0", port=8000)
