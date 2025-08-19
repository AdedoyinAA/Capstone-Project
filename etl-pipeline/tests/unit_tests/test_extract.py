import pytest
import pandas as pd
from scripts.run_etl import main


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("scripts.run_etl.logger")


@pytest.fixture
def mock_setup_env(mocker):
    return mocker.patch("scripts.run_etl.setup_env")


@pytest.fixture
def mock_extract_data(mocker):
    mock_data = (
        pd.DataFrame({"id": [1, 2]}),
        pd.DataFrame({"name": ["Alice", "Bob"]}),
    )
    return mocker.patch("scripts.run_etl.extract_data", return_value=mock_data)


def test_main_handles_extraction_error(mock_logger, mock_setup_env, mocker):
    """Test ETL pipeline handles extraction errors"""
    mocker.patch(
        "scripts.run_etl.extract_data", side_effect=Exception("Extract failed")
    )

    with pytest.raises(SystemExit):
        main()

    mock_logger.error.assert_called_once_with(
        "ETL pipeline failed: Extract failed"
    )
