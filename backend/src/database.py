from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os

db_name = os.environ["POSTGRES_DB"]
db_host = os.environ["POSTGRES_HOST"]
db_user = os.environ["POSTGRES_USER"]
db_password = os.environ["POSTGRES_PASSWORD"]

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
