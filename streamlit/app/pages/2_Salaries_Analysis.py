import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px
from utils.load_sql_query_utils import load_table

FILE_NAME = "player_info_and_salaries.sql"
st.set_page_config(
    page_title="Salaries Analysis",
    layout="wide"
)

st.title(":blue[Salaries Analysis] 💸💸")
st.write(
    "How does the average salary change "
    "based on their height, weight or their playing positions?"
)

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

player_recent_salaries_df.loc[:, "inflation_adjusted_salary"] = \
    player_recent_salaries_df["inflation_adjusted_salary"].apply(
        lambda x: int(str(x).replace(",", ""))
    )

# Group by height
average_salary_by_height_df = (
    player_recent_salaries_df
    .groupby("height_m", as_index=False)["inflation_adjusted_salary"]
    .mean()
    .round(2)
)

# Group by weight
average_salary_by_weight_df = (
    player_recent_salaries_df
    .groupby("weight_kg", as_index=False)["inflation_adjusted_salary"]
    .mean()
    .round(2)
)

# Keep only players that play one position
single_position_players_df = player_recent_salaries_df[
    ~player_recent_salaries_df["position"].str.contains(",", na=False)
]

# Group by playing position
average_salary_by_position_df = (
    single_position_players_df
    .groupby("position", as_index=False)["inflation_adjusted_salary"]
    .mean()
    .round(2)
)

# Choose a comparison metric
metric_options = {
    "Height (m)": (average_salary_by_height_df, "height_m"),
    "Position": (average_salary_by_position_df, "position"),
    "Weight (kg)": (average_salary_by_weight_df, "weight_kg")
}

selected_metric_to_display = st.selectbox(
    "Select Metric to Compare:",
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
        y="inflation_adjusted_salary",
        labels={
            "position": "Player Position",
            "inflation_adjusted_salary": "Average Salary ($)"
        },
        color_discrete_sequence=["#60b4ff"],
        title="Average Salary by Position"
    )
else:
    fig = px.line(
        df,
        x=x_column,
        y="inflation_adjusted_salary",
        labels={
            "height_m": "Player Height (metres)",
            "weight_kg": "Player Weight (kgs)",
            "inflation_adjusted_salary": "Average Salary ($)"
        },
        color_discrete_sequence=["#60b4ff"],
        markers=True,
        title=f"Average Salary by {selected_metric_to_display}"
    )
fig.update_layout(title_font=dict(size=22, color='#60b4ff'))
st.plotly_chart(fig, use_container_width=True)
