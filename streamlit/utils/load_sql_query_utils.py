import streamlit as st
import pandas as pd
from utils.sql_utils import load_sql_query


# Cache the function so it doesn't rerun every time the streamlit app reloads
@st.cache_data
def load_table(filename, _engine):
    """
    Load a SQL query from a file and execute it against a database engine.
    The results are cached by Streamlit to avoid re-running the query
    unnecessarily across app reruns.

    Args:
        filename (str): Path to the `.sql` file containing the query.
        _engine (sqlalchemy.engine.Engine): Database engine/connection
        used to execute the query.

    Returns:
        pd.DataFrame: DataFrame containing the query results.

    Raises:
        Exception: If there is an error while loading the query file
        or executing the SQL query.
    """
    try:
        query = load_sql_query(filename)
        return pd.read_sql(query, _engine)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
