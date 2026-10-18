import os
import gspread
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

load_dotenv()

sheet_id = os.getenv("SHEET_ID")
tab_name = os.getenv("SHEET_TAB")
key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

client = gspread.service_account(filename=key_path)
worksheet = client.open_by_key(sheet_id).worksheet(tab_name)
values = worksheet.get_all_values()
header = values[0]
data = values[1:]
df = pd.DataFrame(data, columns=header)

# storing data as plain text in bronze table

out_dir = Path("data/bronze")
out_dir.mkdir(parents=True, exist_ok=True)
df.to_parquet(out_dir / "transactions.parquet", index=False)
print(f"Saved Bronze Data to {out_dir / 'transactions.parquet'}")
