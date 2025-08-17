import pandas as pd
from typing import Tuple
from src.transform.clean_boxscores import clean_boxscores


def transform_data(data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    cleaned_boxscores = clean_boxscores(data[0])

    return (cleaned_boxscores)
