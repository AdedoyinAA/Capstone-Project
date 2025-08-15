import pandas as pd
import logging
import timeit
from src.utils.logging_utils import setup_logger, log_extract_success

# Define the file path for the player info CSV file
FILE_PATH = "data/raw/player_info.csv"

# Configure the logger
logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)

TYPE = "PLAYER INFORMATION from KAGGLE"

EXPECTED_PERFORMANCE = 1


def extract_playerinfo() -> pd.DataFrame:
    # Performance analysis
    start_time = timeit.default_timer()

    try:
        player_info = pd.read_csv(FILE_PATH)
        extract_playerinfo_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            TYPE,
            player_info.shape,
            extract_playerinfo_execution_time,
            EXPECTED_PERFORMANCE,
        )
        return player_info
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")
