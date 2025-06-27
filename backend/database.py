from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os
# Explicitly load .env from root dir
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

import urllib.parse

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = urllib.parse.quote_plus(os.getenv("POSTGRES_PASSWORD", ""))
POSTGRES_DB = os.getenv("POSTGRES_DB", "VisionX")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


print("✅ POSTGRES_USER =", os.getenv("POSTGRES_USER"))
print("✅ POSTGRES_PASSWORD =", os.getenv("POSTGRES_PASSWORD"))
print("✅ POSTGRES_DB =", os.getenv("POSTGRES_DB"))
print("✅ POSTGRES_HOST =", os.getenv("POSTGRES_HOST"))

# ✅ Now this uses env vars properly
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
print("✅ SQLALCHEMY_DATABASE_URL =", SQLALCHEMY_DATABASE_URL)
print("Connection successful")
print()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
        print("Database connection established")
    finally:
        db.close() 