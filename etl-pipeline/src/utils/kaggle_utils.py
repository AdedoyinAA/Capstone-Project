import os
import subprocess
import zipfile
import logging
from src.utils.logging_utils import setup_logger


class KaggleConnectionError(Exception):
    pass


class KaggleDownloadError(Exception):
    pass


# Configure the logger
logger = setup_logger(__name__, "kaggle_query.log", level=logging.DEBUG)


def check_kaggle_credentials():
    """This is done to check if the Kaggle API credentials exist."""
    kaggle_path = os.path.expanduser("~/.kaggle/kaggle.json")
    if not os.path.exists(kaggle_path):
        logger.setLevel(logging.ERROR)
        logger.error("Kaggle API credentials not found.")
        raise KaggleConnectionError("Kaggle API credentials not found.")
    logger.info("Kaggle API credentials found.")


def download_nba_dataset_from_kaggle(dataset, destination="data/raw"):
    """This downloads the entire Kaggle dataset,
    unzips it and stores the CSV files in the data/raw folder"""
    try:
        # Create the destination folder if it does not exist already
        os.makedirs(destination, exist_ok=True)

        # Run the Kaggle CLI to download the dataset as a zip file
        subprocess.run(
            ["kaggle",
             "datasets",
             "download",
             dataset,
             "-p",
             destination,
             "--force"],
            check=True
        )

        # Find the downloaded zip file
        downloaded_files = [f for f in os.listdir(destination)
                            if f.endswith(".zip")]
        if not downloaded_files:
            raise KaggleDownloadError("No zip file was \
                downloaded from Kaggle.")

        zip_file = os.path.join(destination, downloaded_files[0])

        # Extract the contents into a temp folder
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination)

        # Remove the zip file after extraction
        os.remove(zip_file)

        logger.info(f"Dataset '{dataset}' downloaded and "
                    f"extracted to '{destination}'.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Kaggle CLI error: {e}")
        raise KaggleDownloadError(f"Failed to download "
                                  f"dataset {dataset} from Kaggle.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise KaggleDownloadError(f"Unexpected error when "
                                  f"downloading dataset {dataset}: {e}")
