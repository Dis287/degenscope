import os
import streamlit as st

# Securely load API key — works in Streamlit Cloud AND Codespaces
api_key = st.secrets.get("POLYGON_API_KEY") or os.environ.get("POLYGON_API_KEY")

if not api_key:
    st.error("🔑 API key not found! Add POLYGON_API_KEY in Streamlit Secrets or run `export POLYGON_API_KEY='your_key'` in terminal.")
    st.stop()

client = RESTClient(api_key=api_key)
