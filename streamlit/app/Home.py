import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from utils.load_sql_query_utils import load_table
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


FILE_NAME = "team_stats.sql"
st.set_page_config(
    page_title="HoopMetrics",
    layout="wide",
    initial_sidebar_state="auto",
)


column_1, column_2, column_3 = st.columns([1, 2, 1])
with column_2:
    st.image("../images/nba_logo.avif")

st.markdown(
    "<h1 style='text-align: center; color: #60b4ff;'>HoopMetrics! 🏀</h1>",
    unsafe_allow_html=True
)


# Load database credentials from secrets.toml
db_config = st.secrets["database"]

engine = create_engine(
    f"postgresql+psycopg2://{db_config['SOURCE_DB_USER']}:"
    f"{db_config['SOURCE_DB_PASSWORD']}@"
    f"{db_config['SOURCE_DB_HOST']}:"
    f"{db_config['SOURCE_DB_PORT']}/{db_config['SOURCE_DB_NAME']}"
)

team_stats_df = load_table(FILE_NAME, engine)

# Get the years
years = sorted(team_stats_df["year"].unique())

st.markdown(
    "<h3 style='font-size:32px; color:#60b4ff;'>"
    "Team Statistics 📊</h3>",
    unsafe_allow_html=True
)

# Add dropdown for year selection
selected_year = st.selectbox(
    label="Select a Year:",
    options=years,
    help="Choose a year"
)

# Filter teams based on selected year
teams_for_year = team_stats_df.loc[
    team_stats_df["year"] == selected_year, "team_name"
].unique()

# Add dropdown for team selection
selected_team = st.selectbox(
    label="Select a Team:",
    options=sorted(teams_for_year),
    help="Choose a team",
    index=9  # Default is Golden State Warriors :)
)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# Filter the final DataFrame
filtered_team_stats_df = team_stats_df[
    (team_stats_df["year"] == selected_year)
    & (team_stats_df["team_name"] == selected_team)
]

# Display metrics in columns
column_1, column_2, column_3 = st.columns([1, 1, 1])
with column_1:
    st.metric(
        label=":blue[Total Wins]",
        value=filtered_team_stats_df["total_wins"],
        border=True,
        help="Total number of wins in the year"
    )
    st.metric(
        label=":blue[Total Losses]",
        value=filtered_team_stats_df["total_losses"],
        border=True,
        help="Total number of losses in the year"
    )
with column_2:
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
        color_discrete_map={"Win": "#60b4ff", "Loss": "red"}
    )
    # Set figure size
    pie_chart.update_layout(width=350, height=350)  # smaller size
    st.plotly_chart(pie_chart)
with column_3:
    st.metric(
        label=":blue[Total Games]",
        value=filtered_team_stats_df["total_games"],
        border=True,
        help="Total number of games"
    )
    st.metric(
        label=":blue[Win Percentage (%)]",
        value=filtered_team_stats_df["win_pct"],
        border=True,
        help="Win percentage for games in the year"
    )

st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='font-size:32px; color:#60b4ff;'>"
    "Heatmap of Team Performance (2016-2020) 🌡️</h3>",
    unsafe_allow_html=True
)

# Create a pivot DataFrame to use for the visualisation.
pivot_df = team_stats_df.pivot(
    index="team_name",  # Y axis
    columns="year",  # X axis
    values="win_pct"  # Cell values
)


# Rename columns for heatmap
pivot_df = pivot_df.rename(columns={
    "team_name": "Team",
    "year": "Year"
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
