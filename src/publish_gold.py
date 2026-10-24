import os

import duckdb
import gspread
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TABLES = ["invested_total", "invested_by_category"]


def to_cell(value):
    """Convert pandas/numpy values into plain types that Google Sheets accepts."""
    if pd.isna(value):
        return ""
    if hasattr(value, "isoformat"):   # dates and timestamps
        return value.isoformat()[:10]
    if hasattr(value, "item"):        # numpy numbers -> plain Python numbers
        return value.item()
    return value


client = gspread.service_account(filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
spreadsheet = client.open_by_key(os.getenv("OUTPUT_SHEET_ID"))
con = duckdb.connect("data/warehouse.duckdb", read_only=True)

for table in TABLES:
    df = con.execute(f"select * from gold.{table}").df()
    header = list(df.columns)
    rows = [[to_cell(v) for v in row] for row in df.itertuples(index=False)]

    try:
        worksheet = spreadsheet.worksheet(table)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=table, rows=100, cols=max(len(header), 5))

    worksheet.clear()
    worksheet.update(values=[header] + rows, range_name="A1")
    print(f"Published {table}: {len(rows)} rows")

con.close()