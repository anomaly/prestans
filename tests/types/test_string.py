import unittest

from prestans.exception import InvalidChoiceError
from prestans.exception import InvalidFormatError
from prestans.exception import MinimumLengthError
from prestans.exception import MaximumLengthError
from prestans.exception import RequiredAttributeError
from prestans.types import String


class StringUnitTest(unittest.TestCase):

    def test_required(self):
        required = String(required=True)
        self.assertRaises(RequiredAttributeError, required.validate, None)
        self.assertRaises(RequiredAttributeError, required.validate, "")
        self.assertEqual(required.validate("apple"), "apple")

    def test_not_required(self):
        not_required = String(required=False)
        self.assertEqual(not_required.validate("apple"), "apple")
        self.assertEqual(not_required.validate(""), "")
        self.assertEqual(not_required.validate(None), None)

    def test_types(self):
        types = String()
        self.assertEqual(types.validate("orange"), "orange")
        self.assertEqual(types.validate(1), "1")
        self.assertEqual(types.validate(1.0), "1.0")
        self.assertEqual(types.validate(True), "True")

    def test_default(self):
        default = String(default="orange")
        self.assertEqual(default.validate(None), "orange")
        self.assertEqual(default.validate("apple"), "apple")

    def test_min_length(self):
        length = String(min_length=5, max_length=7)
        self.assertRaises(MinimumLengthError, length.validate, "1234")
        self.assertEqual(length.validate("12345"), "12345")

    def test_max_length(self):
        length = String(min_length=5, max_length=7)
        self.assertRaises(MaximumLengthError, length.validate, "123456789")
        self.assertEqual(length.validate("1234567"), "1234567")

    def test_format(self):
        format = String(format="[0-9]{2}[a-z]{5}[0-9]{3}")
        self.assertRaises(InvalidFormatError, format.validate, "cat")
        self.assertRaises(InvalidFormatError, format.validate, "ab45678as")
        self.assertEqual(format.validate("12abcde123"), "12abcde123")
        self.assertEqual(format.validate("89uwxyz789"), "89uwxyz789")

    def test_choices(self):
        choices = String(choices=["apple", "banana"])
        self.assertRaises(InvalidChoiceError, choices.validate, "orange")
        self.assertRaises(InvalidChoiceError, choices.validate, "grape")

        self.assertEqual(choices.validate("apple"), "apple")
        self.assertEqual(choices.validate("banana"), "banana")
