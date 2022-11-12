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

#validating the regex method
def test_regex():
    test_data = pd.DataFrame(
        {
            "x": ["eat", "sleep", "travel"],
            "y": [2.0, 3.0, 4.0],
            "z": ["aaa", "bbb", "ccc"],
            "w": [1,2,3],
        }
    )

    column_check=Column(String,name="w",regex="TRUE")
    assert column_check.regex=="TRUE"




    column_check=Column(String,name="w",regex="TRUE")
    assert column_check.regex=="TRUE"
