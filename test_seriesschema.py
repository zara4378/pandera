import pandas as pd
import pytest

from pandera import (
    SeriesSchema,
    Check,
    errors,
    DataFrameSchema,Column
)
from pandera.schemas import SeriesSchemaBase
from pandera.engines.pandas_engine import Engine

def test_seriesschema_checks() -> None:
    
    series_schema_without_checks = SeriesSchema()
    series_schema_withone_check = SeriesSchema(checks=Check.eq(0))
    series_schema_withmultiple_checks = SeriesSchema(
        checks=[Check.gt(0), Check.lt(100)]
    )

    for schema in [
        series_schema_without_checks,
        series_schema_withone_check,
        series_schema_withmultiple_checks,
    ]:
        assert isinstance(schema.checks, list)

    assert len(series_schema_without_checks.checks) == 0
    assert len(series_schema_withone_check.checks) == 1
    assert len(series_schema_withmultiple_checks.checks) == 2
    
    
def test_seriesschema_multiplevalidators() -> None:
    
    schema = SeriesSchema(
        int,
        [
            Check(lambda j: 0 <= j <= 35, element_wise=True),
            Check(lambda k: (k == 19).any()),
        ],
    )
    multiplevalidated_series = schema.validate(pd.Series([1, 4, 19, 35]))
    assert isinstance(multiplevalidated_series, pd.Series)

    with pytest.raises(errors.SchemaError):
         schema.validate(pd.Series([1, 4, 17, 35]))
         
def test_nodtypewithoutnull() -> None:
    
    schema = SeriesSchema(nullable=False)
    validatenodatatype = schema.validate(pd.Series([2, 7, 2, 3, 4, 6]))
    assert isinstance(validatenodatatype, pd.Series)

    with pytest.raises(errors.SchemaError):
        schema = SeriesSchema(nullable=False)
        schema.validate(pd.Series([0, 2, 3, None, 4, 1]))
        
def test_nodtypewithnull() -> None:
   
    schema = SeriesSchema(nullable=True)
    validatenodatatype = schema.validate(pd.Series([0, 4, 5, None, 4, 1]))
    assert isinstance(validatenodatatype, pd.Series)

    with pytest.raises(errors.SchemaError):
        schema = SeriesSchema(nullable=False)
        schema.validate(pd.Series([0, None, 3, None, 4, 1]))
        
def test_coerce_withouttype() -> None:
    
    df = pd.DataFrame({"col": [4, 5, 6]})
    for schema in [
        DataFrameSchema({"col": Column(coerce=True)}),
        DataFrameSchema({"col": Column()}, coerce=True),
    ]:
        assert isinstance(schema(df), pd.DataFrame)


def test_schematype() -> None:
    
    schema = DataFrameSchema(
        columns={
            "col1": Column(int),
            "col2": Column(str),
            "col3": Column("uint64"),
        }
    )
    assert schema.dtypes == {
        "col1": Engine.dtype("int64"),
        "col2": Engine.dtype("str"),
        "col3": Engine.dtype("uint64"),
    }
    
