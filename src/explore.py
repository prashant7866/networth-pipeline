import duckdb

duckdb.sql("""
    select
        try_cast(replace(investment_amount, ',', '') as double)  as amount,
        upper(trim(txn_type))                                    as txn_type,
        trim(investment_category)                                as investment_category,
        trim(Fund_stock_name)                                    as instrument_name,
        trim(Broker)                                             as broker,
        try_cast(nullif(trim(Price_per_share), '') as double)    as price_per_share,
        strptime(trim("Date"), '%d/%m/%Y')::date                 as txn_date
    from 'data/bronze/transactions.parquet'
""").show()
