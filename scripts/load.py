import logging

from google.cloud import bigquery


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ID = "dauntless-loop-499615-j7"
BUCKET_NAME = "customer-etl-bucket"

DATASET_NAME = "customer_dataset"
TABLE_NAME = "customer"

SOURCE_URI = (
    f"gs://{BUCKET_NAME}/processed/users/*.parquet"
)


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logger = logging.getLogger(__name__)


# --------------------------------------------------
# GCS → BIGQUERY
# --------------------------------------------------

def load_bigquery():
    """
    Load transformed Parquet data from
    Google Cloud Storage into BigQuery.
    """

    # Create BigQuery client
    client = bigquery.Client(
        project=PROJECT_ID
    )

    # Destination table
    table_id = (
        f"{PROJECT_ID}."
        f"{DATASET_NAME}."
        f"{TABLE_NAME}"
    )

    # Configure BigQuery load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        autodetect=True,
        create_disposition=(
            bigquery.CreateDisposition.CREATE_IF_NEEDED
        ),
        write_disposition=(
            bigquery.WriteDisposition.WRITE_TRUNCATE
        ),
    )

    # Load Parquet files from GCS
    load_job = client.load_table_from_uri(
        SOURCE_URI,
        table_id,
        job_config=job_config,
    )

    # Wait for job completion
    load_job.result()

    logger.info(
        "Successfully loaded data into %s",
        table_id,
    )