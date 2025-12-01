# db_prep_mysql.py
"""
Optional: load CSV files in data/ into MySQL.
Requires pymysql and a running MySQL server.
Edit config.py for credentials.
"""

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import config

DATA_DIR = Path("data")

def csvs_to_mysql():
    user = config.MYSQL_USER
    pwd = config.MYSQL_PASSWORD
    host = config.MYSQL_HOST
    port = config.MYSQL_PORT
    dbname = config.MYSQL_DB
    uri = f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{dbname}"
    engine = create_engine(uri)
    csv_files = list(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print("No CSVs found in", DATA_DIR.resolve())
        return
    for csv in csv_files:
        table = csv.stem
        print(f"Uploading {csv} -> {table} (MySQL)")
        df = pd.read_csv(csv)
        df.to_sql(table, con=engine, if_exists="replace", index=False)
    print("Done.")

if __name__ == "__main__":
    csvs_to_mysql()