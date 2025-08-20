import pandas as pd
from src.utils.kaggle_utils import (
    check_kaggle_credentials,
    download_nba_dataset_from_kaggle,
    KaggleConnectionError,
    KaggleDownloadError
)
import logging
import timeit
from src.utils.logging_utils import setup_logger, log_extract_success

# Define the file path for the box scores CSV file
FILE_PATH = "data/raw/boxscore.csv"

# Configure the logger
logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)

TYPE = "BOX SCORES from KAGGLE"

EXPECTED_PERFORMANCE = 1


def extract_csvs():
    """
    Check for Kaggle API key, downloads the CSV files from Kaggle
    and stores in data/raw
    """
    try:
        check_kaggle_credentials()
        # Dataset on kaggle
        dataset = "patrickhallila1994/nba-data-from-basketball-reference"
        save_path = "data/raw"
        download_nba_dataset_from_kaggle(dataset, destination=save_path)
    except KaggleConnectionError as e:
        logger.error(f"Connection failed: {e}")
    except KaggleDownloadError as e:
        logger.error(f"Download failed: {e}")


def extract_boxscores() -> pd.DataFrame:
    """
    Extracts box scores data from downloaded CSV and stores
    in a DataFrame

    Raises:
        Exception: Handles any exception that are raised
        during runtime

    Returns:
        pd.DataFrame: DataFrame containing box scores data
    """
    extract_csvs()
    # Performance analysis
    start_time = timeit.default_timer()
    try:
        # Read the downloaded CSV file
        box_scores = pd.read_csv(FILE_PATH)
        extract_boxscores_execution_time = timeit.default_timer() - start_time

        # Logging
        log_extract_success(
            logger,
            TYPE,
            box_scores.shape,
            extract_boxscores_execution_time,
            EXPECTED_PERFORMANCE,
        )
        return box_scores
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error loading {FILE_PATH}: {e}")
        raise Exception(f"Failed to load CSV file: {FILE_PATH}")
