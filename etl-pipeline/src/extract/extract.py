from src.extract.extract_boxscores import extract_boxscores
from src.extract.extract_games import extract_games
from src.utils.logging_utils import setup_logger


# Configure the logger
logger = setup_logger("extract_data", "extract_data.log")


def extract_data():
    try:
        logger.info("Starting data extraction process")

        box_scores = extract_boxscores()
        games = extract_games()

        logger.info(
            "Data extraction completed successfully"
        )

        return (box_scores, games)

    except Exception as e:
        logger.error(f"Data extraction failed: {e}")
        raise
