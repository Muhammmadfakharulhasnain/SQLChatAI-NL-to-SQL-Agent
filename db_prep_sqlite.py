# db_prep_sqlite.py
"""
Create a SQLite database file from CSV files.
Drop CSVs into `data/` folder and run:
    python db_prep_sqlite.py
This will create `mydata.db`.
"""

import sqlite3
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
OUT_DB = "mydata.db"

def csvs_to_sqlite(data_dir=DATA_DIR, out_db=OUT_DB):
    conn = sqlite3.connect(out_db)
    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in", data_dir.resolve())
        return
    for csv in csv_files:
        table_name = csv.stem
        print(f"Loading {csv} -> table `{table_name}`")
        df = pd.read_csv(csv)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print("Done. SQLite DB created at", out_db)

if __name__ == "__main__":
    csvs_to_sqlite()