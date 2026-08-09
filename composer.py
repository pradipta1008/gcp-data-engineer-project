from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocSubmitJobOperator,
    DataprocDeleteClusterOperator,
)
from datetime import datetime

from scripts.extract import extract_api
from scripts.load import load_bigquery

PROJECT_ID = "dauntless-loop-499615-j7"
REGION = "us-central1"
CLUSTER_NAME = "customer-etl-cluster"

PYSPARK_URI = "gs://us-central1-composer-demo-ca6a87ef-bucket/dags/scripts/pyspark_job.py"

default_args = {
    "owner": "airflow"
}

CLUSTER_CONFIG = {
    "gce_cluster_config": {
        "zone_uri": "us-central1-a"
    },
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "e2-standard-2",
        "disk_config": {
            "boot_disk_type": "pd-standard",
            "boot_disk_size_gb": 30,
        },
    },
    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "e2-standard-2",
        "disk_config": {
            "boot_disk_type": "pd-standard",
            "boot_disk_size_gb": 30,
        },
    },
}

PYSPARK_JOB = {
    "reference": {
        "project_id": PROJECT_ID
    },
    "placement": {
        "cluster_name": CLUSTER_NAME
    },
    "pyspark_job": {
        "main_python_file_uri": PYSPARK_URI
    }
}

with DAG(
    dag_id="customer_etl",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
) as dag:

    extract = PythonOperator(
        task_id="extract_api",
        python_callable=extract_api,
    )

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
        cluster_config=CLUSTER_CONFIG,
    )

    run_pyspark = DataprocSubmitJobOperator(
        task_id="run_pyspark_job",
        project_id=PROJECT_ID,
        region=REGION,
        job=PYSPARK_JOB,
    )

    load = PythonOperator(
        task_id="load_bigquery",
        python_callable=load_bigquery,
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
        trigger_rule="all_done",
    )

    extract >> create_cluster >> run_pyspark >> load >> delete_cluster