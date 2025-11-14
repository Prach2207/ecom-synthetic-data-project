import sqlite3
import pandas as pd
import os

DB_NAME = "ecommerce.db"
DATA_FOLDER = "data"

def load_csv_to_sqlite(csv_file, table_name, conn):
    df = pd.read_csv(os.path.join(DATA_FOLDER, csv_file))
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {csv_file} → table {table_name}")

def main():
    conn = sqlite3.connect(DB_NAME)

    # Map CSV files to table names
    files = {
        "customers.csv": "customers",
        "products.csv": "products",
        "orders.csv": "orders",
        "order_items.csv": "order_items",
        "reviews.csv": "reviews"
    }

    for csv, table in files.items():
        load_csv_to_sqlite(csv, table, conn)

    conn.close()
    print("\n✅ All CSVs loaded into ecommerce.db successfully!")

if __name__ == "__main__":
    main()
