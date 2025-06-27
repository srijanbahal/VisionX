from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    print("✅ SUCCESS: Connected to the database.")
    conn.close()
except Exception as e:
    print("❌ FAILED to connect:")
    print(e)
