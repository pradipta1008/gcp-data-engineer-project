import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import bigquery

PROJECT_ID = "your-project-id"
DATASET = "customer_dataset"
TABLE = "customer"

vertexai.init(
    project=PROJECT_ID,
    location="us-central1"
)

model = GenerativeModel("gemini-2.5-pro")

client = bigquery.Client(project=PROJECT_ID)

query = f"""
SELECT customer_name,
       city,
       balance
FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
LIMIT 10
"""

rows = client.query(query).result()

text = ""

for row in rows:
    text += f"""
Customer Name: {row.customer_name}
City: {row.city}
Balance: {row.balance}
"""

response = model.generate_content(
    f"""
Summarize the following customer data in 5 bullet points.

{text}
"""
)

print(response.text)