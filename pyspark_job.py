from pyspark.sql import SparkSession
from pyspark.sql.functions import upper, col

# -----------------------------
# Configuration
# -----------------------------
PROJECT_ID = "dauntless-loop-499615-j7"

INPUT_PATH = "gs://customer-etl-bucket/raw/users.json"

OUTPUT_PATH = "gs://customer-etl-bucket/processed/users"

# -----------------------------
# Create Spark Session
# -----------------------------
spark = (
    SparkSession.builder
    .appName("Customer_ETL_PySpark")
    .getOrCreate()
)

# -----------------------------
# Read JSON from GCS
# -----------------------------
df = spark.read.option("multiline", "true").json(INPUT_PATH)

# -----------------------------
# Data Transformation
# -----------------------------
df = (
    df
    .dropDuplicates(["id"])
    .filter(col("id").isNotNull())
    .withColumn("name", upper(col("name")))
)

# -----------------------------
# Select Required Columns
# -----------------------------
final_df = df.select(
    "id",
    "name",
    "username",
    "email",
    "phone",
    "website",
    "company",
    "address"
)

# -----------------------------
# Write to GCS as Parquet
# -----------------------------
(
    final_df.write
    .mode("overwrite")
    .parquet(OUTPUT_PATH)
)

print("PySpark transformation completed successfully.")

spark.stop()