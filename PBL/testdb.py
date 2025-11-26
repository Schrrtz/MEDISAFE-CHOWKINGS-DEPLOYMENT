# test_db_connection.py
from pathlib import Path
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

print("📌 Starting test_db_connection.py")

# ----------------------------
# Step 1: Load .env file
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent
print(f"Loading .env from: {BASE_DIR / '.env'}")
load_dotenv(BASE_DIR / '.env')  # make sure .env is in the same folder as this script

# ----------------------------
# Step 2: Read database credentials
# ----------------------------
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_SSLMODE = os.getenv('DB_SSLMODE', 'require')

print("Database credentials loaded:")
print(f"DB_NAME={DB_NAME}, DB_USER={DB_USER}, DB_HOST={DB_HOST}, DB_PORT={DB_PORT}, SSL={DB_SSLMODE}")

# ----------------------------
# Step 3: Connect to database
# ----------------------------
print("Attempting database connection...")
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        sslmode=DB_SSLMODE
    )
    print("✅ Connection successful!")
    conn.close()
except OperationalError as e:
    print("❌ Connection failed!")
    print(e)
except Exception as e:
    print("❌ Unexpected error!")
    print(e)
