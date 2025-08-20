import streamlit as st
import pandas as pd
from utils.sql_utils import load_sql_query


# Cache the function so it doesn't rerun every time the streamlit app reloads
@st.cache_data
def load_table(filename, _engine):
    try:
        query = load_sql_query(filename)
        return pd.read_sql(query, _engine)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
