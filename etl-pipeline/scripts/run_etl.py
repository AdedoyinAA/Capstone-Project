import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract_data
from src.utils.logging_utils import setup_logger

# Configure the logger
logger = setup_logger("etl_pipeline", "etl_pipeline.log")


def main():
    try:
        # Get the argument from the run_etl command and set up the environment
        setup_env(sys.argv)
        env = os.getenv("ENV", "unknown")

        logger.info(f"Starting ETL pipeline in {env} environment")

        logger.info("Beginning data extraction phase")
        extract_data()
        logger.info("Data extraction phase completed")

        logger.info(
            f"ETL pipeline completed successfully in {env} environment"
        )

    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
