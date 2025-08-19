import os
from unittest.mock import patch
from src.utils.schema_utils import set_schema


@patch.dict(os.environ, {"ENV": "dev"})
def test_else_clause():
    schema = set_schema()
    assert schema == "de_2506_a"
