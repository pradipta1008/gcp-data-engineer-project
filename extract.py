import requests
from google.cloud import storage

# -----------------------------
# Configuration
# -----------------------------
BUCKET_NAME = "customer-etl-bucket"
API_URL = "https://jsonplaceholder.typicode.com/users"
DESTINATION_BLOB = "raw/users.json"


def extract_api():
    """
    Extract data from REST API
    and upload raw JSON to Google Cloud Storage.
    """

    # Create Storage Client
    storage_client = storage.Client()

    # Get Bucket
    bucket = storage_client.bucket(BUCKET_NAME)

    # Call REST API
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    # Create Blob
    blob = bucket.blob(DESTINATION_BLOB)

    # Upload JSON to GCS
    blob.upload_from_string(
        response.text,
        content_type="application/json"
    )

    print(f"Successfully uploaded data to gs://{BUCKET_NAME}/{DESTINATION_BLOB}")