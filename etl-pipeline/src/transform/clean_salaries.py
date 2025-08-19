import pandas as pd
import os
from src.utils.trimming_whitespace_utils import trim_whitespaces
from src.utils.remove_special_characters_utils import remove_special_characters

FILE_PATH = "data/processed/cleaned_salaries.csv"

# Create directory if it does not exist
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)


def clean_salaries(salaries: pd.DataFrame) -> pd.DataFrame:
    # Rename columns
    salaries = rename_columns(salaries)
    # Trim whitespaces
    salaries = trim_whitespaces(salaries)
    # Remove dollar sign from salary columns
    salaries = remove_dollar_sign(salaries)
    # Convert year to numeric
    salaries = convert_year_to_numeric(salaries)
    # Remove special characters from player names
    salaries = remove_special_characters(salaries)
    # Keep only salaries from 2015 to 2019
    salaries = filter_2015_to_2019(salaries)
    # Save the cleaned dataframe as a CSV
    salaries.to_csv(FILE_PATH, index=False)

    return salaries


def rename_columns(salaries: pd.DataFrame) -> pd.DataFrame:
    dict_for_renaming_columns = {
        "playerName": "player_name ",
        "seasonStartYear": "season_start_year ",
        "salary": "salary ",
        "inflationAdjSalary": "inflation_adjusted_salary",
    }
    salaries = salaries.rename(columns=dict_for_renaming_columns)

    return salaries


def remove_dollar_sign(salaries: pd.DataFrame) -> pd.DataFrame:
    columns_to_remove_dollar_sign = [
        "salary",
        "inflation_adjusted_salary"
    ]
    salaries[columns_to_remove_dollar_sign] = \
        salaries[columns_to_remove_dollar_sign].apply(
            lambda col: col.str.replace("$", "", regex=False)
        )

    return salaries


def convert_year_to_numeric(salaries: pd.DataFrame) -> pd.DataFrame:
    salaries["season_start_year"] = pd.to_numeric(
        salaries["season_start_year"], errors="coerce"
    )

    return salaries


def filter_2015_to_2019(salaries: pd.DataFrame) -> pd.DataFrame:
    # Filter only dates between 2014 and 2019
    salaries_filtered = salaries[
        (salaries["season_start_year"] >= 2015) &
        (salaries["season_start_year"] <= 2019)]

    return salaries_filtered
