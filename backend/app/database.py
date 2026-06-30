import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load variables from .env into the environment
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The "engine" is the actual connection to PostgreSQL
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating individual DB sessions (conversations)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is what our table classes (models) will inherit from
Base = declarative_base()

# Dependency function — FastAPI will use this to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()