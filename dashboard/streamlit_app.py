import os

import gspread
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Net worth tracker", layout="wide")
st.title("Net worth tracker")


def get_client():
    """Use Streamlit secrets in the cloud, or your .env and key file locally."""
    try:
        creds = dict(st.secrets["gcp_service_account"])
        return gspread.service_account_from_dict(creds), st.secrets["OUTPUT_SHEET_ID"]
    except (KeyError, FileNotFoundError):
        client = gspread.service_account(filename=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
        return client, os.getenv("OUTPUT_SHEET_ID")


@st.cache_data(ttl=600)
def load_tab(name):
    client, sheet_id = get_client()
    rows = client.open_by_key(sheet_id).worksheet(name).get_all_records()
    return pd.DataFrame(rows)


total = load_tab("invested_total").iloc[0]
by_category = load_tab("invested_by_category")
by_category["net_invested"] = pd.to_numeric(by_category["net_invested"])

c1, c2, c3, c4 = st.columns(4)
c1.metric("Net invested", f"₹{float(total.net_invested):,.0f}")
c2.metric("Total bought", f"₹{float(total.total_bought):,.0f}")
c3.metric("Total sold", f"₹{float(total.total_sold):,.0f}")
c4.metric("Transactions", int(total.txn_count))

st.caption(f"From {total.first_txn_date} to {total.last_txn_date}")

st.subheader("Invested by category")
left, right = st.columns(2)
with left:
    st.bar_chart(by_category.set_index("investment_category")["net_invested"])
with right:
    st.dataframe(by_category, hide_index=True)