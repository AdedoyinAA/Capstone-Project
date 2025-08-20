from pathlib import Path


def load_sql_query(filename: str):
    sql_path = Path("sql") / filename
    with open(sql_path, "r") as file:
        query = file.read()
    return query
