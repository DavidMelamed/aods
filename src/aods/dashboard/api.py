"""FastAPI application exposing opportunity endpoints."""

from fastapi import FastAPI
from aods.pipeline import run_pipeline

app = FastAPI(title="AODS")


@app.get("/opportunities")
def opportunities():
    return run_pipeline()
