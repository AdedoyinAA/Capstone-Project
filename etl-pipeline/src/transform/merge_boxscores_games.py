import pandas as pd

FILE_PATH = "data/processed/merged_boxscores_games.csv"


def merge_boxscores_games(
    boxscores: pd.DataFrame,
    games: pd.DataFrame
) -> pd.DataFrame:
    boxscores_and_games_df = pd.merge(
        boxscores,
        games,
        on="game_id",
        how="inner"
    )

    boxscores_and_games_df.to_csv(FILE_PATH, index=False)

    return boxscores_and_games_df
