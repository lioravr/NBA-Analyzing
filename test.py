import random
from typing_extensions import assert_never
from backend.function import *
from visualization.main import *
import unittest as pa

#
# test the visualization function:
#


def test_gen_scoring_efficiency_plot():
    year= random.randint(1977,2022)	
    assert gen_scoring_efficiency_plot(year)
    assert(pa.TestCase.assertIsNotNone)


#
# test the backend function:
#


def test_load_data():
    year= random.randint(1977,2022)	
    df = load_data(year,'play-by-play')
    assert df.isnull().values.any() == False

