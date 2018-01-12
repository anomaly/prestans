import unittest

from prestans.types import Model
from prestans.types import String


class ModelUnitTest(unittest.TestCase):

    class TestModel(Model):
        string = String(required=True, max_length=10)

    def test_default(self):
        pass

    def test_choices(self):
        pass
