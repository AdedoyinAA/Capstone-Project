import pandas as pd
from typing import Tuple
from src.transform.clean_boxscores import clean_boxscores
from src.transform.clean_games import clean_games
from src.transform.clean_playerinfo import clean_playerinfo
from src.transform.clean_salaries import clean_salaries
from src.utils.logging_utils import setup_logger


# Configure the logger
logger = setup_logger("transform_data", "transform_data.log")


def transform_data(data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting data transformation process")
        cleaned_boxscores = clean_boxscores(data[0])
        cleaned_games = clean_games(data[1])
        cleaned_playerinfo = clean_playerinfo(data[2])
        cleaned_salaries = clean_salaries(data[3])
        logger.info(
            "Data transformation completed successfully"
        )
        return (
            cleaned_boxscores,
            cleaned_games,
            cleaned_playerinfo,
            cleaned_salaries
        )

    except Exception as e:
        logger.error(f"Data transformation failed: {e}")
        raise
