import pandas as pd
import pytest
from src.transform.merge_boxscores_games import merge_boxscores_games


# Sample boxscores dataframe for testing
@pytest.fixture
def sample_boxscores():
    data = {
        "game_id": [1, 2],
        "team_name": ["Team A", "Team B"],
        "points": [100, 95]
    }

    return pd.DataFrame(data)


# Sample games dataframe for testing
@pytest.fixture
def sample_games():
    data = {
        "game_id": [1, 2],
        "home_team": ["Team A", "Team C"],
        "away_team": ["Team D", "Team B"]
    }
    return pd.DataFrame(data)


def test_merge_boxscores_games(sample_boxscores, sample_games):
    merged = merge_boxscores_games(
        sample_boxscores.copy(),
        sample_games.copy()
    )

    # Check for correct columns
    expected_columns = set([
        "game_id",
        "team_name",
        "points",
        "home_team",
        "away_team"
    ])
    assert expected_columns.issubset(merged.columns), "Columns mismatch"

    # Check that the merge worked correctly
    assert (
        merged.loc[merged['game_id'] == 1, 'team_name'].values[0] == "Team A"
    )
    assert (
        merged.loc[merged['game_id'] == 2, 'home_team'].values[0] == "Team C"
    )
