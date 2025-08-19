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
    columns_to_drop = ["Colleges", "From", "To"]
    playerinfo = playerinfo.drop(columns=columns_to_drop, axis="columns")

    return playerinfo


def rename_columns(playerinfo: pd.DataFrame) -> pd.DataFrame:
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
    # Remove rows with null values from the weight column
    playerinfo = playerinfo.dropna(subset=["weight"])

    # remove rows with null values from the height column
    playerinfo = playerinfo.dropna(subset=["birth_date"])

    return playerinfo


def change_position_values(playerinfo: pd.DataFrame) -> pd.DataFrame:
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
    # Add a new column which calculates the player's weight in kilograms(kg)
    playerinfo["weight_kg"] = (
        playerinfo["weight"] * 0.45359237
    ).round(1)

    return playerinfo


# Function to convert "feet-inches" to metres in height column
def height_to_metres(height_string):
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
    # Create the new column
    playerinfo["height_m"] = playerinfo["height"].apply(height_to_metres)

    return playerinfo
