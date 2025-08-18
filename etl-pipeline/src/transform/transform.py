import pandas as pd
from typing import Tuple
from src.transform.clean_boxscores import clean_boxscores
from src.transform.clean_games import clean_games
from src.transform.clean_playerinfo import clean_playerinfo
from src.transform.clean_salaries import clean_salaries
from src.transform.merge_boxscores_games import merge_boxscores_games
from src.transform.transform_merged_boxscores_games import get_player_stats
from src.transform.transform_merged_boxscores_games import get_team_stats
from src.utils.logging_utils import setup_logger


# Configure the logger
logger = setup_logger("transform_data", "transform_data.log")


def transform_data(data) -> Tuple[pd.DataFrame, pd.DataFrame]:
    try:
        logger.info("Starting data transformation process...")
        # Clean box scores data
        logger.info("Cleaning box scores data...")
        cleaned_boxscores = clean_boxscores(data[0])
        logger.info("Box Scores data cleaned successfully.")

        # Clean games data
        logger.info("Cleaning games data...")
        cleaned_games = clean_games(data[1])
        logger.info("Games data cleaned successfully.")

        # Clean player information data
        logger.info("Cleaning player information data...")
        cleaned_playerinfo = clean_playerinfo(data[2])
        logger.info("Player Information data cleaned successfully.")

        # Clean salaries data
        logger.info("Cleaning salaries data...")
        cleaned_salaries = clean_salaries(data[3])
        logger.info("Salaries data cleaned successfully.")

        # Enrich box scores and games data
        logger.info("Merging box scores and games data...")
        merged_boxscores_games = merge_boxscores_games(
            cleaned_boxscores,
            cleaned_games
        )
        logger.info("Data merged successfully.")

        # Get player stats
        logger.info("Extracting Player Stats...")
        player_stats = get_player_stats(merged_boxscores_games)
        logger.info("Player Stats successfully transformed.")

        # Get team stats
        logger.info("Extracting Team Stats...")
        team_stats = get_team_stats(merged_boxscores_games)
        logger.info("Team Stats successfully transformed.")

        logger.info(
            "Data transformation completed successfully."
        )
        return (
            cleaned_boxscores,
            cleaned_games,
            cleaned_playerinfo,
            cleaned_salaries,
            player_stats,
            team_stats
        )

    except Exception as e:
        logger.error(f"Data transformation failed: {e}")
        raise
