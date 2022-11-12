"""Testing the components of the Schema objects."""

import copy
from typing import Any, List, Optional, Tuple, Type

import pandas as pd
import pytest

from pandera import (
    Check,
    Column,
    DataFrameSchema,
    DateTime,
    Float,
    Index,
    Int,
    MultiIndex,
    SeriesSchema,
    String,
    errors,
)
from pandera.engines.pandas_engine import Engine, pandas_version
#vaidating get_regex_column method

@pytest.mark.parametrize(
    "column_name_regex, expected_matches, error",
    (
        # match all values in first level, only baz_* for second level
        ((".", "baz_.+"), [("foo_2", "baz_1"), ("foo_3", "baz_2")], None),
        # no matches should raise a SchemaError
        (("fiz", "."), None, errors.SchemaError),
        # using a string name for a multi-index column raises IndexError
        ("foo_1", None, IndexError),
        # mis-matching number of elements in a tuple column name raises
        # IndexError
        (("foo_.+",), None, IndexError),
        (("foo_.+", ".", "."), None, IndexError),
        (("foo_.+", ".", ".", "."), None, IndexError),
    ),
)
def test_column_regex_matching(
    column_name_regex: str,
    expected_matches: Optional[List[Tuple[str, str]]],
    error: Type[BaseException],
) -> None:
    """
    Column regex pattern matching should yield correct matches and raise
    expected errors.
    """
    columns = pd.MultiIndex.from_tuples(
        (
            ("foo_1", "biz_1"),
            ("foo_2", "baz_1"),
            ("foo_3", "baz_2"),
            ("bar_1", "biz_2"),
            ("bar_2", "biz_3"),
            ("bar_3", "biz_3"),
        )
    )

    column_schema = Column(
        Int,
        Check(lambda s: s >= 0),
        name=column_name_regex,
        regex=True,
    )
    if error is not None:
        with pytest.raises(error):
            column_schema.get_regex_columns(columns)
    else:
        matched_columns = column_schema.get_regex_columns(columns)
        assert expected_matches == matched_columns.tolist()

