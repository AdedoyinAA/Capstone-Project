import pandas as pd
import os

FILE_PATH = "data/processed/merged_boxscores_games.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)


def merge_boxscores_games(
    boxscores: pd.DataFrame,
    games: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge the boxscores DataFrame with the games DataFrame on 'game_id'.

    Args:
        boxscores (pd.DataFrame): DataFrame containing player boxscore
        statistics, must include 'game_id'.
        games (pd.DataFrame): DataFrame containing game-level
        information, must include 'game_id'.

    Returns:
        pd.DataFrame: Merged DataFrame containing
        both player statistics and game information.
    """
    boxscores_and_games_df = pd.merge(
        boxscores,
        games,
        on="game_id",
        how="inner"
    )

    boxscores_and_games_df.to_csv(FILE_PATH, index=False)

    return boxscores_and_games_df
