"""Airflow DAG skeleton for AODS pipeline."""

from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except Exception:  # pragma: no cover - optional
    DAG = None

from aods.pipeline import run_pipeline

if DAG:
    with DAG(
        dag_id="aods_pipeline",
        schedule_interval="@daily",
        start_date=datetime(2024, 1, 1),
        catchup=False,
    ) as dag:
        task = PythonOperator(task_id="run", python_callable=run_pipeline)
        task
