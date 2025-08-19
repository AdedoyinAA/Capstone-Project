import pandas as pd
from src.load.load_team_stats import load_team_stats


def test_load_team_stats_with_none(monkeypatch, caplog):
    # Test None passed as argument
    called = {"create": False}

    def mock_create_team_stats(df):
        called["create"] = True

    monkeypatch.setattr(
        "src.load.load_team_stats.create_team_stats",
        mock_create_team_stats
    )

    caplog.set_level("WARNING")

    load_team_stats(None)

    assert not called["create"]
    assert "No data to load" in caplog.text


def test_load_team_stats_with_data(monkeypatch, caplog):
    # Test load success
    called = {"create": False}

    def mock_create_team_stats(df):
        called["create"] = True
        assert "col1" in df.columns

    monkeypatch.setattr(
        "src.load.load_team_stats.create_team_stats",
        mock_create_team_stats
    )

    caplog.set_level("INFO")

    df = pd.DataFrame({"col1": [1, 2, 3]})
    load_team_stats(df)

    assert called["create"]
    assert "Starting data load process" in caplog.text
    assert (
        "Team Stats Data load process completed successfully" in caplog.text
    )
