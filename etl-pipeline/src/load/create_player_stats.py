import pandas as pd

from sqlalchemy import Connection, text
from config.db_config import load_db_config, DatabaseConfigError
from src.utils.database_utils import (
    get_db_connection,
    DatabaseConnectionError,
    QueryExecutionError
)
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")

TABLE_NAME = "aa_player_stats"


def log_table_action(connection: Connection, table_name: str) -> bool:
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


def create_player_stats(player_stats: pd.DataFrame) -> None:
    # Function to load player_stats into pagila database
    if player_stats.empty:
        logger.warning("No data to load, DataFrame is empty.")
        return

    connection: Connection | None = None
    try:
        # Get a connection to the pagila database
        connection_details = load_db_config()["target_database"]
        connection = get_db_connection(connection_details)

        # Check if table exists
        table_exists = log_table_action(connection, TABLE_NAME)

        # Load player_stats into pagila
        player_stats.to_sql(
            TABLE_NAME,
            con=connection,
            schema="de_2506_a",
            if_exists="replace",
            index=False
        )

        action = "replaced with" if table_exists else "created and loaded into"
        logger.info(f"Data successfully {action} {TABLE_NAME} table.")

        connection.commit()

    except DatabaseConfigError as e:
        logger.error(f"Target database not configured correctly: {e}")
        raise QueryExecutionError(f"Database configuration error: {e}")
    except DatabaseConnectionError as e:
        logger.error(
            "Failed to connect to the database"
            " when creating player stats table:"
            f" {e}"
        )
        raise QueryExecutionError(f"Database connection failed: {e}")
    except pd.errors.DatabaseError as e:
        logger.error(f"Failed to create player stats table: {e}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
    finally:
        if connection and hasattr(connection, "close"):
            connection.close()
