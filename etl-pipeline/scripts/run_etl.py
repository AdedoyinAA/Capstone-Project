import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract_data
from src.transform.transform import transform_data
from src.load.load_player_stats import load_player_stats
from src.load.load_team_stats import load_team_stats
from src.load.load_player_info_and_salaries import (
    load_player_info_and_salaries
)
from src.utils.logging_utils import setup_logger

# Configure the logger
log_base_path = os.getenv("LOG_BASE_PATH")
logger = setup_logger(
    "etl_pipeline",
    "etl_pipeline.log",
    base_path=log_base_path
)


def main():
    try:
        # Get the argument from the run_etl command and set up the environment
        setup_env(sys.argv)
        env = os.getenv("ENV", "unknown")

        logger.info(f"Starting ETL pipeline in {env} environment")

        logger.info("Beginning data extraction phase")
        extracted_data = extract_data()
        logger.info("Data extraction phase completed")
        logger.info(
            f"ETL pipeline completed successfully in {env} environment"
        )
        logger.info("Beginning the data transformation phase")
        transformed_data = transform_data(extracted_data)
        logger.info("Data transformation phase completed")

        logger.info("Beginning data loading phase")
        # Load player stats into Pagila
        load_player_stats(transformed_data[4])
        # Load team stats into Pagila
        load_team_stats(transformed_data[5])
        # Load player info and salaries into Pagila
        load_player_info_and_salaries(transformed_data[6])
        logger.info("Data loading phase completed")
        logger.info(
            f"ETL pipeline completed successfully in {env} environment"
        )

        return transformed_data
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
