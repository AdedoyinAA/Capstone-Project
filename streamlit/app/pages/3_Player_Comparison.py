import streamlit as st
from sqlalchemy import create_engine
from utils.load_sql_query_utils import load_table


FILE_NAME = "player_info_and_salaries.sql"
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
    st.subheader(player_1)
    st.write(f"**Height:** {player_1_info["height_m"]}m")
    st.write(f"**Weight:** {player_1_info["weight_kg"]}kg")
    st.write(f"**Position(s):** {player_1_info["position"]}")
    st.write(f"**Date of Birth:** {player_1_info["birth_date"]}")
    st.write(
        f"**Salary (Inflation Adjusted):** "
        f"${player_1_info["inflation_adjusted_salary"]}"
    )
with column_2:
    st.subheader(player_2)
    st.write(f"**Height:** {player_2_info["height_m"]}m")
    st.write(f"**Weight:** {player_2_info["weight_kg"]}kg")
    st.write(f"**Position(s):** {player_2_info["position"]}")
    st.write(f"**Date of Birth:** {player_2_info["birth_date"]}")
    st.write(
        f"**Salary (Inflation Adjusted):** "
        f"${player_2_info["inflation_adjusted_salary"]}"
    )
