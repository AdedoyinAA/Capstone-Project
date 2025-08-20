import pandas as pd
import os
from src.utils.trimming_whitespace_utils import trim_whitespaces
from src.utils.remove_special_characters_utils import remove_special_characters

FILE_PATH = "data/processed/cleaned_playerinfo.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)


def clean_playerinfo(playerinfo: pd.DataFrame) -> pd.DataFrame:
    # Remove unnecessary columns
    playerinfo = remove_unnecessary_columns(playerinfo)
    # Rename columns
    playerinfo = rename_columns(playerinfo)
    # Remove missing values
    playerinfo = remove_missing_values(playerinfo)
    # Change position values
    playerinfo = change_position_values(playerinfo)
    # Calculate weight in kg
    playerinfo = calculate_weight_kg(playerinfo)
    # Calculate height in metres
    playerinfo = calculate_height_m(playerinfo)
    # Trim whitespaces
    playerinfo = trim_whitespaces(playerinfo)
    # Remove special characters from player names
    playerinfo = remove_special_characters(playerinfo)
    # Save the cleaned dataframe as a CSV
    playerinfo.to_csv(FILE_PATH, index=False)
    return playerinfo


def remove_unnecessary_columns(playerinfo: pd.DataFrame) -> pd.DataFrame:
    """Remove unnecessary columns from the player information DataFrame.

    This function drops the columns "Colleges", "From", and "To"
    from the given DataFrame, which are not needed for further analysis.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player information
        including
        columns "Colleges", "From", and "To".

    Returns:
        pd.DataFrame: A new DataFrame with the unnecessary columns removed.
    """
    columns_to_drop = ["Colleges", "From", "To"]
    playerinfo = playerinfo.drop(columns=columns_to_drop, axis="columns")

    return playerinfo


def rename_columns(playerinfo: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns in the player information DataFrame to more descriptive
    names.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player information
        with columns like "playerName", "Pos", "Ht", "Wt", "birthDate", etc.

    Returns:
        pd.DataFrame: A new DataFrame with renamed columns for clarity, e.g.,
        "playerName" → "player_name", "Pos" → "position", "Ht" → "height",
        etc.
    """
    dict_for_renaming_columns = {
        "playerName": "player_name",
        "From": "from ",
        "To": "to ",
        "Pos": "position",
        "Ht": "height",
        "Wt": "weight",
        "birthDate": "birth_date",
        "Colleges": "colleges"
    }
    playerinfo = playerinfo.rename(columns=dict_for_renaming_columns)

    return playerinfo


def remove_missing_values(playerinfo: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows with missing critical player information from the DataFrame.

    Specifically, rows with missing values in the "weight" or "birth_date"
    columns are dropped to ensure data completeness.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player information.

    Returns:
        pd.DataFrame: A new DataFrame with rows containing null values in
        "weight" or "birth_date" removed.
    """
    # Remove rows with null values from the weight column
    playerinfo = playerinfo.dropna(subset=["weight"])

    # remove rows with null values from the height column
    playerinfo = playerinfo.dropna(subset=["birth_date"])

    return playerinfo


def change_position_values(playerinfo: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the values in the 'position' column of the player
    information DataFrame.

    This function replaces abbreviated or combined position codes with
    more readable, descriptive strings using a predefined mapping.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player information
            with a 'position' column.

    Returns:
        pd.DataFrame: A new DataFrame with updated 'position' values.
    """
    # Create a map to change the values in the position column
    mapping_dict = {
        "F-C": "Forward, Center",
        "C-F": "Center, Forward",
        "C": "Center",
        "G": "Guard",
        "F": "Forward",
        "G-F": "Guard, Forward",
        "F-G": "Forward, Guard"
    }
    playerinfo["position"] = playerinfo["position"].replace(mapping_dict)

    return playerinfo


def calculate_weight_kg(playerinfo: pd.DataFrame) -> pd.DataFrame:
    """
    Convert player weights from pounds to kilograms and add a new column.
    This function calculates the weight of each player in kilograms using the
    conversion factor (1 lb = 0.45359237 kg) and rounds the result to
    one decimal place.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player information
            with a 'weight' column in pounds.

    Returns:
        pd.DataFrame: A DataFrame with an additional 'weight_kg' column
        representing player weights in kilograms.
    """
    # Add a new column which calculates the player's weight in kilograms(kg)
    playerinfo["weight_kg"] = (
        playerinfo["weight"] * 0.45359237
    ).round(1)

    return playerinfo


# Function to convert "feet-inches" to metres in height column
def height_to_metres(height_string):
    """
    Convert a height from feet-inches format to metres.

    This function takes a string representing height in the format
    'feet-inches' (e.g., '6-2'), converts it to total inches, then
    converts that to metres and rounds the result to 2 decimal places.
    If the input format is invalid, it returns None.

    Args:
        height_string (str): Height string in 'feet-inches' format.

    Returns:
        float or None: Height in metres rounded to 2 decimal places, or None
        if the input is invalid.
    """
    try:
        # Save the feet and inches values in a list
        feet, inches = map(int, height_string.split("-"))
        # Find the total value of inches
        total_inches = feet * 12 + inches
        # Convert to metres rounded to 2 decimal places
        return round(total_inches * 0.0254, 2)
    except Exception:
        return None


def calculate_height_m(playerinfo: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate players' height in metres and add it as a new column.
    This function applies the `height_to_metres` conversion function to the
    'height' column of the DataFrame, which contains heights in feet-inches
    format (e.g., '6-2'), and creates a new column 'height_m' with the values
    in metres.

    Args:
        playerinfo (pd.DataFrame): DataFrame containing player information
        including a 'height' column in feet-inches format.

    Returns:
        pd.DataFrame: Updated DataFrame with an additional 'height_m' column
        containing height values in metres.
    """
    # Create the new column
    playerinfo["height_m"] = playerinfo["height"].apply(height_to_metres)

    return playerinfo
