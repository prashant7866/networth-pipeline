from pathlib import Path
import duckdb

con = duckdb.connect("data/warehouse.duckdb")
con.execute(Path("sql/silver_transactions.sql").read_text())
print(con.sql("select count(*) as row_count from silver.transactions"))
con.close()