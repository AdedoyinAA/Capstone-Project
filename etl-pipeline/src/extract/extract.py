from src.extract.extract_boxscores import extract_boxscores
from src.extract.extract_games import extract_games
from src.extract.extract_playerinfo import extract_playerinfo
from src.extract.extract_salaries import extract_salaries
from src.utils.logging_utils import setup_logger


# Configure the logger
logger = setup_logger("extract_data", "extract_data.log")


def extract_data():
    """
    Function which executes the extraction process

    Returns:
        Tuple: A tuple containing all the extracted DataFrames
    """
    try:
        logger.info("Starting data extraction process")
        # Extract the box scores data
        box_scores = extract_boxscores()
        games = extract_games()
        player_info = extract_playerinfo()
        salaries = extract_salaries()

        logger.info(
            "Data extraction completed successfully"
        )

        return (box_scores, games, player_info, salaries)

    except Exception as e:
        logger.error(f"Data extraction failed: {e}")
        raise
