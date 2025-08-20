import pandas as pd


def remove_special_characters(data: pd.DataFrame) -> pd.DataFrame:
    """
    Removes special characters from the 'player_name' column of the DataFrame.
    Only keeps letters, numbers, spaces, hyphens, and apostrophes.

    Args:
        data (pd.DataFrame): Input DataFrame containing a 'player_name' column.

    Returns:
        pd.DataFrame: DataFrame with cleaned 'player_name' values.
    """
    data["player_name"] = \
        data["player_name"].str.replace(r"[^a-zA-Z0-9\s\-']", "", regex=True)

    return data
