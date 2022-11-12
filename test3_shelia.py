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

#validating coerce_datatype method
def test_coerce_dtype():
     test_data = pd.DataFrame(
        {
            "x": ["eat", "sleep", "travel"],
            "y": [2.0, 3.0, 4.0],
            "z": ["aaa", "bbb", "ccc"],
            "x": [1,2,3],
        }
        )

     column_check=Column(String,name="x")
     x=column_check.coerce_dtype(test_data)
     assert isinstance(x,pd.DataFrame)

