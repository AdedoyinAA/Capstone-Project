import pandas as pd
from src.transform.transform_merged_boxscores_games import (
    get_player_stats,
    get_team_stats,
    determine_winner
)


# Sample dataframe for testing
def sample_data():
    return pd.DataFrame({
        "game_id": [1, 1, 2, 2],
        "season_start_year": [2015, 2015, 2015, 2015],
        "home_team": ["Team A", "Team A", "Team B", "Team B"],
        "away_team": ["Team B", "Team B", "Team A", "Team A"],
        "team_name": ["Team A", "Team B", "Team B", "Team A"],
        "points_home": [100, 100, 90, 90],
        "points_away": [90, 90, 85, 85],
        "player_name": ["P1", "P2", "P3", "P4"],
        "minutes_played": [30, 28, 35, 32],
        "field_goals": [10, 8, 9, 7],
        "field_goals_attempted": [20, 15, 18, 16],
        "three_pointers": [2, 3, 1, 2],
        "three_pointers_attempted": [6, 7, 5, 6],
        "free_throws": [4, 2, 5, 3],
        "free_throws_attempted": [5, 4, 6, 4],
        "total_rebounds": [8, 6, 7, 5],
        "assists": [5, 7, 6, 4],
        "points": [24, 18, 22, 17],
        "is_starter": [1, 1, 1, 0],
        "field_goals_percentage_%": [0.5, 0.53, 0.5, 0.44],
        "three_point_percentage_%": [0.33, 0.43, 0.2, 0.33],
        "free_throws_percentage_%": [0.8, 0.67, 0.83, 0.75],
    })


def test_get_player_stats():
    df = sample_data()
    result_df = get_player_stats(df)

    # Check that columns exist
    expected_columns = {
        "player_name",
        "season_start_year",
        "points_per_game",
        "assists_per_game",
        "rebounds_per_game",
        "field_goal_%_per_game",
        "three_point_%_per_game",
        "free_throws_%_per_game",
        "total_three_pointers",
    }
    assert expected_columns.issubset(result_df.columns)


def test_get_team_stats(tmp_path):
    df = sample_data()
    result = get_team_stats(df)

    expected_columns = {
        "season_start_year",
        "team_name",
        "total_games",
        "total_wins",
        "total_losses",
        "win_%"
    }
    assert expected_columns.issubset(result.columns)

    # Check win counts and number of games are correct
    team_a = result[result["team_name"] == "Team A"].iloc[0]
    assert team_a["total_wins"] == 1
    assert team_a["total_losses"] == 1
    assert team_a["win_%"] == 50.0
    assert team_a["total_games"] == 2


def test_determine_winner_else():
    # Sample row where team_name is not in home/away
    row = pd.Series({
        "team_name": "Team X",
        "home_team": "Team A",
        "away_team": "Team B",
        "points_home": 100,
        "points_away": 90
    })

    result = determine_winner(row)
    assert result is None
