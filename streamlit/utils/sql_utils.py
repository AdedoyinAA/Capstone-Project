from pathlib import Path


def load_sql_query(filename: str):
    # Get the absolute path for the sql directory
    base_dir = Path(__file__).parent.parent
    sql_path = base_dir / "sql" / filename

    if not sql_path.exists():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")
    with open(sql_path, "r") as file:
        query = file.read()
    return query
