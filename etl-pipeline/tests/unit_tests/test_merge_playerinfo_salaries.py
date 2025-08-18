import pandas as pd
import pytest
from src.transform.merge_playerinfo_salaries import merge_playerinfo_salaries


# Sample player info dataframe for testing
@pytest.fixture
def sample_playerinfo():
    data = {
        "player_name": ["LeBron James", "Stephen Curry"],
        "position": ["Forward, Guard", "Guard"],
        "height": ["6-9", "6-2"],
        "weight": [250.0, 185.0],
        "birth_date": ["December 30, 1984", "March 14, 1988"],
        "weight_kg": [113.4, 83.9],
        "height_m": [2.08, 1.88]
    }

    return pd.DataFrame(data)


# Sample salaries dataframe for testing
@pytest.fixture
def sample_salaries():
    data = {
        "player_name": ["LeBron James", "Stephen Curry"],
        "season_start_year": [2016, 2015],
        "salary": ["30,963,450", "11,370,786"],
        "inflation_adjusted_salary": ["34,904,635", "12,945,956"]
    }

    return pd.DataFrame(data)


def test_merge_player_info_salaries(sample_playerinfo, sample_salaries):
    merged = merge_playerinfo_salaries(
        sample_playerinfo.copy(),
        sample_salaries.copy()
    )

    # Check for correct columns
    expected_columns = set([
        "player_name",
        "position",
        "height",
        "weight",
        "birth_date",
        "weight_kg",
        "height_m",
        "season_start_year",
        "salary",
        "inflation_adjusted_salary"
    ])
    assert expected_columns.issubset(merged.columns), "Columns mismatch"

    # Check that the merge worked correctly
    assert (
        merged.loc[
            merged["player_name"] == "LeBron James", "salary"]
        .values[0] == "30,963,450"
    )
    assert (
        merged.loc[
            merged["player_name"] == "Stephen Curry", "salary"]
        .values[0] == "11,370,786"
    )
