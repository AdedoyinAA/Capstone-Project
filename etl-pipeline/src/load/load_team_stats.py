import pandas as pd
from typing import Optional
from src.load.create_team_stats import (
    create_team_stats
)
from src.utils.logging_utils import setup_logger


# Setup the logger
logger = setup_logger("load_data", "load_data.log")


def load_team_stats(team_stats: Optional[pd.DataFrame]) -> None:
    if team_stats is None or team_stats.empty:
        logger.warning("No data to load - DataFrame is empty or None")
        return

    logger.info("Starting data load process...")
    create_team_stats(team_stats)
    logger.info("Team Stats Data load process completed successfully.")
