from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker  

engine = create_engine("postgresql://postgres:postgres@localhost:5432/ticketsense", echo=False)

def get_engine():
    return engine

SessionLocal = sessionmaker(bind=engine)