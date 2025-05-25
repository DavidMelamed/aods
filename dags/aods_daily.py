from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

with DAG(
    "aods_daily",
    start_date=days_ago(1),
    schedule_interval="0 5 * * *",
    catchup=False,
) as dag:
    ingest = BashOperator(task_id="ingest", bash_command="python -m aods.pipeline ingest")
    train = BashOperator(task_id="train_models", bash_command="python train_models.py")
    score = BashOperator(task_id="score", bash_command="python -m aods.pipeline score")
    optimize = BashOperator(task_id="optimize", bash_command="python -m aods.pipeline optimize")
    archive = BashOperator(task_id="archive_raw", bash_command="python scripts/archive_snapshot.py")

    ingest >> train >> score >> optimize >> archive
