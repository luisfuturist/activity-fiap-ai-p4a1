from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base  # Assuming models.py is in the same directory

DATABASE_URL = "postgresql://fiap_p4a1:fiap_p4a1@localhost:5432/fiap_p4a1"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine) #Create tables if they don't exist.  Only run this once!

# Function to get a database session.  Consider using a context manager for better resource management.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()