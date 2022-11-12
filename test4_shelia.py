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

#validating if column object works as a dataframe

def test_column() -> None:
    """tests if the column object can be used to check as a dataframe. checks for the column class"""
    test_data = pd.DataFrame(
        {
            "x": ["eat", "sleep", "travel"],
            "y": [2.0, 3.0, 4.0],
            "z": ["aaa", "bbb", "ccc"],
            "w": [1,2,3],
        }
    )

    column_1= Column(String, name="x")
    column_2= Column(Float, name="y")
    column_3 = Column(String, name="z")
    column_4= Column(Int, name="w")

    assert isinstance(
        test_data.pipe(column_1).pipe(column_2).pipe(column_3).pipe(column_4), pd.DataFrame
    )

    with pytest.raises(errors.SchemaError):
        Column(Int)(test_data)

