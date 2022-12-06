import pandera as pa
import pandas as pd
from pandera import (
    Check,
    Column,
    DataFrameSchema,
    Index,
    MultiIndex,
    SeriesSchema,
    errors,
)
from typing import Dict
import pytest
from datetime import datetime
from pandera.engines.pandas_engine import Engine


# get_dtypes
test_schema = DataFrameSchema(
    {
        "first_col": Column(int),
        "var*": Column(float, regex=True),
    }
)
test_data = pd.DataFrame(
    {
        "first_col": [1254, 41852, 103],
        "variable1": [8.0, 4.1, 2.2],
        "variable2": [1.760, 1.16, 15.2],
    }
)
time_taken_by_get_dtypes = test_schema.get_dtypes(test_data)

# validate - ordered columns
test_schema2 = DataFrameSchema(columns={
                "column_a": Column(int, required=False),
                "column_b": Column(int, required=False),
            })
test_df2 = pd.DataFrame(
    data=[[154, 2456, 398]],
    columns=["column_a", "column_a", "column_b"],
    index=pd.MultiIndex.from_arrays(
        [[1], [2], [3]], names=["column_a", "column_a", "column_b"]
    ),
)
time_taken_by_validate = test_schema2.validate(test_df2)

# dtypes
schema4 = DataFrameSchema(
    columns={
        "col1": Column(int),
        "col2": Column(str),
        "col3": Column(datetime),
        "col4": Column("uint16"),
    }
)
schema4.dtypes == {
    "col1": Engine.dtype("int64"),
    "col2": Engine.dtype("str"),
    "col3": Engine.dtype("datetime64[ns]"),
    "col4": Engine.dtype("uint16"),
}

# add_columns
schema5 = DataFrameSchema(
        {
            "column_no_1": Column(int, Check(lambda x: X >= 0)),
        },
        strict=True,
    )
schema6 = schema5.add_columns(
        {
            "column_no_2": Column(str, Check(lambda y: y <= 0)),
            "column_no_3": Column(object, Check(lambda z: z == 0)),
        }
    )