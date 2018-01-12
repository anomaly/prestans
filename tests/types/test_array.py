import unittest

from prestans.types import Array
from prestans.types import Boolean
from prestans.types import Float
from prestans.types import Integer
from prestans.types import String


class ArrayUnitTest(unittest.TestCase):

    def test_is_scalar(self):
        string_array = Array(element_template=String())
        self.assertTrue(string_array.is_scalar)

        integer_array = Array(element_template=Integer())
        self.assertTrue(integer_array.is_scalar)

        boolean_array = Array(element_template=Boolean())
        self.assertTrue(boolean_array.is_scalar)

        float_array = Array(element_template=Float())
        self.assertTrue(float_array.is_scalar)

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def test_append(self):
        pass
