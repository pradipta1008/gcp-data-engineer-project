import logging

import vertexai
from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ID = "dauntless-loop-499615-j7"
LOCATION = "us-central1"

DATASET = "customer_dataset"
TABLE = "customer"


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logger = logging.getLogger(__name__)


# --------------------------------------------------
# VERTEX AI
# --------------------------------------------------

def run_vertex_ai():
    """
    Read customer data from BigQuery,
    send it to Gemini, and generate a summary.
    """

    # --------------------------------------------------
    # INITIALIZE VERTEX AI
    # --------------------------------------------------

    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
    )

    # --------------------------------------------------
    # INITIALIZE GEMINI MODEL
    # --------------------------------------------------

    model = GenerativeModel(
        "gemini-2.5-pro"
    )

    # --------------------------------------------------
    # CREATE BIGQUERY CLIENT
    # --------------------------------------------------

    client = bigquery.Client(
        project=PROJECT_ID
    )

    # --------------------------------------------------
    # QUERY CUSTOMER DATA
    # --------------------------------------------------

    query = f"""
        SELECT
            id,
            name,
            email,
            phone,
            website
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        LIMIT 10
    """

    rows = client.query(query).result()

    # --------------------------------------------------
    # PREPARE CUSTOMER DATA
    # --------------------------------------------------

    customer_data = []

    for row in rows:
        customer_data.append(
            f"""
Customer ID: {row.id}
Customer Name: {row.name}
Email: {row.email}
Phone: {row.phone}
Website: {row.website}
"""
        )

    text = "\n".join(customer_data)

    # --------------------------------------------------
    # GENERATE SUMMARY
    # --------------------------------------------------

    prompt = f"""
Summarize the following customer data
in 5 concise bullet points.

{text}
"""

    response = model.generate_content(
        prompt
    )

    # --------------------------------------------------
    # LOG RESULT
    # --------------------------------------------------

    logger.info(
        "Vertex AI customer summary generated successfully."
    )

    logger.info(
        "Gemini response:\n%s",
        response.text,
    )

    return response.text