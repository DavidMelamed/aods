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

