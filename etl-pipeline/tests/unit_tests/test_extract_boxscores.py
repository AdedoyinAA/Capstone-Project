import pandas as pd
import pytest
from unittest.mock import patch
from src.extract.extract_boxscores import (
    KaggleDownloadError,
    KaggleConnectionError,
    extract_boxscores_csv,
    extract_boxscores,
    TYPE,
    FILE_PATH,
    EXPECTED_PERFORMANCE
)
import logging


@pytest.fixture
def mock_log_extract_success(mocker):
    return mocker.patch("src.extract.extract_boxscores.log_extract_success")


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.extract.extract_boxscores.logger")


def test_extract_boxscores_csv_to_dataframe(mocker):
    mock_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "teamName": ["Los Clippers Clippers",
                         "Sacramento Kings",
                         "Golden State Warriors"]
        }
    )
    mocker.patch(
        "src.extract.extract_boxscores.pd.read_csv", return_value=mock_df
    )

    df = extract_boxscores()

    assert isinstance(df, pd.DataFrame)
    pd.testing.assert_frame_equal(df, mock_df)


def test_log_extract_success_boxscores(
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
        "src.extract.extract_boxscores.pd.read_csv", return_value=mock_df
    )

    mock_start_time = 100.0
    mock_end_time = 100.5
    mocker.patch(
        "src.extract.extract_boxscores.timeit.default_timer",
        side_effect=[mock_start_time, mock_end_time],
    )

    df = extract_boxscores()

    mock_log_extract_success.assert_called_once_with(
        mock_logger, TYPE, df.shape, mock_execution_time, EXPECTED_PERFORMANCE
    )


def test_log_boxscores_error(mocker, mock_logger):
    # Mock pd.read_csv to raise an exception
    mocker.patch(
        "src.extract.extract_boxscores.pd.read_csv",
        side_effect=Exception(f"Failed to load CSV file: {FILE_PATH}"),
    )

    # Call the function and assert exception
    with pytest.raises(
        Exception, match=f"Failed to load CSV file: {FILE_PATH}"
    ):
        extract_boxscores()

    # Verify that the error was logged
    mock_logger.error.assert_called_once_with(
        f"Error loading {FILE_PATH}: Failed to load CSV file: {FILE_PATH}"
    )


@patch("src.extract.extract_boxscores.check_kaggle_credentials",
       side_effect=KaggleConnectionError("No creds"))
def test_extract_boxscores_csv_connection_error(mock_check, caplog):
    with caplog.at_level(logging.ERROR):
        extract_boxscores_csv()
    assert "Connection failed: No creds" in caplog.text
    mock_check.assert_called_once()


@patch("src.extract.extract_boxscores.check_kaggle_credentials")
@patch("src.extract.extract_boxscores.download_nba_dataset_from_kaggle",
       side_effect=KaggleDownloadError("Download failed"))
def test_extract_boxscores_csv_download_error(mock_download,
                                              mock_check,
                                              caplog):
    with caplog.at_level(logging.ERROR):
        extract_boxscores_csv()

    assert "Download failed: Download failed" in caplog.text
    mock_check.assert_called_once()
    mock_download.assert_called_once()
