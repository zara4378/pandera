.. currentmodule:: pandera

.. _lazy_validation:

Lazy Validation
===============

*New in version 0.4.0*

By default, when you call the ``validate`` method on schema or schema component
objects, a :class:`~pandera.errors.SchemaError` is raised as soon as one of the
assumptions specified in the schema is falsified. For example, for a
:class:`~pandera.schemas.DataFrameSchema` object, the following situations will raise an
exception:

* a column specified in the schema is not present in the dataframe.
* if ``strict=True``, a column in the dataframe is not specified in the schema.
* the ``data type`` does not match.
* if ``coerce=True``, the dataframe column cannot be coerced into the specified
  ``data type``.
* the :class:`~pandera.checks.Check` specified in one of the columns returns ``False`` or
  a boolean series containing at least one ``False`` value.


For example:

.. testcode:: non_lazy_validation

   import pandas as pd
   import pandera as pa

   from pandera import Check, Column, DataFrameSchema

   df = pd.DataFrame({"column": ["a", "b", "c"]})

   schema = pa.DataFrameSchema({"column": Column(int)})
   schema.validate(df)

.. testoutput:: non_lazy_validation

    Traceback (most recent call last):
    ...
    SchemaError: expected series 'column' to have type int64, got object


For more complex cases, it is useful to see all of the errors raised during
the ``validate`` call so that you can debug the causes of errors on different
columns and checks. The ``lazy`` keyword argument in the ``validate`` method
of all schemas and schema components gives you the option of doing just this:

.. testcode:: lazy_validation
    :skipif: SKIP_PANDAS_LT_V1

    import logging
    import pandas as pd
    import pandera as pa

    from pandera import Check, Column, DataFrameSchema

    logging.basicConfig(filename='example.log',encoding='utf-8',level=logging.INFO,filemode='w',format='%(message)s')

    schema = pa.DataFrameSchema(
        columns={
            "int_column": Column(int),
            "float_column": Column(float, Check.greater_than(0)),
            "str_column": Column(str, Check.equal_to("a")),
            "date_column": Column(pa.DateTime),
        },
        strict=True
    )

    df = pd.DataFrame({
        "int_column": ["a", "b", "c"],
        "float_column": [0, 1, 2],
        "str_column": ["a", "b", "d"],
        "unknown_column": None,
    })

    schema.validate(df, lazy=True)

.. testoutput:: lazy_validation
    :skipif: SKIP_PANDAS_LT_V1

    Traceback (most recent call last):
    ...
    pandera.errors.SchemaErrors: A total of 5 schema errors were found.

    Error Counts
    ------------
    - column_not_in_schema: 1
    - column_not_in_dataframe: 1
    - schema_component_check: 3

    Schema Error Summary
    --------------------
                                                             failure_cases  n_failure_cases
    schema_context  column       check
    DataFrameSchema <NA>         column_in_dataframe         [date_column]                1
                                 column_in_schema         [unknown_column]                1
    Column          float_column dtype('float64')                  [int64]                1
                    int_column   dtype('int64')                   [object]                1
                    str_column   equal_to(a)                        [b, d]                2

    Usage Tip
    ---------

    Directly inspect all errors by catching the exception:

    ```
    try:
        schema.validate(dataframe, lazy=True)
    except SchemaErrors as err:
        err.failure_case_summary # summary of schema errors
        err.failure_cases  # dataframe of schema errors
        err.data  # invalid dataframe
    ```

As you can see from the output above, a :class:`~pandera.errors.SchemaErrors`
exception is raised with printing a summary of the error counts and failure cases
caught by the schema. You can also see from the **Usage Tip** that you can
catch these errors, and inspect the failure cases in a more granular form while
still logging a summary of the failure cases. As opposed to printing the output,
the errors can be logged as part of your workflow:


.. testcode:: lazy_validation
    :skipif: SKIP_PANDAS_LT_V1

    try:
        schema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        logging.info('Failure case summary:')
        logging.info('\n'+err.failure_case_summary.to_string()) 
        logging.info('\nSchema errors and failure cases:')
        logging.info('\n'+err.failure_cases.to_string())
        logging.info('\nDataFrame object that failed validation:')
        logging.info('\n'+err.data.to_string())

The log file, example.log will contain:

.. testoutput:: lazy_validation
    :skipif: SKIP_PANDAS_LT_V1

    Failure case summary:

         column                 check   count
    0  float_column  dtype('float64')       1
    1  float_column   greater_than(0)       1
    2    int_column    dtype('int64')       1
    3    str_column       equal_to(a)       2

    Schema errors and failure cases:
        schema_context        column                check check_number  \
    0  DataFrameSchema          None     column_in_schema         None
    1  DataFrameSchema          None  column_in_dataframe         None
    2           Column    int_column       dtype('int64')         None
    3           Column  float_column     dtype('float64')         None
    4           Column  float_column      greater_than(0)            0
    5           Column    str_column          equal_to(a)            0
    6           Column    str_column          equal_to(a)            0

         failure_case index
    0  unknown_column  None
    1     date_column  None
    2          object  None
    3           int64  None
    4               0     0
    5               b     1
    6               d     2

    DataFrame object that failed validation:
      int_column  float_column str_column unknown_column
    0          a             0          a           None
    1          b             1          b           None
    2          c             2          d           None

If you want to append the failure case information to the DataFrame object that failed validation,
include ``err.data_with_error_info`` as part of your logging. The output will inform you which
columns failed in your DataFrame:

.. testoutput:: lazy_validation
    :skipif: SKIP_PANDAS_LT_V1


    DataFrame object that failed validation with error info:

    check                                     equal_to(a) greater_than(0)         
    int_column  float_column str_column index
        a             0          a      0             NaN    float_column
        b             1          b      1      str_column             NaN
        c             2          d      2      str_column             NaN


To convert the DataFrame output in a different file formats like csv ,xml and html use the syntax below
    try:
        schema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        logging.info('Data in CSV format:')
        logging.info('\n'+err.data.to_csv()) 
        logging.info('\nData in HTML format:')
        logging.info('\n'+err.data.to_html())
        logging.info('\nData in XML format:')
        logging.info('\n'+err.data.to_xml())
      
