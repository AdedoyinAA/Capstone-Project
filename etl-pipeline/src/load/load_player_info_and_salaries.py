import pandas as pd
from typing import Optional
from src.load.create_player_info_and_salaries import (
    create_player_info_and_salaries
)
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")


def load_player_info_and_salaries(
    player_info_and_salaries: Optional[pd.DataFrame]
) -> None:
    if player_info_and_salaries is None or player_info_and_salaries.empty:
        logger.warning("No data to load - DataFrame is empty or None")
        return

    logger.info("Starting data load process...")
    create_player_info_and_salaries(player_info_and_salaries)
    logger.info(
        "Player Information and Salaries Data "
        "load process completed successfully."
    )
