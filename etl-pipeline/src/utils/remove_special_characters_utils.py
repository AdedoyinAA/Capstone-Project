import pandas as pd


def remove_special_characters(data: pd.DataFrame) -> pd.DataFrame:
    data["player_name"] = \
        data["player_name"].str.replace(r"[^a-zA-Z0-9\s\-']", "", regex=True)

    return data
