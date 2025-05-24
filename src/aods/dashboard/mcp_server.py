"""Simple websocket server exposing MCP interface."""

import asyncio
from fastapi import FastAPI
from fastapi.websockets import WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

from .api import get_top_opportunities

app = FastAPI()

@app.websocket("/mcp")
async def mcp(ws: WebSocket):
    await ws.accept()
    await ws.send_json(get_top_opportunities())
    await ws.close()

HTML = """
<!DOCTYPE html>
<html><body><script>
var ws = new WebSocket('ws://' + location.host + '/mcp');
ws.onmessage = (ev) => { console.log(ev.data); };
</script></body></html>
"""

@app.get("/")
async def root():
    return HTMLResponse(HTML)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
