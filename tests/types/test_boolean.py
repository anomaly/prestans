import unittest

from prestans.exception import RequiredAttributeError
from prestans.types import Boolean


class BooleanUnitTest(unittest.TestCase):

    def test_types(self):
        types = Boolean()
        types.validate("string")

    def test_required(self):
        required = Boolean(required=True)
        self.assertRaises(RequiredAttributeError, required.validate, None)

    def test_not_required(self):
        not_required = Boolean(required=False)

    def test_default(self):
        default_true = Boolean(default=True)
        self.assertEqual(default_true.validate(None), True)
        self.assertEqual(default_true.validate(False), False)

        default_false = Boolean(default=False)
        self.assertEqual(default_false.validate(None), False)
        self.assertEqual(default_false.validate(True), True)
