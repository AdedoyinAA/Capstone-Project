import pandas as pd


def trim_whitespaces(data: pd.DataFrame) -> pd.DataFrame:
    # Trim leading and trailing whitespaces in column names
    data.columns = data.columns.str.strip()

    # Trim leading and trailing whitespaces in rows
    data[data.select_dtypes(include="string").columns] = (
        data.select_dtypes(
            include="string").apply(lambda x: x.str.strip())
    )

    return data
