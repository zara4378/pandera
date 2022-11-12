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


#validating the set_name function

def test_set_name()->None:
    "test if name of the column object has been changed"

    test_data = pd.DataFrame(
        {
            "x": ["eat", "sleep", "travel"],
            "y": [2.0, 3.0, 4.0],
            "z": ["aaa", "bbb", "ccc"],
            "w": [1,2,3],
        }
    )

    column_a= Column(Int, name="w")
    data1=column_a.set_name("p")
    #print(data1.name)
    assert data1.name=="p"

