import pandas as pd
from db.connection import get_engine
from models.schema import Customers, Tickets

def load_data(df: pd.DataFrame):
    engine = get_engine()

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # 1. Append new unique customers
    unique_customers = (
        df[["customer_name", "customer_email", "customer_age", "customer_gender"]]
        .drop_duplicates(subset=["customer_email"])
        .copy()
    )
    
    # if_exists="append" safely adds new records without dropping tables!
    unique_customers.to_sql("customers", engine, if_exists="append", index=False)
    print("Customers inserted!")

    # 2. Resolve Foreign Keys
    db_customers = pd.read_sql("SELECT customer_id, customer_email FROM customers", engine)
    tickets_df = df.merge(db_customers, on="customer_email", how="left")
    tickets_df = tickets_df.rename(columns={"customer_id": "owner"})

    tickets_to_insert = tickets_df[[
        "ticket_id", "owner", "product_purchased", "date_of_purchase",
        "ticket_type", "ticket_subject", "ticket_description", "ticket_status",
        "resolution", "ticket_priority", "ticket_channel", "first_response_time",
        "time_to_resolution", "customer_satisfaction_rating"
    ]]

    # 3. Append tickets
    tickets_to_insert.to_sql("tickets", engine, if_exists="append", index=False)
    print("Tickets inserted!")