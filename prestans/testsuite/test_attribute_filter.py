import sys
import unittest
import os

from prestans.parser import AttributeFilter
from prestans.types import (
    Array,
    String,
    Integer,
    Boolean,
    Float
)

array_of_strings = Array(element_template=String())
array_of_booleans = Array(element_template=Boolean())
array_of_integers = Array(element_template=Integer())
array_of_floats = Array(element_template=Float())


class TestAttributeFilter(unittest.TestCase):
    def test_from_model_with_string_array_should_return_attribute_filter(self):
        self._scalar_array_test(array_of_strings)

    def test_from_model_with_boolean_array_should_return_attribute_filter(self):
        self._scalar_array_test(array_of_booleans)

    def test_from_model_with_integer_array_should_return_attribute_filter(self):
        self._scalar_array_test(array_of_integers)

    def test_from_model_with_float_array_should_return_attribute_filter(self):
        self._scalar_array_test(array_of_floats)

    def _scalar_array_test(self, array_type):
        attribute_filter = AttributeFilter.from_model(model_instance=array_type, default_value=True, should_be=True)


if __name__ == '__main__':
    unittest.main()
