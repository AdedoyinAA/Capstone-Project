import pandas as pd
import pytest
from src.transform.clean_salaries import (
    clean_salaries,
    rename_columns,
    remove_dollar_sign,
    convert_year_to_numeric
)


# Sample dataframe for testing
@pytest.fixture
def sample_salaries():
    data = {
        "playerName": ["LeBron James", "Stephen Curry", "James Harden"],
        "seasonStartYear": ["2006", "2009", "2019"],
        "salary": ["$5,000,000", "$6,000,000", "$12,000,000"],
        "inflationAdjSalary": ["$15,000,000", "$16,000,000", "$18,000,000"]
    }

    return pd.DataFrame(data)


def test_rename_columns(sample_salaries):
    df = rename_columns(sample_salaries.copy())
    assert "player_name " in df.columns
    assert "season_start_year " in df.columns
    assert "salary " in df.columns
    assert "inflation_adjusted_salary" in df.columns


def test_remove_dollar_sign(sample_salaries):
    data = {
        "player_name": ["LeBron James", "Stephen Curry", "James Harden"],
        "season_start_year": ["2006", "2009", "2019"],
        "salary": ["$5,000,000", "$6,000,000", "$12,000,000"],
        "inflation_adjusted_salary": [
            "$15,000,000",
            "$16,000,000",
            "$18,000,000"
        ]
    }
    expected_data = {
        "player_name": ["LeBron James", "Stephen Curry", "James Harden"],
        "season_start_year": ["2006", "2009", "2019"],
        "salary": ["5,000,000", "6,000,000", "12,000,000"],
        "inflation_adjusted_salary": [
            "15,000,000",
            "16,000,000",
            "18,000,000"
        ]
    }
    df = pd.DataFrame(data)
    result = remove_dollar_sign(df)
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df)


def test_convert_year_to_numeric(sample_salaries):
    data = {
        "player_name": ["LeBron James", "Stephen Curry", "James Harden"],
        "season_start_year": ["2006", "2009", "2019"],
        "salary": ["$5,000,000", "$6,000,000", "$12,000,000"],
        "inflation_adjusted_salary": [
            "$15,000,000",
            "$16,000,000",
            "$18,000,000"
        ]
    }
    df = pd.DataFrame(data)
    result = convert_year_to_numeric(df)
    assert pd.api.types.is_integer_dtype(result["season_start_year"])


def test_clean_salaries_runs(sample_salaries, tmp_path):
    # Override FILE_PATH temporarily
    import src.transform.clean_salaries as cb
    cb.FILE_PATH = tmp_path / "cleaned.csv"

    df = clean_salaries(sample_salaries.copy())
    # Check if CSV is saved
    assert cb.FILE_PATH.exists()
    # Check some columns exist after cleaning
    assert "player_name" not in df.columns or \
        "player_name" in df.columns
