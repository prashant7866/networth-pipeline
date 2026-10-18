import duckdb

con = duckdb.connect("data/warehouse.duckdb", read_only=True)

checks = {
    "amount is a positive number":
        "select * from silver.transactions where amount is null or amount <= 0",
    "txn_type is BUY or SELL":
        "select * from silver.transactions where txn_type is null or txn_type not in ('BUY', 'SELL')",
    "date is valid and not in the future":
        "select * from silver.transactions where txn_date is null or txn_date > current_date",
}

failed = False
for name, sql in checks.items():
    bad_rows = con.execute(sql).fetchall()
    if bad_rows:
        failed = True
        print(f"FAIL  {name}: {len(bad_rows)} bad rows")
        print(bad_rows)
    else:
        print(f"PASS  {name}")

con.close()

if failed:
    raise SystemExit(1)