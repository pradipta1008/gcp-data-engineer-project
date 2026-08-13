from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocSubmitJobOperator,
    DataprocDeleteClusterOperator,
)

from scripts.extract import extract_api
from scripts.load import load_bigquery
from scripts.vertex_ai import run_vertex_ai


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ID = "dauntless-loop-499615-j7"
REGION = "us-central1"

CLUSTER_NAME = "customer-etl-cluster"

# Composer bucket created by Terraform
PYSPARK_URI = (
    "gs://dauntless-loop-499615-j7-composer/"
    "dags/scripts/pyspark_job.py"
)


# --------------------------------------------------
# DEFAULT ARGUMENTS
# --------------------------------------------------

default_args = {
    "owner": "airflow",
}


# --------------------------------------------------
# DATAPROC CLUSTER CONFIGURATION
# --------------------------------------------------

CLUSTER_CONFIG = {
    "gce_cluster_config": {},

    "master_config": {
        "num_instances": 1,
        "machine_type_uri": "e2-small",
        "disk_config": {
            "boot_disk_type": "pd-standard",
            "boot_disk_size_gb": 30,
        },
    },

    "worker_config": {
        "num_instances": 2,
        "machine_type_uri": "e2-small",
        "disk_config": {
            "boot_disk_type": "pd-standard",
            "boot_disk_size_gb": 30,
        },
    },
}


# --------------------------------------------------
# PYSPARK JOB CONFIGURATION
# --------------------------------------------------

PYSPARK_JOB = {
    "reference": {
        "project_id": PROJECT_ID,
    },

    "placement": {
        "cluster_name": CLUSTER_NAME,
    },

    "pyspark_job": {
        "main_python_file_uri": PYSPARK_URI,
    },
}


# --------------------------------------------------
# DAG
# --------------------------------------------------

with DAG(
    dag_id="customer_etl",
    start_date=datetime(2024, 1, 1),
    schedule="@once",
    catchup=False,
    default_args=default_args,
    tags=["customer", "etl", "gcp"],
) as dag:

    # --------------------------------------------------
    # 1. EXTRACT API → GCS
    # --------------------------------------------------

    extract = PythonOperator(
        task_id="extract_api",
        python_callable=extract_api,
    )

    # --------------------------------------------------
    # 2. CREATE TEMPORARY DATAPROC CLUSTER
    # --------------------------------------------------

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
        cluster_config=CLUSTER_CONFIG,
    )

    # --------------------------------------------------
    # 3. RUN PYSPARK JOB
    # --------------------------------------------------

    run_pyspark = DataprocSubmitJobOperator(
        task_id="run_pyspark_job",
        project_id=PROJECT_ID,
        region=REGION,
        job=PYSPARK_JOB,
    )

    # --------------------------------------------------
    # 4. LOAD → BIGQUERY
    # --------------------------------------------------

    load = PythonOperator(
        task_id="load_bigquery",
        python_callable=load_bigquery,
    )

    # --------------------------------------------------
    # 5. VERTEX AI
    # --------------------------------------------------

    vertex_ai = PythonOperator(
        task_id="vertex_ai",
        python_callable=run_vertex_ai,
    )

    # --------------------------------------------------
    # 6. DELETE TEMPORARY DATAPROC CLUSTER
    # --------------------------------------------------

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id=PROJECT_ID,
        region=REGION,
        cluster_name=CLUSTER_NAME,
        trigger_rule="all_done",
    )

    # --------------------------------------------------
    # PIPELINE ORDER
    # --------------------------------------------------

    (
        extract
        >> create_cluster
        >> run_pyspark
        >> load
        >> vertex_ai
        >> delete_cluster
    )