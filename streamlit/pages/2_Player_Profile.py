import streamlit as st
from sqlalchemy import create_engine
from utils.load_sql_query_utils import load_table


FILE_NAME = "player_info_and_salaries.sql"
# Set the page title and layout size
st.set_page_config(
    page_title="Player Profile",
    layout="wide",
    initial_sidebar_state="auto"
)

st.title(":blue[Player Profile] 👤")


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

# Select player
player = st.selectbox(
    "Select a :blue[Player]:",
    player_info_df["player_name"],
    help="Choose the player",
    index=193  # Stephen Curry
)

# Filter the DataFrame for each player
player_info = player_info_df[
    player_info_df["player_name"] == player
    ].iloc[0]

# Display the players' info
st.markdown(
    "<h3 style='font-size:32px; color:#60b4ff;'>"
    f"{player} </h3>",
    unsafe_allow_html=True
)
st.metric(
    label=":blue[Height (m)]",
    value=f"{player_info['height_m']}",
    border=True,
    help="Player's height in metres"
)
st.metric(
    label=":blue[Weight (kg)]",
    value=f"{player_info['weight_kg']}",
    border=True,
    help="Player's weight in kilograms"
)
st.metric(
    label=":blue[Position(s)]",
    value=f"{player_info['position']}",
    border=True,
    help="Player's position"
)
st.metric(
    label=":blue[Date of Birth]",
    value=f"{player_info['birth_date']}",
    border=True,
    help="Player's date of birth"
)
st.metric(
    label=":blue[Salary]",
    value=f"${player_info['salary']}",
    border=True,
    help="Player's last recorded salary per year"
    )
