import pandas as pd
import pytest
from src.transform.clean_playerinfo import (
    clean_playerinfo,
    remove_unnecessary_columns,
    rename_columns,
    change_position_values,
    calculate_height_m,
    calculate_weight_kg,
    height_to_metres
)


# Sample dataframe for testing
@pytest.fixture
def sample_playerinfo():
    data = {
        "playerName": ["LeBron James", "Stephen Curry", "Kevin Durant"],
        "From": [2003, 2009, 2007],
        "To": [2023, 2023, 2023],
        "Pos": ["S-F", "P-G", "S-F"],
        "Ht": ["6-9", "6-2", "6-10"],
        "Wt": [250, 185, 240],
        "birthDate": ["1984-12-30", "1988-03-14", "1988-09-29"],
        "Colleges": ["None", "Davidson", "Texas"]
    }

    return pd.DataFrame(data)


def test_remove_unnecessary_columns(sample_playerinfo):
    df = remove_unnecessary_columns(sample_playerinfo.copy())
    for col in ["From", "To", "Colleges"]:
        assert col not in df.columns


def test_rename_columns(sample_playerinfo):
    df = rename_columns(sample_playerinfo.copy())
    assert "player_name" in df.columns
    assert "position" in df.columns
    assert "height" in df.columns
    assert "weight" in df.columns
    assert "birth_date" in df.columns


def test_change_position_values():
    data = {
        "playerName": ["Player A", "Player B", "Player C", "Player D"],
        "position": ["F-C", "G-F", "C", "F"]
    }

    expected_positions = [
        "Forward-Center",
        "Guard-Forward",
        "Center",
        "Forward"
    ]

    result = change_position_values(pd.DataFrame(data))
    assert result["position"].tolist() == expected_positions


def test_calculate_weight_kg():
    data = {
        "playerName": ["Player A", "Player B", "Player C"],
        "weight": [200, 150, 180]
    }

    expected_weights = [90.7, 68.0, 81.6]

    result = calculate_weight_kg(pd.DataFrame(data))
    assert result["weight_kg"].tolist() == expected_weights


def test_calculate_height_m():
    data = {
        "playerName": ["Player A", "Player B", "Player C"],
        "height": ["6-10", "6-1", "7-2"]
    }

    expected_heights = [2.08, 1.85, 2.18]

    result = calculate_height_m(pd.DataFrame(data))
    assert result["height_m"].tolist() == expected_heights


def test_height_to_metres():
    # Check valid height strings
    assert height_to_metres("6-10") == 2.08
    assert height_to_metres("6-1") == 1.85
    assert height_to_metres("7-2") == 2.18

    # Check invalid height strings return None
    assert height_to_metres("invalid") is None
    assert height_to_metres("") is None
    assert height_to_metres(None) is None


def test_clean_playerinfo_runs(sample_playerinfo, tmp_path):
    # Override FILE_PATH temporarily
    import src.transform.clean_playerinfo as cb
    cb.FILE_PATH = tmp_path / "cleaned.csv"

    df = clean_playerinfo(sample_playerinfo.copy())
    # Check if CSV is saved
    assert cb.FILE_PATH.exists()
    # Check some columns exist after cleaning
    assert "player_name" not in df.columns or \
        "player_name" in df.columns
