import pandas as pd

FILE_PATH = "data/processed/cleaned_boxscores.csv"


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

    # Save the cleaned dataframe as a CSV
    boxscores.to_csv(FILE_PATH, index=False)
    return boxscores


def remove_unnecessary_columns(boxcores: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = ["ORB", "DRB", "STL", "BLK", "TOV", "PF", "+/-"]
    boxcores.drop(
        columns=columns_to_drop,
        inplace=True
    )
    return boxcores


def check_player_conditions(boxscores: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        "Did Not Play",
        "Player Suspended",
        "Not With Team",
        "Did Not Dress"
    ]

    # Find rows where minutes_played == "Did Not Play" or "Player Suspended"
    mask = boxscores["MP"].isin(conditions)

    # Replace the values with 0 where the mask returns True
    columns_to_replace = [
        "FG",
        "FGA",
        "3P",
        "3PA",
        "FT",
        "FTA",
        "TRB",
        "AST",
        "PTS"
    ]
    boxscores.loc[mask, columns_to_replace] = 0
    return boxscores


def convert_to_numeric(boxscores: pd.DataFrame) -> pd.DataFrame:
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


def trim_whitespaces(boxscores: pd.DataFrame) -> pd.DataFrame:
    # Trim leading and trailing whitespaces in column names
    boxscores.columns = boxscores.columns.str.strip()

    # Trim leading and trailing whitespaces in rows
    boxscores[boxscores.select_dtypes(include="string").columns] = (
        boxscores.select_dtypes(
            include="string").apply(lambda x: x.str.strip())
    )

    return boxscores


def calculate_field_goals_percentage(boxscores: pd.DataFrame) -> pd.DataFrame:
    # Add a new column which calculates the field goals percentage
    boxscores["field_goals_percentage_%"] = (
        boxscores["field_goals"] / boxscores["field_goals_attempted"] * 100
    ).round(2)

    # Change NaN values to 0
    boxscores.loc[boxscores[
        "field_goals_attempted"] == 0,
        "field_goals_percentage_%"] = 0

    return boxscores


def calculate_three_point_percentage(boxscores: pd.DataFrame) -> pd.DataFrame:
    # Add a new column which calculates the three pointers percentage
    boxscores["three_point_percentage_%"] = (
        (boxscores["three_pointers"]
         / boxscores["three_pointers_attempted"]
         * 100)
    ).round(2)

    # Change NaN values to 0
    boxscores.loc[boxscores[
        "three_pointers_attempted"] == 0,
        "three_point_percentage_%"] = 0

    return boxscores
