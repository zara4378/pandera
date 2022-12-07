import pytest
import re
import pandera as pa
import HtmlTestRunner
import unittest


from pandera.errors import SchemaError, SchemaInitError
from pandera import Check, Column, DataFrameSchema
from pandera.typing import DataFrame, Index, Series, String
from typing import Any, Generic, Iterable, Optional, TypeVar




def test_schema() -> None:
    
    class validate(pa.SchemaModel):
        a: Series[int]
        b: Series[str]
        c: Series[Any]
        idx: Index[str]
        
    expect = pa.DataFrameSchema(name = "validate", columns = {"a": pa.Column(int), "b": pa.Column(str), 
                                                            "c": pa.Column()}, index = pa.Index(str))
    assert expect == validate.to_schema()
    
def test_empty_schema() -> None:
    empty = pa.DataFrameSchema(name = "Empty")
    
    class Empty(pa.SchemaModel):
        pass
    assert empty == Empty.to_schema()
    

    
    
def test_invalid_annotations() -> None: 
    
    class absent(pa.SchemaModel):
        x = pa.Field()
        y: Series[int]
        z = pa.Field()
        _num = 0
        
    error = re.escape("Found missing annotations: ['x', 'z']")
     
    with pytest.raises(pa.errors.SchemaInitError, match=error): absent.to_schema()
    
   
        
    
def test_empty_data() -> None:
     expect = pa.DataFrameSchema(name = "emptyData", columns = {"emptyColumn": pa.Column()})
     
     class emptyData(pa.SchemaModel):
         emptyColumn: pa.typing.Series
     
     assert emptyData.to_schema() == expect
     
     
     
def test_invalid_field() -> None:
    
    class invalid(pa.SchemaModel):
        a: Series[int] = 0
        
    with pytest.raises(pa.errors.SchemaInitError, match="'a' can only be assigned a 'Field'"): invalid.to_schema()
    
    

def test_multipleIndex() -> None:
    
    class Schema(pa.SchemaModel):
        a: Index[int] = pa.Field(gt=0)
        b: Index[str]
        
    expect = pa.DataFrameSchema(name = "Schema", index = pa.MultiIndex(
        [pa.Index(int, name="a", checks=pa.Check.gt(0)), pa.Index(str, name="b")]))
    
    assert expect == Schema.to_schema()
    
    
# testCases = unittest.TestLoader().loadTestsFromTestCase(testModels)


# outfile = open("C: Users\zahra\Documents\Pandera_ZaraReport.html", "w")

# runner = HtmlTestRunner.HTMLTestRunner(
#     stream = outfile)
#     #title = 'title', 
#     #description = 'Unit Test Report')

# runner.run(testCases)

