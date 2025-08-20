import pandas as pd
import os
from src.utils.trimming_whitespace_utils import trim_whitespaces

FILE_PATH = "data/processed/cleaned_boxscores.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)


def clean_boxscores(boxscores: pd.DataFrame) -> pd.DataFrame:
    # Remove unnecessary columns
    boxscores = remove_unnecessary_columns(boxscores)
    # Change numeric values to 0 where there are any conditions,
    # where a player did not play a game for any reason
    boxscores = check_player_conditions(boxscores)
    # Convert to int64
    boxscores = convert_to_numeric(boxscores)
    # Rename columns
    boxscores = rename_columns(boxscores)
    # Trim whitespaces
    boxscores = trim_whitespaces(boxscores)
    # Calculate field goals percentage
    boxscores = calculate_field_goals_percentage(boxscores)
    # Calculate three point percentage
    boxscores = calculate_three_point_percentage(boxscores)
    # Calculate free throws percentage
    boxscores = calculate_free_throws_percentage(boxscores)

    # Save the cleaned dataframe as a CSV
    boxscores.to_csv(FILE_PATH, index=False)
    return boxscores


def remove_unnecessary_columns(boxcores: pd.DataFrame) -> pd.DataFrame:
    """Remove columns from the boxscores DataFrame that
    are not needed for analysis.

    Args:
        boxcores (pd.DataFrame): The original DataFrame
        containing player boxscore statistics.

    Returns:
        pd.DataFrame: A DataFrame with unnecessary columns removed.
    """
    columns_to_drop = ["ORB", "DRB", "STL", "BLK", "TOV", "PF", "+/-"]
    boxcores.drop(
        columns=columns_to_drop,
        inplace=True
    )
    return boxcores


def check_player_conditions(boxscores: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where players did not participate in a game.

    Args:
        boxscores (pd.DataFrame): The DataFrame containing player boxscore
        data, including a 'MP' (minutes played) column
        which may indicate game participation status.

    Returns:
        pd.DataFrame: A cleaned DataFrame containing only rows where players
        actually played, with rows such as 'Did Not Play',
        'Player Suspended', 'Not With Team', and 'Did Not Dress' removed.
    """
    conditions = [
        "Did Not Play",
        "Player Suspended",
        "Not With Team",
        "Did Not Dress"
    ]

    # Keep only rows where players played a game
    boxscores = boxscores.loc[~boxscores["MP"].isin(conditions)].copy()

    return boxscores


def convert_to_numeric(boxscores: pd.DataFrame) -> pd.DataFrame:
    """Convert selected columns in the boxscores DataFrame to numeric (int64).

    This function ensures that statistical columns such as field goals,
    attempts, rebounds, assists, and points are stored as integers.
    Any non-numeric values are coerced to NaN before conversion.

    Args:
        boxscores (pd.DataFrame): The DataFrame
        containing player boxscore data.

    Returns:
        pd.DataFrame: The DataFrame with specified columns converted
        to int64 numeric type.
    """
    columns_to_convert_to_int = [
        "FG",
        "FGA",
        "3P",
        "3PA",
        "FT",
        "FTA",
        "TRB",
        "AST",
        "PTS",
        "isStarter"
    ]

    # Change to numeric data type int64
    boxscores[columns_to_convert_to_int] = boxscores[
        columns_to_convert_to_int].apply(
            pd.to_numeric, errors="coerce").astype("int64")

    return boxscores


def rename_columns(boxscores: pd.DataFrame) -> pd.DataFrame:
    """Rename columns in the boxscores DataFrame for clarity and consistency.

    This function renames columns such as 'FG', '3P', and 'MP' into more
    descriptive names like 'field_goals', 'three_pointers', and
    'minutes_played'. This improves readability and standardizes
    column naming conventions for downstream analysis.

    Args:
        boxscores (pd.DataFrame): The DataFrame containing player boxscore data
        with original column names.

    Returns:
        pd.DataFrame: The DataFrame with renamed columns for clarity.
    """
    dict_for_renaming_columns = {
        "teamName": "team_name",
        "playerName": "player_name",
        "MP": "minutes_played",
        "FG": "field_goals",
        "FGA": "field_goals_attempted",
        "3P": "three_pointers",
        "3PA": "three_pointers_attempted",
        "FT": "free_throws",
        "FTA": "free_throws_attempted",
        "TRB": "total_rebounds",
        "AST": "assists",
        "PTS": "points",
        "isStarter": "is_starter"
    }
    boxscores = boxscores.rename(columns=dict_for_renaming_columns)

    return boxscores


def calculate_field_goals_percentage(boxscores: pd.DataFrame) -> pd.DataFrame:
    """Calculate the field goals percentage for each player in the DataFrame.

    This function computes the field goals percentage as:
        (field_goals / field_goals_attempted) * 100
    It rounds the result to 2 decimal places. If a player attempted 0
    field goals, the percentage is set to 0 to avoid division by zero.

    Args:
        boxscores (pd.DataFrame): The DataFrame containing player boxscore data
        with columns 'field_goals' and 'field_goals_attempted'.

    Returns:
        pd.DataFrame: The DataFrame with a new column 'field_goals_percentage'
        containing the calculated percentages.
    """
    # Add a new column which calculates the field goals percentage
    boxscores["field_goals_percentage"] = (
        boxscores["field_goals"] / boxscores["field_goals_attempted"] * 100
    ).round(2)

    # Change NaN values to 0
    boxscores.loc[boxscores[
        "field_goals_attempted"] == 0,
        "field_goals_percentage"] = 0

    return boxscores


def calculate_three_point_percentage(boxscores: pd.DataFrame) -> pd.DataFrame:
    """Calculate the three-point field goal percentage for each player.

    This function computes the three-point percentage as:
        (three_pointers / three_pointers_attempted) * 100
    and rounds the result to 2 decimal places. If a player attempted 0
    three-pointers, the percentage is set to 0 to avoid division by zero.

    Args:
        boxscores (pd.DataFrame): The DataFrame containing player boxscore data
        with columns 'three_pointers' and 'three_pointers_attempted'.

    Returns:
        pd.DataFrame: The DataFrame with a new column 'three_point_percentage'
        containing the calculated percentages.
    """
    # Add a new column which calculates the three pointers percentage
    boxscores["three_point_percentage"] = (
        (boxscores["three_pointers"]
         / boxscores["three_pointers_attempted"]
         * 100)
    ).round(2)

    # Change NaN values to 0
    boxscores.loc[boxscores[
        "three_pointers_attempted"] == 0,
        "three_point_percentage"] = 0

    return boxscores


def calculate_free_throws_percentage(boxscores: pd.DataFrame) -> pd.DataFrame:
    """Calculate the free throw percentage for each player.

    This function computes the free throw percentage as:
        (free_throws / free_throws_attempted) * 100
    and rounds the result to 2 decimal places. If a player attempted 0
    free throws, the percentage is set to 0 to avoid division by zero.

    Args:
        boxscores (pd.DataFrame): The DataFrame containing player boxscore data
        with columns 'free_throws' and 'free_throws_attempted'.

    Returns:
        pd.DataFrame: The DataFrame with a new column 'free_throws_percentage'
        containing the calculated percentages.
    """
    # Add a new column which calculates the free throws percentage
    boxscores["free_throws_percentage"] = (
        (boxscores["free_throws"]
         / boxscores["free_throws_attempted"]
         * 100)
    ).round(2)

    # Change NaN values to 0
    boxscores.loc[boxscores[
        "free_throws_attempted"] == 0,
        "free_throws_percentage"] = 0

    return boxscores
