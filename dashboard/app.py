import duckdb
import streamlit as st

st.set_page_config(page_title="Net worth tracker", layout="wide")
st.title("Net worth tracker")


con = duckdb.connect("data/warehouse.duckdb", read_only=True)
total = con.execute("select * from gold.invested_total").df().iloc[0]
by_category = con.execute("select * from gold.invested_by_category").df()
con.close()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net invested", f"₹{total.net_invested:,.0f}")
c2.metric("Total bought", f"₹{total.total_bought:,.0f}")
c3.metric("Total sold", f"₹{total.total_sold:,.0f}")
c4.metric("Transactions", int(total.txn_count))

st.caption(f"From {total.first_txn_date.date()} to {total.last_txn_date.date()}")

st.subheader("Invested by category")
left, right = st.columns(2)
with left:
    st.bar_chart(by_category.set_index("investment_category")["net_invested"])
with right:
    st.dataframe(by_category, hide_index=True)