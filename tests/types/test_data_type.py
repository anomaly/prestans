import unittest

from prestans.types import DataType


class DataTypeUnitTest(unittest.TestCase):

    def test_validate(self):
        data_type = DataType()
        self.assertRaises(NotImplementedError, data_type.validate, "data")