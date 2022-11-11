import pandas as pd
import pytest

from pandera import (
    Check,
)

test_data = [ [['a','a','a','b','b','b','c','c','c'],['a','b','c'],True],
              [['1','1','1','2','2','2','3','3','3'],['1','2','3'],True],
             ]

@pytest.mark.parametrize("duplicate_vals, unique_vals, is_unique", test_data)

def test_unique_values_eq(duplicate_vals, unique_vals, is_unique):
    pd_series = pd.Series(duplicate_vals)
    pd_series_check = Check.unique_values_eq(unique_vals)(pd_series)

    assert pd_series_check.check_passed == is_unique

test_data = [ [['a','a','a','b','b','b','c','c','c'],['a','a','c'],False],
              [['1','1','1','2','2','2','3','3','3'],['1','1','3'],False],
             ]

@pytest.mark.parametrize("duplicate_vals, unique_vals, is_unique", test_data)

def test_unique_values_uneq(duplicate_vals, unique_vals, is_unique):
    pd_series = pd.Series(duplicate_vals)
    pd_series_check = Check.unique_values_eq(unique_vals)(pd_series)

    assert pd_series_check.check_passed == is_unique

test_data = [ (('aaabbbccc','aaabbb'),6,10),
              (('111222','111222333'),6,10),
             ]

@pytest.mark.parametrize("str_vals, min_val, max_val", test_data)

def test_str_length(str_vals, min_val, max_val):
    pd_series = pd.Series(str_vals)
    pd_series_check = Check.str_length(min_val,max_val)(pd_series)

    assert pd_series_check.check_passed == True

test_data = [ (('aaabbbccc','aaabbb'),'aaa'),
              (('aaab','aaacccbbb'),'aaa'),
             ]

@pytest.mark.parametrize("str_vals, str_starts_with", test_data)

def test_str_startswith(str_vals, str_starts_with):
    pd_series = pd.Series(str_vals)
    pd_series_check = Check.str_startswith(str_starts_with)(pd_series)

    assert pd_series_check.check_passed == True

test_data = [ (('aaabbbccc','aaaccc'),'cc'),
              (('aaab','aaacccbbb'),'b'),
             ]

@pytest.mark.parametrize("str_vals, str_ends_with", test_data)

def test_str_endswith(str_vals, str_ends_with):
    pd_series = pd.Series(str_vals)
    pd_series_check = Check.str_endswith(str_ends_with)(pd_series)

    assert pd_series_check.check_passed == True

test_data = [ (('aaabbbccc','aaaccc'),'cc'),
              (('aaab','cccaaabbb'),'ab'),
              (('1112223','1222333'),'223'),
             ]

@pytest.mark.parametrize("str_vals, str_contains", test_data)

def test_str_contains(str_vals, str_contains):
    pd_series = pd.Series(str_vals)
    pd_series_check = Check.str_contains(str_contains)(pd_series)

    assert pd_series_check.check_passed == True

test_data = [ (('aaaccc','aaaccc'),'aaaccc'),
              (('aaab','aaab'),'aaab'),
              (('1222333','1222333'),'1222333'),
             ]

@pytest.mark.parametrize("str_vals, str_matches", test_data)

def test_str_matches(str_vals, str_matches):
    pd_series = pd.Series(str_vals)
    pd_series_check = Check.str_matches(str_matches)(pd_series)

    assert pd_series_check.check_passed == True
