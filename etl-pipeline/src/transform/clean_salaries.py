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
    """
    Rename columns in the salaries DataFrame to more descriptive names.
    This function updates the column names of the input DataFrame to follow
    a consistent naming convention, making it easier to work with the data
    programmatically.

    Args:
        salaries (pd.DataFrame): DataFrame containing salary information
        with columns like 'playerName', 'seasonStartYear', 'salary', and
        'inflationAdjSalary'.

    Returns:
        pd.DataFrame: Updated DataFrame with renamed columns:
        - 'playerName' -> 'player_name'
        - 'seasonStartYear' -> 'season_start_year'
        - 'salary' -> 'salary'
        - 'inflationAdjSalary' -> 'inflation_adjusted_salary'
    """
    dict_for_renaming_columns = {
        "playerName": "player_name ",
        "seasonStartYear": "season_start_year ",
        "salary": "salary ",
        "inflationAdjSalary": "inflation_adjusted_salary",
    }
    salaries = salaries.rename(columns=dict_for_renaming_columns)

    return salaries


def remove_dollar_sign(salaries: pd.DataFrame) -> pd.DataFrame:
    """
    Remove the dollar sign ('$') from salary-related columns in the DataFrame.
    This function cleans the 'salary' and 'inflation_adjusted_salary' columns
    by removing the '$' symbol, allowing them to be converted to numeric types
    for analysis or calculations.

    Args:
        salaries (pd.DataFrame): DataFrame containing salary information with
        columns 'salary' and 'inflation_adjusted_salary'.

    Returns:
        pd.DataFrame: Updated DataFrame with the '$' symbol removed from the
                      specified columns.
    """
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
    """
    Convert the 'season_start_year' column to numeric values.
    This function ensures that the 'season_start_year' column is of numeric
    type (int or float), coercing any invalid entries to NaN. This is useful
    for filtering, sorting, or performing calculations based on the year.

    Args:
        salaries (pd.DataFrame): DataFrame containing a
        'season_start_year' column.

    Returns:
        pd.DataFrame: Updated DataFrame with 'season_start_year'
        converted to numeric type.
    """
    salaries["season_start_year"] = pd.to_numeric(
        salaries["season_start_year"], errors="coerce"
    )

    return salaries


def filter_2015_to_2019(salaries: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the salaries DataFrame to include only seasons from 2015 to 2019.

    Args:
        salaries (pd.DataFrame): DataFrame containing a
        'season_start_year' column.

    Returns:
        pd.DataFrame: Filtered DataFrame with rows where
        'season_start_year' is between 2015 and 2019 inclusive.
    """
    # Filter only dates between 2014 and 2019
    salaries_filtered = salaries[
        (salaries["season_start_year"] >= 2015) &
        (salaries["season_start_year"] <= 2019)]

    return salaries_filtered
