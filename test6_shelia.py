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



def test_index_names() -> None:
    """Tests that multi-index Columns within DataFrames validate correctly."""
    schema = DataFrameSchema(
        {
            ("one"): Column(Float, Check(lambda s: (s > 0) & (s < 1))),
            ("two"): Column(String, Check(lambda s: s.isin(["a", "b", "c", "d"]))),
            ("three"): Column(Int, Check(lambda s: (s > 0) & (s < 10))),
            ("four"): Column(DateTime, Check(lambda s: s == pd.Timestamp(2022, 11, 11))),
        }
    )
    validated_df = schema.validate(
        pd.DataFrame(
            {
                ("one"): [0.1, 0.2, 0.7, 0.3],
                ("two"): ["a", "b", "c", "d"],
                ("three"): [1, 6, 4, 7],
                ("four"): pd.to_datetime(["2022/11/11"] * 4),
            }
        )
    )
    assert isinstance(validated_df, pd.DataFrame)