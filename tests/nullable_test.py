import pandera as pa
import pandas as pd
print("aaaaaaa")
schema = pa.DataFrameSchema({
    "col1": pa.Column(int),
    "col2": pa.Column(int,nullable=True),
    "col3": pa.Column(int,nullable=True),
    "col4": pa.Column(int,nullable=False)
})

data = pd.DataFrame({"col1": [1,2,3],"col3": [3,2,1]})

validated_data = schema(data)
print(validated_data)