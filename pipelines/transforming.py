import pandas as pd 

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
csv_path = DATA_DIR/"customer_support_tickets.csv"

# transforming the raw data
def data_transform(csv_path):
    df = pd.read_csv(csv_path)

    df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'), inplace=True)
    df["ticket_description"] = df.apply(
        lambda row: row["ticket_description"].replace("{product_purchased}", str(row["product_purchased"])), 
        axis= 1
        )

    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.encode('ascii', 'ignore').str.decode('ascii')

    print("data transformed successfully!")

    return df