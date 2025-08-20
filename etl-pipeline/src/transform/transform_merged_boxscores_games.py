import pandas as pd
import os

PLAYER_STATS_FILE_PATH = "data/processed/player_stats.csv"
TEAM_STATS_FILE_PATH = "data/processed/team_stats.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(PLAYER_STATS_FILE_PATH), exist_ok=True)
os.makedirs(os.path.dirname(TEAM_STATS_FILE_PATH), exist_ok=True)

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
    "field_goals_percentage",
    "three_point_percentage",
    "free_throws_percentage"
]


def get_player_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate per-year player statistics from boxscore data.

    Args:
        data (pd.DataFrame): DataFrame containing boxscore statistics
        with columns including:
            'player_name', 'year', 'points', 'assists', 'total_rebounds',
            'field_goals_percentage', 'three_point_percentage',
            'free_throws_percentage', and 'three_pointers'.

    Returns:
        pd.DataFrame: DataFrame with aggregated player statistics per year,
        including:
        - points_per_game
        - assists_per_game
        - rebounds_per_game
        - field_goal_pct_per_game
        - three_point_pct_per_game
        - free_throws_pct_per_game
        - total_three_pointers
    """
    player_stats_df = (
        data.groupby(["player_name", "year"])
        .agg({
            "points": "mean",
            "assists": "mean",
            "total_rebounds": "mean",
            "field_goals_percentage": "mean",
            "three_point_percentage": "mean",
            "free_throws_percentage": "mean",
            "three_pointers": "sum"
        })
        .round({
            "points": 1,
            "assists": 1,
            "total_rebounds": 1,
            "field_goals_percentage": 2,
            "free_throws_percentage": 2,
            "three_point_percentage": 2,
        })
        .reset_index()
        .rename(columns={
            "points": "points_per_game",
            "assists": "assists_per_game",
            "total_rebounds": "rebounds_per_game",
            "field_goals_percentage": "field_goal_pct_per_game",
            "three_point_percentage": "three_point_pct_per_game",
            "free_throws_percentage": "free_throws_pct_per_game",
            "three_pointers": "total_three_pointers"
        })
    )
    player_stats_df.to_csv(PLAYER_STATS_FILE_PATH, index=False)

    return player_stats_df


def determine_winner(row):
    """
    Determine if the team in the row won the game.

    Args:
        row (pd.Series): A row from the boxscore DataFrame containing
        'team_name', 'home_team', 'away_team',
        'points_home', 'points_away'.

    Returns:
        int or None: 1 if the team won, 0 if the team lost,
        None if team not found.
    """
    if row["team_name"] == row["home_team"]:
        # Home team wins if points_home > points_away
        return int(row["points_home"] > row["points_away"])
    elif row["team_name"] == row["away_team"]:
        # Away team wins if points_away > points_home
        return int(row["points_away"] > row["points_home"])
    else:
        # Team not found in this game
        return None


def add_won_game_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add a column indicating whether the team won the game.

    Args:
        data (pd.DataFrame): DataFrame containing 'team_name', 'home_team',
                             'away_team', 'points_home', 'points_away'.

    Returns:
        pd.DataFrame: DataFrame with an added 'won_game' column
        (1 = win, 0 = loss).
    """
    # Column to represent game wins
    data["won_game"] = data.apply(determine_winner, axis=1)

    return data


def remove_unnecessary_columns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove unnecessary columns from the DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.
        COLUMNS_TO_DROP (list): List of column names to remove.

    Returns:
        pd.DataFrame: DataFrame with specified columns removed.
    """
    data.drop(
        columns=COLUMNS_TO_DROP,
        inplace=True
    )

    return data


def remove_duplicates(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with duplicate rows removed.
    """
    # Drop duplicates
    team_wins_df = data.drop_duplicates()

    return team_wins_df


def get_total_number_of_wins(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the total number of wins per team per year.

    Args:
        data (pd.DataFrame): DataFrame containing team game
        results with a 'won_game' column.

    Returns:
        pd.DataFrame: DataFrame with the total number of wins
    """
    # Count total number of wins a team has
    total_wins_df = (
        data.groupby(["year", "team_name"])["won_game"]
        .sum()
        .reset_index()
        .rename(columns={
            "won_game": "total_wins"
        })
    )

    return total_wins_df


def get_total_number_of_games_played(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the total number of games played per team per year.

    Args:
        data (pd.DataFrame): DataFrame containing team game results
        with a 'won_game' column.

    Returns:
        pd.DataFrame: DataFrame with the total games played.
    """
    # Count total number of games a team played every year
    games_played_df = (
        data.groupby(["year", "team_name"])["won_game"]
        .count()
        .reset_index()
        .rename(columns={
            "won_game": "total_games"
        })
    )

    return games_played_df


def get_team_stats(data: pd.DataFrame) -> pd.DataFrame:
    """
    A DataFrame which contains all the stats relating to a team
    per year.

    Args:
        data (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing team statistics.
    """
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
        on=["year", "team_name"])

    # Add a new column to find out how many losses a team had
    team_stats_df["total_losses"] = (
        team_stats_df["total_games"] - team_stats_df["total_wins"]
    )

    # Add a new column to calculate the win percentage
    team_stats_df["win_pct"] = (
        (team_stats_df["total_wins"] / team_stats_df["total_games"] * 100)
        .round(2)
    )
    team_stats_df.to_csv(TEAM_STATS_FILE_PATH, index=False)

    return team_stats_df
