import pandas as pd

from sqlalchemy import Connection
from config.db_config import load_db_config, DatabaseConfigError
from src.utils.database_utils import (
    get_db_connection,
    DatabaseConnectionError,
    QueryExecutionError
)
from src.utils.table_exists_utils import log_table_action
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")

TABLE_NAME = "aa_player_info_and_salaries"


def create_player_info_and_salaries(
    player_info_and_salaries: pd.DataFrame
) -> None:
    # Function to load player info and salaries into pagila database
    if player_info_and_salaries.empty:
        logger.warning("No data to load, DataFrame is empty.")
        return

    connection: Connection | None = None
    try:
        # Get a connection to the pagila database
        connection_details = load_db_config()["target_database"]
        connection = get_db_connection(connection_details)

        # Check if table exists
        table_exists = log_table_action(connection, TABLE_NAME)

        # Load player info and salaries into pagila
        player_info_and_salaries.to_sql(
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
            " when creating player info and salaries table:"
            f" {e}"
        )
        raise QueryExecutionError(f"Database connection failed: {e}")
    except pd.errors.DatabaseError as e:
        logger.error(f"Failed to create player info and salaries table: {e}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
    finally:
        if connection and hasattr(connection, "close"):
            connection.close()
