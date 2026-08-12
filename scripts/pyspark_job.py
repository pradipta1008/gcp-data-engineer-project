import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_PATH = "gs://customer-etl-bucket/raw/users.json"
OUTPUT_PATH = "gs://customer-etl-bucket/processed/users"


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# SPARK SESSION
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("Customer_ETL_PySpark")
    .getOrCreate()
)


try:

    # --------------------------------------------------
    # READ RAW JSON FROM GCS
    # --------------------------------------------------

    logger.info(
        "Reading raw data from %s",
        INPUT_PATH,
    )

    df = (
        spark.read
        .option("multiline", "true")
        .json(INPUT_PATH)
    )

    # --------------------------------------------------
    # DATA TRANSFORMATION
    # --------------------------------------------------

    df = (
        df
        .dropDuplicates(["id"])
        .filter(col("id").isNotNull())
        .withColumn("name", upper(col("name")))
    )

    # --------------------------------------------------
    # SELECT REQUIRED COLUMNS
    # --------------------------------------------------

    final_df = df.select(
        "id",
        "name",
        "username",
        "email",
        "phone",
        "website",
        "company",
        "address",
    )

    # --------------------------------------------------
    # WRITE PROCESSED DATA AS PARQUET
    # --------------------------------------------------

    logger.info(
        "Writing processed data to %s",
        OUTPUT_PATH,
    )

    (
        final_df.write
        .mode("overwrite")
        .parquet(OUTPUT_PATH)
    )

    logger.info(
        "PySpark transformation completed successfully."
    )

finally:

    # --------------------------------------------------
    # STOP SPARK
    # --------------------------------------------------

    spark.stop()