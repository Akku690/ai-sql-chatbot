import os
from dotenv import load_dotenv
from google import genai
import sqlite3
import pandas as pd

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DB_SCHEMA = """
Table: customers(id INTEGER, name TEXT, city TEXT)
Table: orders(id INTEGER, customer_id INTEGER, product TEXT,
    amount REAL, order_date TEXT)
orders.customer_id links to customers.id
"""

def generate_sql(question: str) -> str:
    prompt = f"""You are an expert SQL generator for a SQLite database.
Database schema:
{DB_SCHEMA}

Convert the following question into ONE valid SQLite SELECT query.
Rules:
- Only output the raw SQL query, nothing else (no explanation, no markdown).
- Only generate SELECT statements. Never write INSERT, UPDATE, DELETE or DROP.

Question: {question}
SQL:"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    sql_query = response.text.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    return sql_query


def run_query(sql_query: str) -> pd.DataFrame:
    # Extra safety check: block anything that isn't a SELECT
    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in sql_query.lower() for word in forbidden):
        raise ValueError("Only SELECT queries are allowed.")

    conn = sqlite3.connect("company.db")
    try:
        df = pd.read_sql_query(sql_query, conn)
    finally:
        conn.close()
    return df