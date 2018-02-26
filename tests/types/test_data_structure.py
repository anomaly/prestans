import unittest

from prestans.types import DataStructure


class DataStructureUnitTest(unittest.TestCase):

    def test_blueprint(self):
        self.assertRaises(NotImplementedError, DataStructure().blueprint)

    def test_validate(self):
        self.assertRaises(NotImplementedError, DataStructure().validate, "data")

    def test_as_serializable(self):
        self.assertRaises(NotImplementedError, DataStructure().as_serializable, "data")
