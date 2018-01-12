import unittest

from prestans.types import DataCollection


class DataCollectionUnitTest(unittest.TestCase):

    def test_validate(self):
        data_collection = DataCollection()
        self.assertRaises(NotImplementedError, data_collection.validate, "data")

    def test_as_serializable(self):
        data_collection = DataCollection()
        self.assertRaises(NotImplementedError, data_collection.as_serializable, "data")

    def test_get_attribute_filter(self):
        data_collection = DataCollection()
        self.assertRaises(NotImplementedError, data_collection.get_attribute_filter)
