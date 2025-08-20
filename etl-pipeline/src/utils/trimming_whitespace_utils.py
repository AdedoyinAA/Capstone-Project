import pandas as pd


def trim_whitespaces(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove leading and trailing whitespaces from column names
    and string-type cell values in a DataFrame.

    This function ensures data consistency by:
      - Stripping whitespace from all column names.
      - Stripping whitespace from all string/object columns in each row.

    Args:
        data (pd.DataFrame): Input DataFrame containing raw data
        that may have extra whitespaces in column names or values.

    Returns:
        pd.DataFrame: Cleaned DataFrame with trimmed column names
        and string values.
    """
    # Trim leading and trailing whitespaces in column names
    data.columns = data.columns.str.strip()

    # Trim leading and trailing whitespaces in rows
    data[data.select_dtypes(include="string").columns] = (
        data.select_dtypes(
            include="string").apply(lambda x: x.str.strip())
    )

    return data
