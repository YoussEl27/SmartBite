from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "db")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")


encoded_password = quote_plus(POSTGRES_PASSWORD)


DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{encoded_password}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()