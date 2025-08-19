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
    games = games[(games["isRegular"] == 1)]
    return games


def remove_unnecessary_columns(games: pd.DataFrame) -> pd.DataFrame:
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
    # Change date_time to datetime object
    games["date_time"] = pd.to_datetime(games["date_time"])

    # Change the format to DD-MM-YYYY
    games["date_time"] = games["date_time"].dt.strftime("%d-%m-%Y")

    return games


def filter_2016_to_2020(games: pd.DataFrame) -> pd.DataFrame:
    # Change date_time to datetime object
    games["date_time"] = pd.to_datetime(games["date_time"], format="%Y-%m-%d")
    # Filter only dates between 2015 and 2019
    games_filtered = games[
        (games["date_time"].dt.year >= 2016)
        & (games["date_time"].dt.year <= 2020)
    ]

    return games_filtered


def add_year_column(games: pd.DataFrame) -> pd.DataFrame:
    games["date_time"] = pd.to_datetime(
        games["date_time"],
        format='%d-%m-%Y',
        errors='coerce'
    )
    games["year"] = games["date_time"].dt.year

    return games
