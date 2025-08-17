import pytest
import pandas as pd
from scripts.run_etl import main


@pytest.fixture
def sample_data():
    # Mock dataframes
    df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    df2 = pd.DataFrame({"game_id": [10, 20], "isRegular": [1, 0]})
    df3 = pd.DataFrame({"c": [5, 6], "d": [7, 8]})
    df4 = pd.DataFrame({"salary": ["$1000", "$2000"], "player": ["A", "B"]})
    return [df1, df2, df3, df4]


@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("scripts.run_etl.logger")


@pytest.fixture
def mock_setup_env(mocker):
    return mocker.patch("scripts.run_etl.setup_env")


@pytest.fixture
def mock_transform_data(mocker):
    mock_data = (
        pd.DataFrame({"id": [1, 2]}),
        pd.DataFrame({"name": ["Alice", "Bob"]}),
    )
    return mocker.patch(
        "scripts.run_etl.transform_data",
        return_value=mock_data
    )


def test_main_handles_transformation_error(
    mock_logger,
    mock_setup_env,
    mocker
):
    """Test ETL Pipeline handles transformation errors"""
    mocker.patch(
        "scripts.run_etl.transform_data",
        side_effect=Exception("Transformation failed")
    )

    with pytest.raises(SystemExit):
        main()

    mock_logger.error.assert_called_once_with(
        "ETL pipeline failed: Transformation failed"
    )
