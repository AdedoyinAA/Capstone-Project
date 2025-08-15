import subprocess
import pytest
from unittest.mock import patch, MagicMock
from src.utils.kaggle_utils import (
    check_kaggle_credentials,
    download_nba_dataset_from_kaggle,
    KaggleConnectionError,
    KaggleDownloadError
)


def test_check_kaggle_credentials_exists(tmp_path, caplog):
    # Create a fake kaggle.json file
    creds_path = tmp_path / "kaggle.json"
    creds_path.write_text('{"username":"test","key":"123"}')

    # Patch os.path.expanduser to point to tmp_path
    with patch("os.path.expanduser", return_value=str(creds_path)):
        with caplog.at_level("INFO"):
            check_kaggle_credentials()
            assert "Kaggle API credentials found." in caplog.text


def test_check_kaggle_credentials_missing(tmp_path, caplog):
    fake_path = tmp_path / "nonexistent.json"

    with patch("os.path.expanduser", return_value=str(fake_path)):
        with pytest.raises(KaggleConnectionError) as excinfo:
            with caplog.at_level("ERROR"):
                check_kaggle_credentials()
        assert "Kaggle API credentials not found." in caplog.text
        assert "Kaggle API credentials not found." in str(excinfo.value)


def test_download_nba_dataset_success(tmp_path, caplog):
    dataset = "fake/dataset"

    # Create a fake zip file
    zip_path = tmp_path / "dataset.zip"
    zip_path.write_text("dummy")

    with patch("os.makedirs") as mock_makedirs, \
         patch("subprocess.run") as mock_subprocess, \
         patch("os.listdir", return_value=["dataset.zip"]), \
         patch("zipfile.ZipFile") as mock_zipfile, \
         patch("os.remove") as mock_remove:

        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        with caplog.at_level("INFO"):
            download_nba_dataset_from_kaggle(dataset,
                                             destination=str(tmp_path))

            mock_makedirs.assert_called_once()
            mock_subprocess.assert_called_once()
            mock_zip.extractall.assert_called_once_with(str(tmp_path))
            mock_remove.assert_called_once()
            assert f"Dataset '{dataset}' "
            "downloaded and extracted" in caplog.text


def test_download_nba_dataset_subprocess_error(tmp_path):
    with patch("subprocess.run",
               side_effect=subprocess.CalledProcessError(1, "cmd")):
        with pytest.raises(KaggleDownloadError) as excinfo:
            download_nba_dataset_from_kaggle("fake/dataset",
                                             destination=str(tmp_path))
        assert "Failed to download dataset fake/dataset" in str(excinfo.value)
