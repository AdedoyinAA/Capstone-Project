import pandas as pd
from src.load.load_player_info_and_salaries import (
    load_player_info_and_salaries
)


def test_load_player_info_and_salaries_with_none(monkeypatch, caplog):
    # Test None passed as argument
    called = {"create": False}

    def mock_create_player_info_and_salaries(df):
        called["create"] = True

    monkeypatch.setattr(
        "src.load.load_player_stats.create_player_stats",
        mock_create_player_info_and_salaries
    )

    caplog.set_level("WARNING")

    load_player_info_and_salaries(None)

    assert not called["create"]
    assert "No data to load" in caplog.text


def test_load_player_info_and_salaries_with_data(monkeypatch, caplog):
    # Test load success
    called = {"create": False}

    def mock_create_player_info_and_salaries(df):
        called["create"] = True
        assert "col1" in df.columns

    monkeypatch.setattr(
        "src.load.load_player_info_and_salaries"
        ".create_player_info_and_salaries",
        mock_create_player_info_and_salaries
    )

    caplog.set_level("INFO")

    df = pd.DataFrame({"col1": [1, 2, 3]})
    load_player_info_and_salaries(df)

    assert called["create"]
    assert "Starting data load process" in caplog.text
    assert (
        "Player Information and Salaries Data "
        "load process completed successfully" in caplog.text
    )
