import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import bigquery

PROJECT_ID = "dauntless-loop-499615-j7"
DATASET = "customer_dataset"
TABLE = "customer"


def run_vertex_ai():

    vertexai.init(
        project=PROJECT_ID,
        location="us-central1"
    )

    model = GenerativeModel("gemini-2.5-pro")

    client = bigquery.Client(
        project=PROJECT_ID
    )

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

    text = ""

    for row in rows:
        text += f"""
Customer ID: {row.id}
Customer Name: {row.name}
Email: {row.email}
Phone: {row.phone}
Website: {row.website}
"""

    response = model.generate_content(
        f"""
Summarize the following customer data
in 5 bullet points.

{text}
"""
    )

    print(response.text)
