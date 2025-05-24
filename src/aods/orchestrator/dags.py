
"""Airflow DAG for AODS pipeline."""

from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except Exception:  # pragma: no cover - optional
    DAG = None

from aods.ingestion.keyword_api import KeywordAPIConnector
from aods.analytics.hypothesis import generate_hypotheses


def run_pipeline():
    connector = KeywordAPIConnector()
    raw = connector.pull()
    parsed = connector.parse(raw)
    hyps = generate_hypotheses(parsed)
    return hyps


from aods.pipeline import Pipeline

def run_pipeline():
    pipe = Pipeline()
    pipe.run()


if DAG:
    with DAG(
        dag_id="aods_pipeline",
        schedule_interval="@daily",
        start_date=datetime(2024, 1, 1),
        catchup=False,
    ) as dag:

        task = PythonOperator(task_id="run", python_callable=run_pipeline)
        task

