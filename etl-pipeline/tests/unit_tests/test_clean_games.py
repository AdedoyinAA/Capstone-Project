import pandas as pd
import pytest
from src.transform.clean_games import (
    clean_games,
    rename_columns,
    remove_unnecessary_columns,
    filter_out_only_regular_season_games,
    filter_2015_to_2019,
    trim_whitespaces,
    change_date_format
)


# Sample dataframe for testing
@pytest.fixture
def sample_games():
    data = {
        "seasonStartYear": [2015, 1999],
        "awayTeam": ["Los Angeles Lakers", "Golden State Warriors"],
        "pointsAway": [100, 89],
        "homeTeam": ["Golden State Warriors", "Los Angeles Lakers"],
        "pointsHome": [100, 99],
        "attendance": [16287, 20000],
        "notes": ["at Tokyo, Japan", "at Los Angeles, America"],
        "startET": ["7:30p", "10:30p"],
        "datetime": ["01/11/2015", "01/12/1999"],
        "isRegular": [1, 0],
        "game_id": [25000, 26000]
    }
    return pd.DataFrame(data)


def test_remove_unnecessary_columns(sample_games):
    df = remove_unnecessary_columns(sample_games.copy())
    for col in ["attendance", "notes", "startET", "isRegular"]:
        assert col not in df.columns


def test_trim_whitespaces():
    df = pd.DataFrame({" notes ": [" at Tokyo, Japan "]}, dtype="string")
    df = trim_whitespaces(df)
    assert df.columns[0] == "notes"
    assert df.loc[0, "notes"] == "at Tokyo, Japan"


def test_rename_columns(sample_games):
    df = rename_columns(sample_games.copy())
    assert "season_start_year " in df.columns
    assert "away_team " in df.columns
    assert "points_away " in df.columns
    assert "home_team" in df.columns
    assert "points_home " in df.columns
    assert "date_time" in df.columns


def test_filter_out_reg_season_games(sample_games):
    expected_data = {
        "seasonStartYear": [2015],
        "awayTeam": ["Los Angeles Lakers"],
        "pointsAway": [100],
        "homeTeam": ["Golden State Warriors"],
        "pointsHome": [100],
        "attendance": [16287],
        "notes": ["at Tokyo, Japan"],
        "startET": ["7:30p"],
        "datetime": ["01/11/2015"],
        "isRegular": [1],
        "game_id": [25000]
    }
    df = filter_out_only_regular_season_games(sample_games.copy())
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(df.reset_index(drop=True), expected_df)


def test_filter_2015_to_2019():
    data = {
        "season_start_year": [2015, 1999],
        "away_team": ["Los Angeles Lakers", "Golden State Warriors"],
        "points_away": [100, 89],
        "home_team": ["Golden State Warriors", "Los Angeles Lakers"],
        "points_home": [100, 99],
        "date_time": ["01/11/2015", "01/12/1999"],
        "game_id": [25000, 26000]
    }
    expected_data = {
        "season_start_year": [2015],
        "away_team": ["Los Angeles Lakers"],
        "points_away": [100],
        "home_team": ["Golden State Warriors"],
        "points_home": [100],
        "date_time": ["01/11/2015"],
        "game_id": [25000]
    }
    df = pd.DataFrame(data)
    result = filter_2015_to_2019(df)
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)


def test_change_date_format():
    data = {
        "game_id": [1, 2, 3],
        "date_time": ["2015-01-15", "2016-12-30", "2019-07-04"]
    }
    df = pd.DataFrame(data)

    result = change_date_format(df)

    expected_dates = ["15-01-2015", "30-12-2016", "04-07-2019"]

    assert list(result["date_time"]) == expected_dates
    assert result["date_time"].dtype == object


def test_clean_games_runs(sample_games, tmp_path):
    # Override FILE_PATH temporarily
    import src.transform.clean_games as cb
    cb.FILE_PATH = tmp_path / "cleaned.csv"

    df = clean_games(sample_games.copy())
    # Check if CSV is saved
    assert cb.FILE_PATH.exists()
    # Check some columns exist after cleaning
    assert "game_id" not in df.columns or \
        "game_id" in df.columns
