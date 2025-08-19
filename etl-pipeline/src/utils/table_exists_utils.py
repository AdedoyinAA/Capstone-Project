from sqlalchemy import Connection, text
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")


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
