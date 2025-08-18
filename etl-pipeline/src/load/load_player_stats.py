import pandas as pd
from typing import Optional
from src.load.create_player_stats import (
    create_player_stats
)
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")


def load_player_stats(player_stats: Optional[pd.DataFrame]) -> None:
    if player_stats is None or player_stats.empty:
        logger.warning("No data to load - DataFrame is empty or None")
        return

    logger.info("Starting data load process...")
    create_player_stats(player_stats)
    logger.info("Player Stats Data load process completed successfully.")
