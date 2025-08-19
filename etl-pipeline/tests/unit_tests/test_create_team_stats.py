import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.load.create_team_stats import (
    create_team_stats,
    TABLE_NAME
)
from config.db_config import DatabaseConfigError
from src.utils.database_utils import (
    DatabaseConnectionError,
    QueryExecutionError
)


# Sample DataFrame for testing
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "season_start_year": [2015, 2016],
        "team_name": ["Atlanta Hawks", "Golden State Warriors"]
    })


# Empty DataFrame for testing
@pytest.fixture
def empty_dataframe():
    return pd.DataFrame()


def test_create_team_stats_empty_df(empty_dataframe):
    with patch(
        "src.load.create_team_stats.logger"
    ) as mock_logger:
        create_team_stats(empty_dataframe)

    mock_logger.warning.assert_called_once_with(
        "No data to load, DataFrame is empty."
    )


@patch("src.load.create_team_stats.log_table_action")
@patch("src.load.create_team_stats.get_db_connection")
@patch("src.load.create_team_stats.load_db_config")
def test_create_team_stats_new_table(
    mock_load_config,
    mock_get_connection,
    mock_log_action,
    sample_dataframe
):
    # Test for successful data load into a new table
    mock_load_config.return_value = {
        "target_database": {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "5432"
        }
    }
    mock_connection = Mock()
    mock_connection.close = Mock()
    mock_get_connection.return_value = mock_connection
    mock_log_action.return_value = False

    with patch.object(sample_dataframe, "to_sql") as mock_to_sql:
        with patch(
            "src.load.create_team_stats.logger"
        ) as mock_logger:
            create_team_stats(sample_dataframe)
    mock_log_action.assert_called_once_with(mock_connection, TABLE_NAME)
    mock_to_sql.assert_called_once_with(
        TABLE_NAME,
        con=mock_connection,
        schema="public",
        if_exists="replace",
        index=False
    )
    # Check that success message was logged
    success_calls = [call for call in mock_logger.info.call_args_list
                     if "Data successfully"
                     " created and loaded into" in str(call)]
    assert len(success_calls) == 1
    mock_connection.close.assert_called_once()


@patch('src.load.create_team_stats.load_db_config')
def test_create_team_stats_database_config_error(
    mock_load_config,
    sample_dataframe
):
    # Test Database configuration error
    mock_load_config.side_effect = DatabaseConfigError("Config error")

    with pytest.raises(
        QueryExecutionError,
        match="Database configuration error"
    ):
        create_team_stats(sample_dataframe)


@patch('src.load.create_team_stats.get_db_connection')
@patch('src.load.create_team_stats.load_db_config')
def test_create_team_stats_connection_error(
    mock_load_config,
    mock_get_connection,
    sample_dataframe
):

    mock_load_config.return_value = {
        "target_database": {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "5432"
        }
    }
    mock_get_connection.side_effect = DatabaseConnectionError(
        "Connection failed"
    )

    with pytest.raises(
            QueryExecutionError,
            match="Database connection failed"
            ):
        create_team_stats(sample_dataframe)


@patch('src.load.create_team_stats.log_table_action')
@patch('src.load.create_team_stats.get_db_connection')
@patch('src.load.create_team_stats.load_db_config')
def test_create_team_stats_database_error(
    mock_load_config,
    mock_get_connection,
    mock_log_action,
    sample_dataframe
):
    # Test pandas database error
    mock_load_config.return_value = {
        "target_database": {
            "dbname": "test_db",
            "user": "test_user",
            "password": "test_pass",
            "host": "localhost",
            "port": "5432"
        }
    }
    mock_connection = Mock()
    mock_connection.close = Mock()
    mock_get_connection.return_value = mock_connection
    mock_log_action.return_value = False

    with patch.object(
        sample_dataframe,
        'to_sql',
        side_effect=pd.errors.DatabaseError("SQL error")
    ):

        with pytest.raises(
            QueryExecutionError,
            match="Failed to execute query"
        ):
            create_team_stats(sample_dataframe)

        mock_connection.close.assert_called_once()
