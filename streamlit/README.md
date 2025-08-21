![NBA Logo](/streamlit/images/nba_logo.avif)
# HoopMetrics Streamlit Application

This Streamlit application provides an interave dashboard for exploring NBA data, offering insights into player performance, salaries, and team statistics.

With a clean interface and powerful visualizations, the app allows you to:
- **⛹️ Analyze Player Statistics** – Track points, assists, rebounds, and shooting percentages across calendar years.
- **💸💸 Explore Salaries** – Compare player earnings by height, weight, and position.
- **⚖️ Compare Players** – Select two players side-by-side to compare their yearly stats.
- **🏆 Team Statistics** – Dive into team-level performance and trends across calendar years.
  
This app is built with:
- [Streamlit](https://streamlit.io) for the interactive UI.
- [Pandas](https://pandas.pydata.org) for data processing.
- [Plotly](https://plotly.com) and [Seaborn](https://seaborn.pydata.org) for visualisations.
- SQL queries for enriched data retrieval.
  

## Prerequisites:
- A postgreSQL database which contains the enriched data produced by the ETL Pipeline.
  
## How to Run it:
1. **Follow the same steps outlined in the `etl-pipeline/README.md` file (if not done already).**
2. **You should now have the enriched dataset stored in your postgreSQL database.**
3. **Optional: Deactivate the previous virtual environment using `deactivate` and create a new one in the `streamlit` directory.**
4. **After creating and activating the virtual environment, run the following to install the python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5. **Add a new folder called `.streamlit` in the `streamlit` directory and inside this, add a `secrets.toml` file and add these variables (fill with your own database details)**:
    ```bash
    [database]
    SOURCE_DB_NAME = <your_db_name>
    SOURCE_DB_USER = <your_db_user>
    SOURCE_DB_PASSWORD = <your_db_user_password>
    SOURCE_DB_HOST = <your_db_host>
    SOURCE_DB_PORT = <your_db_port>
    ```
6. **In the `sql` folder, there would be three (3) SQL scripts: `player_info_and_salaries.sql`, `player_stats.sql` and `team_stats.sql`. These would have to be changed to match the schema of your created database i.e.**:
   
    ```sql
    -- player_stats.sql
    SELECT
        player_name,
        year,
        points_per_game,
        assists_per_game,
        rebounds_per_game,
        field_goal_pct_per_game,
        three_point_pct_per_game,
        free_throws_pct_per_game,
        total_three_pointers
    FROM
        de_2506_a.aa_player_stats;
    ```
    In this file, change the table to `public.aa_player_stats`. Your postgreSQL schema name should be `public` for this entire project to work.
7. **Run the Streamlit application**:
   ```bash
   streamlit run Home.py
   ```
