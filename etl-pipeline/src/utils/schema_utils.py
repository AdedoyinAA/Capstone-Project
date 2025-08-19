import os
import sys
from dotenv import load_dotenv
from src.utils.logging_utils import setup_logger

# Setup logger
logger = setup_logger("schema", "schema.log")


def set_schema():
    # Determine which env file to load
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
