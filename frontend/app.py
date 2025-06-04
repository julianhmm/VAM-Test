import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Vertrags Asset Manager")

st.sidebar.title("Navigation")
menu = ["Dashboard", "\u00dcbersicht", "Vertr\u00e4ge", "Assets"]
choice = st.sidebar.radio("Men\u00fc", menu)

if choice == "Dashboard":
    st.header("Dashboard")
    st.write("Willkommen im Vertrags Asset Manager")

if choice == "\u00dcbersicht":
    st.header("\u00dcbersicht")
    if st.button("Vertr\u00e4ge laden"):
        r = requests.get(f"{API_URL}/contracts")
        if r.status_code == 200:
            contracts = r.json()
            for c in contracts:
                st.subheader(f"Vertrag {c['id']} - {c['supplier']}")
                st.write(f"Beschreibung: {c['description']}")
                if c.get('assets'):
                    st.write("Assets:")
                    for a in c['assets']:
                        st.write(f"- {a['vendor']} ({a['id']})")

if choice == "Vertr\u00e4ge":
    st.header("Vertr\u00e4ge")
    if st.button("Vertr\u00e4ge laden"):
        r = requests.get(f"{API_URL}/contracts")
        if r.status_code == 200:
            df = r.json()
            st.write(df)
    with st.form("create_contract"):
        supplier = st.text_input("Lieferant")
        description = st.text_input("Beschreibung")
        contract_date = st.date_input("Vertragsdatum")
        end_date = st.date_input("Vertragsende")
        auto_extend = st.checkbox("Automatisch verl\u00e4ngern")
        notice_period = st.number_input("K\u00fcndigungsfrist (Tage)", min_value=0, step=1)
        submitted = st.form_submit_button("Erstellen")
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
                st.success("Vertrag erstellt")

if choice == "Assets":
    st.header("Assets")
    if st.button("Assets laden"):
        r = requests.get(f"{API_URL}/assets")
        if r.status_code == 200:
            df = r.json()
            st.write(df)
    with st.form("create_asset"):
        vendor = st.text_input("Hersteller")
        purchase_date = st.date_input("Kaufdatum")
        eol = st.date_input("EoL")
        info = st.text_input("Beschreibung")
        submitted = st.form_submit_button("Erstellen")
        if submitted:
            payload = {
                "vendor": vendor,
                "purchase_date": str(purchase_date),
                "eol": str(eol),
                "info": info,
            }
            resp = requests.post(f"{API_URL}/assets", json=payload)
            if resp.status_code == 200:
                st.success("Asset erstellt")
