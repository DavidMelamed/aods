"""FastAPI application exposing opportunity endpoints."""

from fastapi import FastAPI

app = FastAPI(title="AODS")


def get_top_opportunities():
    # Placeholder data
    return [
        {"keyword": "ai", "score": 1.0},
        {"keyword": "ml", "score": 0.8},
    ]


@app.get("/opportunities")
def opportunities():
    return get_top_opportunities()

from fastapi import WebSocket

@app.websocket("/mcp")
async def mcp_endpoint(ws: WebSocket):
    await ws.accept()
    ops = get_top_opportunities()
    await ws.send_json(ops)
    await ws.close()
