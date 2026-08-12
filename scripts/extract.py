import json
import logging

import requests
from google.cloud import storage


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BUCKET_NAME = "customer-etl-bucket"
API_URL = "https://jsonplaceholder.typicode.com/users"
DESTINATION_BLOB = "raw/users.json"


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logger = logging.getLogger(__name__)


# --------------------------------------------------
# EXTRACT API → GCS
# --------------------------------------------------

def extract_api():
    """
    Extract data from REST API
    and upload raw JSON to Google Cloud Storage.
    """

    # Create GCS client
    storage_client = storage.Client()

    # Get existing bucket
    bucket = storage_client.bucket(BUCKET_NAME)

    # Call REST API
    response = requests.get(
        API_URL,
        timeout=30,
    )

    # Raise exception for HTTP errors
    response.raise_for_status()

    # Convert response to JSON
    data = response.json()

    # Convert JSON to string
    json_data = json.dumps(data)

    # Create GCS blob
    blob = bucket.blob(DESTINATION_BLOB)

    # Upload JSON to GCS
    blob.upload_from_string(
        json_data,
        content_type="application/json",
    )

    logger.info(
        "Successfully uploaded data to gs://%s/%s",
        BUCKET_NAME,
        DESTINATION_BLOB,
    )