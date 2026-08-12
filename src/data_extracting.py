from sqlalchemy import select
import pandas as pd

from db.connection import get_engine
from models.schema import Customers, Tickets
from pipelines.init_db import init_database

engine = get_engine()
init_database()

def data_extraction():
    stmt = select(Customers, Tickets).join(Tickets, Customers.customer_id == Tickets.owner)
    df = pd.read_sql(stmt, engine)

    return df