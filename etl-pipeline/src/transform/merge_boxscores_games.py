import pandas as pd

FILE_PATH = "data/processed/merged_boxscores_games.csv"


def merge_boxscores_games(
    boxscores: pd.DataFrame,
    games: pd.DataFrame
) -> pd.DataFrame:
    merged_data = pd.merge(boxscores, games, on="game_id", how="inner")
    merged_data.to_csv(FILE_PATH, index=False)

    return merged_data
