import pandas as pd

FILE_PATH = "data/processed/cleaned_games.csv"


def clean_games(games: pd.DataFrame) -> pd.DataFrame:
    # Remove unnecessary columns
    games = remove_unnecessary_columns(games)
    # Rename columns
    games = rename_columns(games)
    # Trim whitespaces
    games = trim_whitespaces(games)
    # Change date format to DD-MM-YYY
    games = change_date_format(games)
    # Keep only games from 2015 2019
    games = filter_2015_to_2019(games)

    # Save the cleaned dataframe as a CSV
    games.to_csv(FILE_PATH, index=False)
    return games


def remove_unnecessary_columns(games: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = ["attendance", "notes", "startET", "isRegular"]
    games.drop(
        columns=columns_to_drop,
        inplace=True
    )
    return games


def rename_columns(games: pd.DataFrame) -> pd.DataFrame:
    dict_for_renaming_columns = {
        "seasonStartYear": "season_start_year ",
        "awayTeam": "away_team ",
        "pointsAway": "points_away ",
        "homeTeam": "home_team",
        "pointsHome": "points_home ",
        "datetime": "date_time"
    }
    games = games.rename(columns=dict_for_renaming_columns)

    return games


def trim_whitespaces(games: pd.DataFrame) -> pd.DataFrame:
    # Trim leading and trailing whitespaces in column names
    games.columns = games.columns.str.strip()

    # Trim leading and trailing whitespaces in rows
    games[games.select_dtypes(include="string").columns] = (
        games.select_dtypes(
            include="string").apply(lambda x: x.str.strip())
    )

    return games


def change_date_format(games: pd.DataFrame) -> pd.DataFrame:
    # Change date_time to datetime object
    games["date_time"] = pd.to_datetime(games["date_time"], format="%Y-%m-%d")

    # Change the format to DD-MM-YYYY
    games["date_time"] = games["date_time"].dt.strftime("%d-%m-%Y")

    return games


def filter_2015_to_2019(games: pd.DataFrame) -> pd.DataFrame:
    # Filter only dates between 2014 and 2019
    games_filtered = games[
        (games["season_start_year"] >= 2015) &
        (games["season_start_year"] <= 2019)]

    return games_filtered
