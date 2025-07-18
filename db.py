from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://usuario:senha@localhost:5432/nome_do_banco"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
       yield db
    finally:
        db.close() 

def create_table():
    Base.metadata.create_all(bind=engine)
