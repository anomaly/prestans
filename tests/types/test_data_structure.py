import unittest

from prestans.types import DataStructure


class DataStructureUnitTest(unittest.TestCase):

    def test_validate(self):
        data_structure = DataStructure()
        self.assertRaises(NotImplementedError, data_structure.validate, "data")

    def test_as_serializable(self):
        data_structure = DataStructure()
        self.assertRaises(NotImplementedError, data_structure.as_serializable, "data")
