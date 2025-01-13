from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DATABASE_URI = os.getenv("DATABASE_URL")

print(f"SECRET_KEY: {DB_HOST}")
print(f"DATABASE_URL: {DATABASE_URI}")
