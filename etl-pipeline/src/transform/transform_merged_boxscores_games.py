import pandas as pd

PLAYER_STATS_FILE_PATH = "data/processed/player_stats.csv"
TEAM_STATS_FILE_PATH = "data/processed/team_stats.csv"

COLUMNS_TO_DROP = [
    "player_name",
    "minutes_played",
    "field_goals",
    "field_goals_attempted",
    "three_pointers",
    "three_pointers_attempted",
    "free_throws",
    "free_throws_attempted",
    "total_rebounds",
    "assists",
    "points",
    "is_starter",
    "field_goals_percentage_%",
    "three_point_percentage_%",
    "free_throws_percentage_%"
]


def get_player_stats(data: pd.DataFrame) -> pd.DataFrame:
    player_stats_df = (
        data.groupby(["player_name", "season_start_year"])
        .agg({
            "points": "mean",
            "assists": "mean",
            "total_rebounds": "mean",
            "field_goals_percentage_%": "mean",
            "three_point_percentage_%": "mean",
            "free_throws_percentage_%": "mean",
            "three_pointers": "sum"
        })
        .round({
            "points": 1,
            "assists": 1,
            "total_rebounds": 1,
            "field_goals_percentage_%": 2,
            "free_throws_percentage_%": 2,
            "three_point_percentage_%": 2,
        })
        .reset_index()
        .rename(columns={
            "points": "points_per_game",
            "assists": "assists_per_game",
            "total_rebounds": "rebounds_per_game",
            "field_goals_percentage_%": "field_goal_%_per_game",
            "three_point_percentage_%": "three_point_%_per_game",
            "free_throws_percentage_%": "free_throws_%_per_game",
            "three_pointers": "total_three_pointers"
        })
    )
    player_stats_df.to_csv(PLAYER_STATS_FILE_PATH, index=False)

    return player_stats_df


def determine_winner(row):
    if row["team_name"] == row["home_team"]:
        return int(row["points_home"] > row["points_away"])
    elif row["team_name"] == row["away_team"]:
        return int(row["points_away"] > row["points_home"])
    else:
        return None


def add_won_game_column(data: pd.DataFrame) -> pd.DataFrame:
    # Column to represent game wins
    data["won_game"] = data.apply(determine_winner, axis=1)

    return data


def remove_unnecessary_columns(data: pd.DataFrame) -> pd.DataFrame:
    # Drop unnecessary columns
    data.drop(
        columns=COLUMNS_TO_DROP,
        inplace=True
    )

    return data


def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    # Drop duplicates
    team_wins_df = data.drop_duplicates()

    return team_wins_df


def get_total_number_of_wins(data: pd.DataFrame) -> pd.DataFrame:
    # Count total number of wins a team has
    total_wins_df = (
        data.groupby(["season_start_year", "team_name"])["won_game"]
        .sum()
        .reset_index()
        .rename(columns={
            "won_game": "total_wins"
        })
    )

    return total_wins_df


def get_total_number_of_games_played(data: pd.DataFrame) -> pd.DataFrame:
    # Count total number of games a team played every year
    games_played_df = (
        data.groupby(["season_start_year", "team_name"])["won_game"]
        .count()
        .reset_index()
        .rename(columns={
            "won_game": "total_games"
        })
    )

    return games_played_df


def get_team_stats(data: pd.DataFrame) -> pd.DataFrame:
    # Column to represent game wins
    data = add_won_game_column(data)

    # Drop unnecessary columns
    data = remove_unnecessary_columns(data)

    # Drop duplicates
    team_wins_df = remove_duplicates(data)

    # Count total number of wins a team has
    total_wins_df = get_total_number_of_wins(team_wins_df)

    # Count total number of games a team played every year
    games_played_df = get_total_number_of_games_played(team_wins_df)

    # Create a new DataFrame to have the team stats for each year
    team_stats_df = pd.merge(
        games_played_df,
        total_wins_df,
        on=["season_start_year", "team_name"])

    # Add a new column to find out how many losses a team had
    team_stats_df["total_losses"] = (
        team_stats_df["total_games"] - team_stats_df["total_wins"]
    )

    # Add a new column to calculate the win percentage
    team_stats_df["win_%"] = (
        (team_stats_df["total_wins"] / team_stats_df["total_games"] * 100)
        .round(2)
    )
    team_stats_df.to_csv(TEAM_STATS_FILE_PATH, index=False)

    return team_stats_df
