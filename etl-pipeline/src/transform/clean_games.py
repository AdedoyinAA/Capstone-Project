import pandas as pd
import os
from src.utils.trimming_whitespace_utils import trim_whitespaces

FILE_PATH = "data/processed/cleaned_games.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)


def clean_games(games: pd.DataFrame) -> pd.DataFrame:
    # Keep only regular season games
    games = filter_out_only_regular_season_games(games)
    # Remove unnecessary columns
    games = remove_unnecessary_columns(games)
    # Rename columns
    games = rename_columns(games)
    # Trim whitespaces
    games = trim_whitespaces(games)
    # Keep only games from 2015 to 2019
    games = filter_2016_to_2020(games)
    # Add year column
    games = add_year_column(games)
    # Save the cleaned dataframe as a CSV
    games.to_csv(FILE_PATH, index=False)

    return games


def filter_out_only_regular_season_games(games: pd.DataFrame) -> pd.DataFrame:
    """Filter the DataFrame to include only regular season games.

    This function selects rows where the 'isRegular' column is 1,
    effectively removing any playoff or non-regular season games.

    Args:
        games (pd.DataFrame): The DataFrame containing game data with a column
        'isRegular' indicating whether the game is a regular season game
        (1) or not (0).

    Returns:
        pd.DataFrame: The filtered DataFrame
        containing only regular season games.
    """
    games = games[(games["isRegular"] == 1)]
    return games


def remove_unnecessary_columns(games: pd.DataFrame) -> pd.DataFrame:
    """Remove columns from the games DataFrame
    that are not needed for analysis.

    This function drops columns such as attendance, notes, start time,
    regular season indicator, and season start year to simplify the dataset.

    Args:
        games (pd.DataFrame): The DataFrame containing game data.

    Returns:
        pd.DataFrame: A new DataFrame with the unnecessary columns removed.
    """
    columns_to_drop = [
        "attendance",
        "notes",
        "startET",
        "isRegular",
        "seasonStartYear"
    ]
    new_games = games.drop(
        columns=columns_to_drop,
    )
    return new_games


def rename_columns(games: pd.DataFrame) -> pd.DataFrame:
    """Rename columns in the games DataFrame to
    follow a consistent naming convention.

    This function renames columns such as awayTeam,
    pointsAway, homeTeam, pointsHome, and datetime
    to more descriptive and standardized column names.

    Args:
        games (pd.DataFrame): The DataFrame containing game data.

    Returns:
        pd.DataFrame: A new DataFrame with
        columns renamed for clarity and consistency.
    """
    dict_for_renaming_columns = {
        "awayTeam": "away_team ",
        "pointsAway": "points_away ",
        "homeTeam": "home_team",
        "pointsHome": "points_home ",
        "datetime": "date_time"
    }
    games = games.rename(columns=dict_for_renaming_columns)

    return games


def change_date_format(games: pd.DataFrame) -> pd.DataFrame:
    """Convert the 'date_time' column to a standard DD-MM-YYYY string format.

    This function first ensures that the 'date_time'
    column is a datetime object,then formats it as a string
    in the format "DD-MM-YYYY".

    Args:
        games (pd.DataFrame): The DataFrame containing
        game data with a 'date_time' column.

    Returns:
        pd.DataFrame: A new DataFrame with the 'date_time'
        column formatted as "DD-MM-YYYY".
    """
    # Change date_time to datetime object
    games["date_time"] = pd.to_datetime(games["date_time"])

    # Change the format to DD-MM-YYYY
    games["date_time"] = games["date_time"].dt.strftime("%d-%m-%Y")

    return games


def filter_2016_to_2020(games: pd.DataFrame) -> pd.DataFrame:
    """Filter the games DataFrame to include only games
    between 2016 and 2020 (inclusive).

    This function converts the 'date_time' column to a
    datetime object (if not already), then filters the
    DataFrame to keep only rows where the year is between 2016 and 2020.

    Args:
        games (pd.DataFrame): The DataFrame containing game data
        with a 'date_time' column.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only
        games from 2016 to 2020.
    """
    # Change date_time to datetime object
    games["date_time"] = pd.to_datetime(games["date_time"], format="%Y-%m-%d")
    # Filter only dates between 2015 and 2019
    games_filtered = games[
        (games["date_time"].dt.year >= 2016)
        & (games["date_time"].dt.year <= 2020)
    ]

    return games_filtered


def add_year_column(games: pd.DataFrame) -> pd.DataFrame:
    """Add a 'year' column extracted from the 'date_time'
    column in the games DataFrame.

    This function converts the 'date_time' column to a datetime
    object (format: DD-MM-YYYY), coercing any invalid dates to NaT,
    and then creates a new 'year' column with the year of each game.

    Args:
        games (pd.DataFrame): The DataFrame containing
        game data with a 'date_time' column.

    Returns:
        pd.DataFrame: The DataFrame with an added 'year' column.
    """
    games["date_time"] = pd.to_datetime(
        games["date_time"],
        format='%d-%m-%Y',
        errors='coerce'
    )
    games["year"] = games["date_time"].dt.year

    return games
