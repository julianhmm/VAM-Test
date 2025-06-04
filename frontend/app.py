import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Vertrags Asset Manager")

menu = ["Contracts", "Assets"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Contracts":
    st.header("Contracts")
    if st.button("Load Contracts"):
        r = requests.get(f"{API_URL}/contracts")
        if r.status_code == 200:
            df = r.json()
            st.write(df)
    with st.form("create_contract"):
        supplier = st.text_input("Supplier")
        description = st.text_input("Description")
        contract_date = st.date_input("Contract Date")
        end_date = st.date_input("End Date")
        auto_extend = st.checkbox("Auto Extend")
        notice_period = st.number_input("Notice Period Days", min_value=0, step=1)
        submitted = st.form_submit_button("Create")
        if submitted:
            payload = {
                "supplier": supplier,
                "description": description,
                "contract_date": str(contract_date),
                "end_date": str(end_date),
                "auto_extend": auto_extend,
                "notice_period_days": int(notice_period),
            }
            resp = requests.post(f"{API_URL}/contracts", json=payload)
            if resp.status_code == 200:
                st.success("Contract created")

if choice == "Assets":
    st.header("Assets")
    if st.button("Load Assets"):
        r = requests.get(f"{API_URL}/assets")
        if r.status_code == 200:
            df = r.json()
            st.write(df)
    with st.form("create_asset"):
        vendor = st.text_input("Vendor")
        purchase_date = st.date_input("Purchase Date")
        eol = st.date_input("EoL")
        info = st.text_input("Info")
        submitted = st.form_submit_button("Create")
        if submitted:
            payload = {
                "vendor": vendor,
                "purchase_date": str(purchase_date),
                "eol": str(eol),
                "info": info,
            }
            resp = requests.post(f"{API_URL}/assets", json=payload)
            if resp.status_code == 200:
                st.success("Asset created")
