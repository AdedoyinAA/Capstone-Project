import os
import sys
from dotenv import load_dotenv
from src.utils.logging_utils import setup_logger

# Setup logger
logger = setup_logger("schema", "schema.log")


def set_schema():
    """
    Determines the database schema to use based on the runtime environment.

    It loads the appropriate `.env` file depending on the mode provided
    as a command-line argument (`prod`, `dev`, or `test`).
    Defaults to `prod` if no argument is provided.

    - `prod` → loads `.env` and uses schema `"de_2506_a"`
    - `dev`  → loads `.env.dev` and uses schema `"de_2506_a"`
    - `test` → loads `.env.test` and uses schema `"public"`

    Returns:
        schema (str): The schema name to be used for database operations.
    """
    mode = sys.argv[1] if len(sys.argv) > 1 else "prod"

    # Map mode to correct .env file
    env_files = {
        "prod": ".env",
        "dev": ".env.dev",
        "test": ".env.test"
    }

    env_file = env_files.get(mode, ".env")
    load_dotenv(dotenv_path=env_file)

    # Read ENV value from env file
    env = os.getenv("ENV", mode)
    logger.info(f"Current mode: {mode}, ENV variable: {env}")

    # Pick schema
    BASE_SCHEMA = "de_2506_a"
    if env == "test":
        schema = "public"
    else:
        schema = BASE_SCHEMA
    return schema
