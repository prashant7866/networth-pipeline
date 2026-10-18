create schema if not exists gold;

create or replace table gold.invested_total as
select
    sum(case when txn_type = 'BUY' then amount else -amount end) as net_invested,
    sum(case when txn_type = 'BUY' then amount else 0 end)       as total_bought,
    sum(case when txn_type = 'SELL' then amount else 0 end)      as total_sold,
    count(*)                                                     as txn_count,
    min(txn_date)                                                as first_txn_date,
    max(txn_date)                                                as last_txn_date
from silver.transactions;

create or replace table gold.invested_by_category as
select
    investment_category,
    sum(case when txn_type = 'BUY' then amount else -amount end) as net_invested,
    count(*)                                                     as txn_count
from silver.transactions
group by investment_category
order by net_invested desc;