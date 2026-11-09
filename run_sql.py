
from pathlib import Path
import sqlite3
import pandas as pd

# Project folder location
base_folder = Path(__file__).resolve().parent

# Database and SQL file paths
db_path = base_folder / "data" / "instamart_demo.db"
sql_path = base_folder / "sql" / "analysis_queries.sql"

# Connect to database
with sqlite3.connect(db_path) as connection:

    # Read SQL queries
    sql_text = sql_path.read_text(encoding="utf-8")

    # Separate individual queries
    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    # Execute each query and display results
    for number, query in enumerate(queries, start=1):
        print(f"\n--- SQL Query {number} Result ---")

        result = pd.read_sql_query(query, connection)

        print(result.to_string(index=False))

print("\nAll SQL queries completed successfully!")
