import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px
from utils.load_sql_query_utils import load_table

FILE_NAME = "player_info_and_salaries.sql"
# Set the page title and layout size
st.set_page_config(
    page_title="Salaries Analysis",
    layout="wide"
)

st.title(":blue[Salaries Analysis] 💸💸")

# Load the database credentials from secrets.toml
db_config = st.secrets["database"]

engine = create_engine(
    f"postgresql+psycopg2://{db_config['SOURCE_DB_USER']}:"
    f"{db_config['SOURCE_DB_PASSWORD']}@"
    f"{db_config['SOURCE_DB_HOST']}:"
    f"{db_config['SOURCE_DB_PORT']}/{db_config['SOURCE_DB_NAME']}"
)

player_salaries_df = load_table(FILE_NAME, engine)

# Keep the most recent information for each player
player_recent_salaries_df = player_salaries_df.drop_duplicates(
    subset="player_name",
    keep="last"
)

# Remove the commas from the salary string then convert to int
player_recent_salaries_df.loc[:, "salary"] = \
    player_recent_salaries_df["salary"].apply(
        lambda x: int(str(x).replace(",", ""))
    )

# Group by height
average_salary_by_height_df = (
    player_recent_salaries_df
    .groupby("height_m", as_index=False)["salary"]
    .mean()
    .round(2)
)

# Group by weight
average_salary_by_weight_df = (
    player_recent_salaries_df
    .groupby("weight_kg", as_index=False)["salary"]
    .mean()
    .round(2)
)

# Keep only players that play one position
single_position_players_df = player_recent_salaries_df[
    ~player_recent_salaries_df["position"].str.contains(",", na=False)
]

# For players with multiple positions, keep their primary position only
player_recent_salaries_df = player_recent_salaries_df.copy()
player_recent_salaries_df.loc[:, "primary_position"] = (
    player_recent_salaries_df["position"]
    .astype(str)
    .str.split(",")
    .str[0]
    .str.strip()
)
salary_stats = (
    player_recent_salaries_df
    .groupby("primary_position")["salary"].agg(
        median="median",
        p95=lambda x: x.quantile(0.95),
        p99=lambda x: x.quantile(0.99)
    ).reset_index()
)

# Melt the DataFrame so it can be plotted
salary_stats_melted = salary_stats.melt(
    id_vars="primary_position",
    value_vars=["median", "p95", "p99"],
    var_name="statistic",
    value_name="salary"
)

# Custom colours for bar graph
custom_colours = {
    "median": "#60b4ff",  # blue
    "p95": "#ff0000",     # red
    "p99": "#fafafa",     # white
}

# Group by playing position
average_salary_by_position_df = (
    player_recent_salaries_df
    .groupby("primary_position", as_index=False)["salary"]
    .mean()
    .round(2)
)

# Choose a comparison metric
metric_options = {
    "Height (m)": (average_salary_by_height_df, "height_m"),
    "Position": (salary_stats_melted, "primary_position"),
    "Weight (kg)": (average_salary_by_weight_df, "weight_kg")
}

selected_metric_to_display = st.selectbox(
    "Select :blue[Metric] to Compare:",
    list(metric_options.keys())
)


# Get the actual metric name
selected_metric = metric_options[selected_metric_to_display]

# Pick the correct DataFrame and x-axis column
df, x_column = metric_options[selected_metric_to_display]
# df = globals()[df_name]

# Plot a bar graph if the selected metric is Position.
if selected_metric_to_display == "Position":
    fig = px.bar(
        df,
        x=x_column,
        y="salary",
        color="statistic",
        barmode="group",
        text="statistic",
        labels={
            "primary_position": "Player Position",
            "salary": "Salary ($)",
            "statistic": "Statistic"
        },
        color_discrete_map=custom_colours,
        height=550,
        title="Median, P95, P99 Salaries by Position"
    )
else:
    fig = px.line(
        df,
        x=x_column,
        y="salary",
        labels={
            "height_m": "Player Height (metres)",
            "weight_kg": "Player Weight (kgs)",
            "salary": "Average Salary ($)"
        },
        color_discrete_sequence=["#60b4ff"],
        markers=True,
        height=550,
        title=f"Average Salary by {selected_metric_to_display}"
    )

# Change font size and colour of title
fig.update_layout(title_font=dict(size=22, color='#60b4ff'))
# Plot the graph
st.plotly_chart(fig, use_container_width=True)
