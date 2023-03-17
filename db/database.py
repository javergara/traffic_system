from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLite file
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#SQLite engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Class where the database models are inheriting
Base = declarative_base()