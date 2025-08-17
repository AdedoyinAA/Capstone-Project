import pandas as pd
from typing import Tuple
from src.transform.clean_boxscores import clean_boxscores
from src.transform.clean_games import clean_games


def transform_data(data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    cleaned_boxscores = clean_boxscores(data[0])
    cleaned_games = clean_games(data[1])
    return (cleaned_boxscores, cleaned_games)
