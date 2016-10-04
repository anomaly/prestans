import unittest

from prestans.parser import VerbConfig
from prestans.types import (
    Array,
    Integer,
    Boolean,
    String,
    Float
)

array_of_strings = Array(element_template=String())
array_of_booleans = Array(element_template=Boolean())
array_of_integers = Array(element_template=Integer())
array_of_floats = Array(element_template=Float())

class TestVerbConfig(unittest.TestCase):
    def test_verb_config_does_not_except_when_given_scalar_array_response_template(self):
        try:
            VerbConfig(response_template=array_of_strings)
        except:
            self.fail()
        try:
            VerbConfig(response_template=array_of_integers)
        except:
            self.fail()
        try:
            VerbConfig(response_template=array_of_floats)
        except:
            self.fail()
        try:
            VerbConfig(response_template=array_of_booleans)
        except:
            self.fail()