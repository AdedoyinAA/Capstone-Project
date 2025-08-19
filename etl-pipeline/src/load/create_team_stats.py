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
from src.utils.schema_utils import set_schema


schema = set_schema()

# Setup the logger
logger = setup_logger("load_data", "load_data.log")

TABLE_NAME = "aa_team_stats"


def create_team_stats(team_stats: pd.DataFrame) -> None:
    # Function to load player_stats into pagila database
    if team_stats.empty:
        logger.warning("No data to load, DataFrame is empty.")
        return

    connection: Connection | None = None
    try:
        # Get a connection to the pagila database
        connection_details = load_db_config()["target_database"]
        connection = get_db_connection(connection_details)

        # Check if table exists
        table_exists = log_table_action(connection, TABLE_NAME)

        # Load team_stats into pagila
        team_stats.to_sql(
            TABLE_NAME,
            con=connection,
            schema=schema,
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
            "Failed to connect to the database when creating team stats table:"
            f" {e}"
        )
        raise QueryExecutionError(f"Database connection failed: {e}")
    except pd.errors.DatabaseError as e:
        logger.error(f"Failed to create team stats table: {e}")
        raise QueryExecutionError(f"Failed to execute query: {e}")
    finally:
        if connection and hasattr(connection, "close"):
            connection.close()
