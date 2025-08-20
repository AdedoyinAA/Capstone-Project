import streamlit as st
from sqlalchemy import create_engine
from utils.load_sql_query_utils import load_table


FILE_NAME = "player_info_and_salaries.sql"
# Set the page title and layout size
st.set_page_config(
    page_title="Player Comparison",
    layout="wide",
    initial_sidebar_state="auto"
)

st.title(":blue[Player Comparison] ⚖️")


# Load database credentials from secrets.toml
db_config = st.secrets["database"]

engine = create_engine(
    f"postgresql+psycopg2://{db_config['SOURCE_DB_USER']}:"
    f"{db_config['SOURCE_DB_PASSWORD']}@"
    f"{db_config['SOURCE_DB_HOST']}:"
    f"{db_config['SOURCE_DB_PORT']}/{db_config['SOURCE_DB_NAME']}"
)

player_info_df = load_table(FILE_NAME, engine)

# Keep the most recent information for each player
player_info_df = player_info_df.drop_duplicates(
    subset="player_name",
    keep="last"
)


# Select players
column_1, column_2 = st.columns(2)
with column_1:
    player_1 = st.selectbox(
        "Select First Player:",
        player_info_df["player_name"],
        help="Choose the first player",
        index=193  # Stephen Curry
    )
with column_2:
    player_2 = st.selectbox(
        "Select Second Player:",
        player_info_df["player_name"],
        help="Choose the second player",
        index=404  # LeBron James
    )

# Filter the DataFrame for each player
player_1_info = player_info_df[
    player_info_df["player_name"] == player_1
    ].iloc[0]
player_2_info = player_info_df[
    player_info_df["player_name"] == player_2
    ].iloc[0]

# Display the players' info
column_1, column_2 = st.columns(2)
with column_1:
    st.markdown(
        "<h3 style='font-size:32px; color:#60b4ff;'>"
        f"{player_1} </h3>",
        unsafe_allow_html=True
    )
    st.metric(
        label=":blue[Height (m)]",
        value=f"{player_1_info['height_m']}",
        border=True,
        help="Player's height in metres"
    )
    st.metric(
        label=":blue[Weight (kg)]",
        value=f"{player_1_info['weight_kg']}",
        border=True,
        help="Player's weight in kilograms"
    )
    st.metric(
        label=":blue[Position(s)]",
        value=f"{player_1_info['position']}",
        border=True,
        help="Player's position"
    )
    st.metric(
        label=":blue[Date of Birth]",
        value=f"{player_1_info['birth_date']}",
        border=True,
        help="Player's date of birth"
    )
    st.metric(
        label=":blue[Salary (Inflation Adjusted)]",
        value=f"${player_1_info['inflation_adjusted_salary']}",
        border=True,
        help="Player's salary per year"
    )
with column_2:
    st.markdown(
        "<h3 style='font-size:32px; color:#ff4b4b;'>"
        f"{player_2} </h3>",
        unsafe_allow_html=True
    )
    st.metric(
        label=":red[Height (m)]",
        value=f"{player_2_info['height_m']}",
        border=True,
        help="Player's height in metres"
    )
    st.metric(
        label=":red[Weight (kg)]",
        value=f"{player_2_info['weight_kg']}",
        border=True,
        help="Player's weight in kilograms"
    )
    st.metric(
        label=":red[Position(s)]",
        value=f"{player_2_info['position']}",
        border=True,
        help="Player's position"
    )
    st.metric(
        label=":red[Date of Birth]",
        value=f"{player_2_info['birth_date']}",
        border=True,
        help="Player's date of birth"
    )
    st.metric(
        label=":red[Salary (Inflation Adjusted)]",
        value=f"${player_2_info['inflation_adjusted_salary']}",
        border=True,
        help="Player's salary per year"
    )
