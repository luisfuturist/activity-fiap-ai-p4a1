from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


DATABASE_URL = "postgresql://fiap_p4a1:fiap_p4a1@localhost:5433/fiap_p4a1"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create tables if they don't exist.  Only run this once!  Move this to init_db.py
#Base.metadata.create_all(engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()