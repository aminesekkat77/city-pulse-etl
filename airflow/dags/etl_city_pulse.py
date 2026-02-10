from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "hbibi",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="etl_city_pulse",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@hourly",
    catchup=False,
    default_args=default_args,
    tags=["city-pulse", "etl"],
) as dag:

    extract_bikes = BashOperator(
        task_id="extract_bikes",
        bash_command="python /opt/airflow/scripts/extract_bikes.py",
    )

    extract_weather = BashOperator(
        task_id="extract_weather",
        bash_command="python /opt/airflow/scripts/extract_weather.py",
    )

    transform_bikes = BashOperator(
        task_id="transform_bikes",
        bash_command="python /opt/airflow/transform/transform_bikes.py",
    )

    transform_weather = BashOperator(
        task_id="transform_weather",
        bash_command="python /opt/airflow/transform/transform_weather.py",
    )

    create_tables = BashOperator(
        task_id="create_tables",
        bash_command="python /opt/airflow/load/create_tables.py",
    )

    load_to_postgres = BashOperator(
        task_id="load_to_postgres",
        bash_command="python /opt/airflow/load/load_to_postgres.py",
    )

    build_gold = BashOperator(
        task_id="build_gold",
        bash_command="python /opt/airflow/load/build_gold.py",
    )

    # Dépendances (pas de list >> list)
    extract_bikes >> transform_bikes
    extract_weather >> transform_weather

    [transform_bikes, transform_weather] >> create_tables >> load_to_postgres >> build_gold
