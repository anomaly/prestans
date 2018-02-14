import unittest

from prestans.types import DataCollection


class DataCollectionUnitTest(unittest.TestCase):

    def test_blueprint(self):
        self.assertRaises(NotImplementedError, DataCollection().blueprint)

    def test_validate(self):
        self.assertRaises(NotImplementedError, DataCollection().validate, "data")

    def test_as_serializable(self):
        self.assertRaises(NotImplementedError, DataCollection().as_serializable, "data")

    def test_attribute_rewrite_map(self):
        self.assertRaises(NotImplementedError, DataCollection().attribute_rewrite_map)

    def test_attribute_rewrite_reverse_map(self):
        self.assertRaises(NotImplementedError, DataCollection().attribute_rewrite_reverse_map)

    def test_get_attribute_filter(self):
        self.assertRaises(NotImplementedError, DataCollection().get_attribute_filter)
