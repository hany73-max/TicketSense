from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:postgres@localhost:5432/ticketsense", echo=False)

def get_engine():
    return engine