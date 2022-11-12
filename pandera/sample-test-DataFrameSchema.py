from pandera import (
    Column,
    DataFrameSchema,
    Index,
    MultiIndex,
    SeriesSchema,
    errors,
)
from pandera.engines.pandas_engine import Engine
from typing import Dict
from pandera import DataFrameSchema
import pandas as pd
import pytest


#Test case#1 to test schema dtpye and get_dtypes 
def test_case_for_get_dtypes():
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
    assert test_schema.get_dtypes(test_data) == {
        "first_col": Engine.dtype(int),
        "variable1": Engine.dtype(float),
        "variable2": Engine.dtype(float),
    }

# Test Case#2 to check column name change
def test_case_for_df_reset_column_name() -> None:
    DataFrameSchema(columns={"new_column_name": Column(name="old_column_name")})


# Test case#3 for ordered columns
@pytest.mark.parametrize(
    "test_columns,test_index",
    [
        (
            {
                "column_a": Column(int, required=False),
                "column_b": Column(int, required=False),
            },
            None,
        ),
        (
            None,
            MultiIndex(
                indexes=[Index(int, name="column_a"), Index(int, name="column_b")],
            ),
        ),
    ],
)
def test_case_for_ordered_df(
    test_columns: Dict[str, Column], test_index: MultiIndex
) -> None:

    test_schema = DataFrameSchema(columns=test_columns, index=test_index, ordered=True)

    test_df = pd.DataFrame(
        data=[[154, 2456, 398]],
        columns=["column_a", "column_a", "column_b"],
        index=pd.MultiIndex.from_arrays(
            [[1], [2], [3]], names=["column_a", "column_a", "column_b"]
        ),
    )
    assert isinstance(test_schema.validate(test_df), pd.DataFrame)


# Test case#4 to detect duplicate columns
def test_case_for_duplicate_columns_in_df():
    test_data_col_labels = ["first", "first", "third"]
    test_schema = DataFrameSchema(
        columns={i: Column(int) for i in test_data_col_labels},
        unique_column_names=True,
    )
    assert test_schema.unique_column_names


# Test case#5 to check how null cases are handeled when data type is not specified
def test_case_for_no_dtype_df():
    test_schema = DataFrameSchema({"column_A": Column(nullable=False)})
    test_df = test_schema.validate(pd.DataFrame({"column_A": [-12453.1, -676.355, 17.089]}))
    assert isinstance(test_df, pd.DataFrame)


# Test case#6 to check how null cases are handeled in SeriesSchemas when data type is specified
def test_case_for_no_dtype_series() -> None:
    test_schema = SeriesSchema(nullable=False)
    test_series = test_schema.validate(pd.Series([ 23, 34, 45, 56, 67]))
    assert isinstance(test_series, pd.Series)

    test_schema = SeriesSchema(nullable=True)
    test_series = test_schema.validate(pd.Series([23, 34, None, 56, 67]))
    assert isinstance(test_series, pd.Series)

    with pytest.raises(errors.SchemaError):
        test_schema = SeriesSchema(nullable=False)
        test_schema.validate(pd.Series([23, 34, None, 56, 67]))