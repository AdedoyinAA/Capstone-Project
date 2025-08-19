from unittest.mock import Mock, patch
from src.load.create_player_stats import (
    log_table_action,
)


def test_log_table_action_table_exists():
    # Test the logging when the table exists
    mock_connection = Mock()
    mock_result = Mock()
    mock_result.scalar.return_value = True
    mock_connection.execute.return_value = mock_result

    with patch(
        'src.utils.table_exists_utils.logger'
    ) as mock_logger:
        result = log_table_action(mock_connection, "test_table")

    assert result is True
    mock_logger.info.assert_called_once_with(
        "Replacing data in test_table table..."
    )


def test_log_table_action_table_does_not_exist():
    mock_connection = Mock()
    mock_result = Mock()
    mock_result.scalar.return_value = False
    mock_connection.execute.return_value = mock_result

    with patch(
        'src.utils.table_exists_utils.logger'
    ) as mock_logger:
        result = log_table_action(mock_connection, "test_table")

    assert result is False
    mock_logger.info.assert_called_once_with(
        "Creating new test_table table..."
    )
