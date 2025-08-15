import pandas as pd
import logging
import timeit
from src.utils.logging_utils import setup_logger, log_extract_success

# Define the file path for the games CSV file
FILE_PATH = "data/raw/games.csv"

# Configure the logger
logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)

TYPE = "GAMES from KAGGLE"

EXPECTED_PERFORMANCE = 1


def extract_games() -> pd.DataFrame:
    # Performance analysis
    start_time = timeit.default_timer()

    try:
        games = pd.read_csv(FILE_PATH)
        extract_games_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            TYPE,
            games.shape,
            extract_games_execution_time,
            EXPECTED_PERFORMANCE,
        )
        return games
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")
