import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from utils.sql_utils import load_sql_query
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="HoopMetrics",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title(":blue[HoopMetrics] 🏀")


# Load database credentials from secrets.toml
db_config = st.secrets["database"]

engine = create_engine(
    f"postgresql+psycopg://{db_config['SOURCE_DB_USER']}:"
    f"{db_config['SOURCE_DB_PASSWORD']}@"
    f"{db_config['SOURCE_DB_HOST']}:"
    f"{db_config['SOURCE_DB_PORT']}/{db_config['SOURCE_DB_NAME']}"
)


# Cache the function so it doesn't rerun every time the streamlit app reloads
@st.cache_data
def load_team_stats():
    try:
        query = load_sql_query("team_stats.sql")

        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error fetching data: {e}")


team_stats_df = load_team_stats()

# Get the season start years
season_start_years = sorted(team_stats_df["season_start_year"].unique())

st.subheader(":blue[Individual Team Stats]")

# Add dropdown for year selection
selected_year = st.selectbox("Select a Season Start Year:", season_start_years)

# Filter teams based on selected year
teams_for_year = team_stats_df.loc[
    team_stats_df["season_start_year"] == selected_year, "team_name"
].unique()

# Add dropdown for team selection
selected_team = st.selectbox("Select a Team:", sorted(teams_for_year))

# Filter the final dataframe
filtered_team_stats_df = team_stats_df[
    (team_stats_df["season_start_year"] == selected_year)
    & (team_stats_df["team_name"] == selected_team)
]

# Display metrics in columns
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric(
        label=":blue[Total Wins]",
        value=filtered_team_stats_df["total_wins"],
        border=True,
        help="Total number of wins in the calendar year"
    )
    st.metric(
        label=":blue[Total Losses]",
        value=filtered_team_stats_df["total_losses"],
        border=True,
        help="Total number of losses in the calendar year"
    )
with col2:
    # Pie Chart for wins vs losses
    wins = filtered_team_stats_df["total_wins"].values[0]
    losses = filtered_team_stats_df["total_losses"].values[0]
    pie_chart_df = pd.DataFrame({
        "Result": ["Win", "Loss"],
        "Count": [wins, losses]
    })
    pie_chart = px.pie(
        pie_chart_df,
        names="Result",
        values="Count",
        color="Result",
        color_discrete_map={"Win": "blue", "Loss": "red"}
    )
    st.plotly_chart(pie_chart)
with col3:
    st.metric(
        label=":blue[Total Games]",
        value=filtered_team_stats_df["total_games"],
        border=True,
        help="Total number of games in the calendar year"
    )
    st.metric(
        label=":blue[Win Percentage]",
        value=filtered_team_stats_df["win_pct"],
        border=True,
        help="Win percentage for games in the calendar year"
    )


st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)

st.subheader(":blue[Heatmap of Team Performance (2015-2019)]")
# Create a pivot DataFrame to use for the visualisation.
pivot_df = team_stats_df.pivot(
    index="team_name",  # Y axis
    columns="season_start_year",  # X axis
    values="win_pct"  # Cell values
)
# Rename columns for heatmap
pivot_df = pivot_df.rename(columns={
    "team_name": "Team",
    "season_start_year": "Year"
    }
)

# Create the heatmap using seaborn
heatmap, ax = plt.subplots(figsize=(8, 6), facecolor="black")
sns.heatmap(
    pivot_df,
    annot=True,  # Show the numbers inside the cells
    fmt=".1f",  # Round to 1 decimal place
    cmap="YlGnBu",  # Colour range is yellow to green to blue
    cbar_kws={"label": "Win %", "orientation": "vertical"},  # Legend
    ax=ax
)

# Edit the legend colours
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.label.set_color("white")        # Color of colorbar label
cbar.ax.tick_params(colors="white")

# Edit the axis labels,colours and font size
ax.set_xlabel("Year", fontsize=12, color="white")
ax.set_ylabel("Team", fontsize=12, color="white")
ax.set_title("Team Win % by Year", fontsize=12, color="white")
ax.tick_params(colors="white")
ax.yaxis.set_tick_params(color="white")

# Plot the heatmap
st.pyplot(heatmap)
