import pandas as pd
import pandera as pa
from pandera import (DataFrameSchema, Column)
from pandera.engines.pandas_engine import Engine

# This will give correct output with coercion 
# schema = DataFrameSchema(columns={f"column_{i}": Column(float) for i in range(5)},dtype=int,coerce=True,)

df = pd.DataFrame({f"column_{i}": range(10) for i in range(5)}, dtype=int)
print(df) 
# This will give output without coercion. Error will be shown
schema = DataFrameSchema(columns={f"column_{i}": Column(float) for i in range(5)},dtype=float)
print(schema(df))