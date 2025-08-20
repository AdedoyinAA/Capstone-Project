import pandas as pd
import os

FILE_PATH = "data/processed/merged_playerinfo_salaries.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)


def merge_playerinfo_salaries(
    playerinfo: pd.DataFrame,
    salaries: pd.DataFrame
) -> pd.DataFrame:
    """
    Merge the player information DataFrame with the salaries
    DataFrame on 'player_name'.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player details
        such as height, weight, position, and birth date.
        salaries (pd.DataFrame): DataFrame containing player salaries
        and season information, must include 'player_name'.

    Returns:
        pd.DataFrame: Merged DataFrame containing player information
        along with salary data for each season.
    """
    player_info_and_salaries_df = pd.merge(
        playerinfo,
        salaries,
        how="inner",
        on="player_name"
    )

    player_info_and_salaries_df = player_info_and_salaries_df[[
        "season_start_year",
        "player_name",
        "position",
        "height",
        "weight",
        "birth_date",
        "weight_kg",
        "height_m",
        "salary",
        "inflation_adjusted_salary"
    ]]

    player_info_and_salaries_df.to_csv(FILE_PATH, index=False)

    return player_info_and_salaries_df
