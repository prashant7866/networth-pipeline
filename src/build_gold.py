from pathlib import Path
import duckdb

con = duckdb.connect("data/warehouse.duckdb")
con.execute(Path("sql/gold_kpis.sql").read_text())
print(con.sql("select * from gold.invested_total"))
print(con.sql("select * from gold.invested_by_category"))
con.close()