import pandas as pd
import pytest
from src.extract.extract_games import (
    extract_games,
    TYPE,
    FILE_PATH,
    EXPECTED_PERFORMANCE
)


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch("src.extract.extract_games.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.extract.extract_games.logger")


def test_extract_games_csv_to_dataframe(mocker):
    mock_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "teamName": ["Los Clippers Clippers",
                         "Sacramento Kings",
                         "Golden State Warriors"]
        }
    )
    mocker.patch(
        "src.extract.extract_games.pd.read_csv", return_value=mock_df
    )

    df = extract_games()

    assert isinstance(df, pd.DataFrame)
    pd.testing.assert_frame_equal(df, mock_df)


def test_log_extract_success_games(
    mocker, mock_log_extract_success, mock_logger
):
    mock_execution_time = 0.5
    mock_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "teamName": ["Los Clippers Clippers",
                         "Sacramento Kings",
                         "Golden State Warriors"]
        }
    )

    mocker.patch(
        "src.extract.extract_games.pd.read_csv", return_value=mock_df
    )

    mock_start_time = 100.0
    mock_end_time = 100.5
    mocker.patch(
        "src.extract.extract_games.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time],
    )

    df = extract_games()

    mock_log_extract_success.assert_called_once_with(
        mock_logger, TYPE, df.shape, mock_execution_time, EXPECTED_PERFORMANCE
    )


def test_log_games_error(mocker, mock_logger):
    # Mock pd.read_csv to raise an exception
    mocker.patch(
        "src.extract.extract_games.pd.read_csv",
        side_effect=Exception(f"Failed to load CSV file: {FILE_PATH}"),
    )

    # Call the function and assert exception
    with pytest.raises(
        Exception, match=f"Failed to load CSV file: {FILE_PATH}"
    ):
        extract_games()

    # Verify that the error was logged
    mock_logger.error.assert_called_once_with(
        f"Error loading {FILE_PATH}: Failed to load CSV file: {FILE_PATH}"
    )
