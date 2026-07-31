from sqlalchemy import create_engine, Integer, MetaData, String, Column, VARCHAR, DATE, DateTime, Table, ForeignKey
import pandas as pd 
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

df = pd.read_csv(DATA_DIR / "Cleaned_Data.csv")
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

engine = create_engine("postgresql://postgres:postgres@localhost:5432/ticketsense")
meta = MetaData()

# creating the customers table 
customers_table = Table(
    "customers", 
    meta,
    Column("customer_id", Integer, primary_key=True, autoincrement=True),
    Column("customer_name", VARCHAR(100), nullable=False),
    Column("customer_email", VARCHAR(100), nullable=False),
    Column("customer_age", Integer, nullable=False),
    Column("customer_gender", VARCHAR(20), nullable=False)
)

# creating the tickets table 
tickets_table = Table(
    "tickets", 
    meta,
    Column("owner", Integer, ForeignKey("customers.customer_id")),
    Column("ticket_id", Integer, nullable=False, primary_key=True),
    Column("ticket_type", VARCHAR(100), nullable=False),
    Column("ticket_subject", VARCHAR(200), nullable=False),
    Column("ticket_description", String, nullable=False),
    Column("ticket_status", VARCHAR(50), nullable=False),
    Column("resolution", String, nullable=True),                
    Column("ticket_priority", VARCHAR(50), nullable=True),
    Column("ticket_channel", VARCHAR(50), nullable=True),
    Column("product_purchased", VARCHAR(100), nullable=False),
    Column("date_of_purchase", DATE, nullable=False),
    Column("first_response_time", DateTime, nullable=True),
    Column("time_to_resolution", DateTime, nullable=True),
    Column("customer_satisfaction_rating", Integer, nullable=True)
)

# reset the engine
tickets_table.drop(engine, checkfirst=True)
customers_table.drop(engine, checkfirst=True)
meta.create_all(engine)

# Extract and insert unique customers
unique_customers = df[["customer_name", "customer_email", "customer_age", "customer_gender"]].drop_duplicates(subset=["customer_email"]).copy()
unique_customers.to_sql("customers", engine, if_exists="append", index=False)
print("Customers table inserted!")

# Fetch generated customer IDs from lowercase table
db_customers = pd.read_sql("SELECT customer_id, customer_email FROM customers", engine)

# Merge back onto dataframe and rename customer_id -> owner
tickets_df = df.merge(db_customers, on="customer_email", how="left")
tickets_df = tickets_df.rename(columns={"customer_id": "owner"})

tickets_to_insert = tickets_df[[
    "ticket_id", "owner", "product_purchased", "date_of_purchase",
    "ticket_type", "ticket_subject", "ticket_description", "ticket_status",
    "resolution", "ticket_priority", "ticket_channel", "first_response_time",
    "time_to_resolution", "customer_satisfaction_rating"
]]

tickets_to_insert.to_sql("tickets", engine, if_exists="append", index=False)
print("Tickets table inserted!")

print("Data uploaded successfully!")