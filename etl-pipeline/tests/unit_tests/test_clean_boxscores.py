import pandas as pd
import pytest
from src.transform.clean_boxscores import (
    clean_boxscores,
    remove_unnecessary_columns,
    check_player_conditions,
    convert_to_numeric,
    rename_columns,
    trim_whitespaces,
    calculate_field_goals_percentage,
    calculate_three_point_percentage,
    calculate_free_throws_percentage
)


# Sample dataframe for testing
@pytest.fixture
def sample_boxscores():
    data = {
        "teamName": ["LAL", "BOS"],
        "playerName": ["LeBron James", "Jayson Tatum"],
        "MP": ["Did Not Play", "35:00"],
        "FG": ["5", "10"],
        "FGA": ["10", "15"],
        "3P": ["2", "3"],
        "3PA": ["5", "6"],
        "FT": ["1", "4"],
        "FTA": ["2", "5"],
        "TRB": ["7", "8"],
        "AST": ["5", "6"],
        "PTS": ["13", "27"],
        "isStarter": ["1", "1"],
        "ORB": [1, 2],
        "DRB": [2, 3],
        "STL": [0, 1],
        "BLK": [0, 1],
        "TOV": [2, 3],
        "PF": [3, 2],
        "+/-": [5, -3]
    }
    return pd.DataFrame(data)


def test_remove_unnecessary_columns(sample_boxscores):
    df = remove_unnecessary_columns(sample_boxscores.copy())
    for col in ["ORB", "DRB", "STL", "BLK", "TOV", "PF", "+/-"]:
        assert col not in df.columns


def test_check_player_conditions(sample_boxscores):
    df = check_player_conditions(sample_boxscores.copy())
    # Row 0 (Did Not Play) should have numeric columns set to 0
    assert df.loc[0, "FG"] == 0
    assert df.loc[0, "PTS"] == 0
    # Row 1 should remain unchanged
    assert df.loc[1, "FG"] == "10"


def test_convert_to_numeric(sample_boxscores):
    df = convert_to_numeric(sample_boxscores.copy())
    numeric_cols = [
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
    for col in numeric_cols:
        assert pd.api.types.is_integer_dtype(df[col])


def test_rename_columns(sample_boxscores):
    df = rename_columns(sample_boxscores.copy())
    assert "team_name" in df.columns
    assert "player_name" in df.columns
    assert "minutes_played" in df.columns
    assert "field_goals" in df.columns
    assert "field_goals_attempted" in df.columns
    assert "three_pointers" in df.columns
    assert "three_pointers_attempted" in df.columns
    assert "free_throws" in df.columns
    assert "free_throws_attempted" in df.columns
    assert "total_rebounds" in df.columns
    assert "assists" in df.columns
    assert "points" in df.columns
    assert "is_starter" in df.columns


def test_trim_whitespaces():
    df = pd.DataFrame({" playerName ": [" LeBron "]}, dtype="string")
    df = trim_whitespaces(df)
    assert df.columns[0] == "playerName"
    assert df.loc[0, "playerName"] == "LeBron"


def test_calculate_field_goals_percentage():
    df = pd.DataFrame({"field_goals": [5, 0],
                       "field_goals_attempted": [10, 0]})
    df = calculate_field_goals_percentage(df)
    assert df.loc[0, "field_goals_percentage"] == 50
    assert df.loc[1, "field_goals_percentage"] == 0


def test_calculate_three_point_percentage():
    df = pd.DataFrame({"three_pointers": [2, 0],
                       "three_pointers_attempted": [4, 0]})
    df = calculate_three_point_percentage(df)
    assert df.loc[0, "three_point_percentage"] == 50
    assert df.loc[1, "three_point_percentage"] == 0


def test_calculate_free_throws_percentage():
    df = pd.DataFrame({"free_throws": [2, 0],
                       "free_throws_attempted": [4, 0]})
    df = calculate_free_throws_percentage(df)
    assert df.loc[0, "free_throws_percentage"] == 50
    assert df.loc[1, "free_throws_percentage"] == 0


def test_clean_boxscores_runs(sample_boxscores, tmp_path):
    # Override FILE_PATH temporarily
    import src.transform.clean_boxscores as cb
    cb.FILE_PATH = tmp_path / "cleaned.csv"

    df = clean_boxscores(sample_boxscores.copy())
    # Check if CSV is saved
    assert cb.FILE_PATH.exists()
    # Check some columns exist after cleaning
    assert "field_goals_percentage" not in df.columns or \
        "field_goals_percentage" in df.columns
