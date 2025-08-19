import os
import logging
from src.utils.logging_utils import setup_logger
from typing import Dict


class KaggleConfigurationError(Exception):
    pass


# Configure the logger
logger = setup_logger(__name__, "kaggle.log", level=logging.DEBUG)


def load_kaggle_config() -> Dict[str, Dict[str, str]]:
    """
    Load the kaggle configuration from the environment variables
    Set this with the appropriate values in the .env file or in the
    deployment environment.
    Run with the ENV environment variable set to the appropriate environment,
    so for the dev environment:
        run_etl dev
    Other environments are test and prod
    :return: Dictionaty containing kaggle connection parameters.
    """

    config = {
        "kaggle": {
            "username": os.getenv("KAGGLE_USERNAME", "error"),
            "key": os.getenv("KAGGLE_KEY", ""),
        },
    }

    validate_kaggle_config(config)

    return config


def validate_kaggle_config(config):
    for kaggle_key, kaggle_config in config.items():
        for key, value in kaggle_config.items():
            if value == "error":
                logger.setLevel(logging.ERROR)
                logger.error(
                    f"Configuration error: {kaggle_key} {key}"
                    f" is set to 'error'"
                )
                raise KaggleConfigurationError(
                    f"Configuration error: {kaggle_key} {key}"
                    f" is set to 'error'"
                )
