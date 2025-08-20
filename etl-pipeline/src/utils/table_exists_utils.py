from sqlalchemy import Connection, text
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")


def log_table_action(connection: Connection, table_name: str) -> bool:
    """
    Check if a table exists in the connected database and log the action.
    Executes a query against `information_schema.tables` to determine if
    the specified table already exists in the database.
    Logs whether the table will be replaced (if it exists) or created
    (if it does not exist).

    Args:
        connection (Connection): Active SQLAlchemy database connection.
        table_name (str): The name of the table to check.

    Returns:
        table_exists (bool): True if the table exists, False otherwise.
    """
    # Checks if the table exists or not
    result = connection.execute(
        text(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE"
            " table_name = :table_name)"
        ),
        {"table_name": table_name}
    ).scalar()

    table_exists = bool(result) if result is not None else False

    if table_exists:
        logger.info(f"Replacing data in {table_name} table...")
    else:
        logger.info(f"Creating new {table_name} table...")

    return table_exists
