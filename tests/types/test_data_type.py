import unittest

from prestans.types import DataType


class DataTypeUnitTest(unittest.TestCase):

    def test_blueprint(self):
        self.assertRaises(NotImplementedError, DataType().blueprint)

    def test_validate(self):
        self.assertRaises(NotImplementedError, DataType().validate, "data")