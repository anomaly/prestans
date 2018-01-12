import unittest

from prestans.exception import InvalidChoiceError
from prestans.exception import InvalidFormatError
from prestans.exception import MinimumLengthError
from prestans.exception import MaximumLengthError
from prestans.exception import RequiredAttributeError
from prestans.types import String


class StringUnitTest(unittest.TestCase):

    def test_required(self):
        string = String(required=True)
        self.assertTrue(string.required)
        self.assertRaises(RequiredAttributeError, string.validate, None)
        self.assertRaises(RequiredAttributeError, string.validate, "")
        self.assertEqual(string.validate("apple"), "apple")

    def test_not_required(self):
        string = String(required=False)
        self.assertFalse(string.required)
        self.assertEqual(string.validate("apple"), "apple")
        self.assertEqual(string.validate(""), "")
        self.assertEqual(string.validate(None), None)

    def test_invalid_types(self):
        types = String()
        self.assertEqual(types.validate("orange"), "orange")
        self.assertEqual(types.validate(1), "1")
        self.assertEqual(types.validate(1.0), "1.0")
        self.assertEqual(types.validate(True), "True")

    def test_default(self):
        default = "orange"
        string = String(required=True, default=default)
        self.assertEquals(string.default, default)
        self.assertEqual(string.validate(None), "orange")
        self.assertEqual(string.validate("apple"), "apple")

        string = String(required=False, default=default)
        self.assertEquals(string.default, default)
        self.assertEquals(string.validate(None), "orange")
        self.assertEquals(string.validate("apple"), "apple")

    def test_min_less_than_max(self):
        self.assertRaises(ValueError, String, min_length=2, max_length=1)

    def test_non_positive_min_length(self):
        self.assertRaises(ValueError, String, min_length=-1)

    def test_min_length(self):
        string = String(min_length=5, max_length=7)
        self.assertEquals(string.min_length, 5)
        self.assertRaises(MinimumLengthError, string.validate, "1234")
        self.assertEqual(string.validate("12345"), "12345")

    def test_non_positive_max_length(self):
        self.assertRaises(ValueError, String, max_length=-1)

    def test_max_length(self):
        string = String(min_length=5, max_length=7)
        self.assertEquals(string.max_length, 7)
        self.assertRaises(MaximumLengthError, string.validate, "123456789")
        self.assertEqual(string.validate("1234567"), "1234567")

    def test_format(self):
        format_string = "[0-9]{2}[a-z]{5}[0-9]{3}"
        string = String(format=format_string)
        self.assertEquals(string.format, format_string)
        self.assertRaises(InvalidFormatError, string.validate, "cat")
        self.assertRaises(InvalidFormatError, string.validate, "ab45678as")
        self.assertEqual(string.validate("12abcde123"), "12abcde123")
        self.assertEqual(string.validate("89uwxyz789"), "89uwxyz789")

    def test_choices(self):
        choices = ["apple", "banana"]
        string = String(choices=choices)
        self.assertEquals(string.choices, choices)
        self.assertRaises(InvalidChoiceError, string.validate, "orange")
        self.assertRaises(InvalidChoiceError, string.validate, "grape")

        self.assertEqual(string.validate("apple"), "apple")
        self.assertEqual(string.validate("banana"), "banana")

    def test_description(self):
        string = String()
        self.assertIsNone(string.description)

        description = "Description"
        string = String(description=description)
        self.assertEquals(string.description, description)

    def test_trim(self):
        string = String()
        self.assertTrue(string.trim)

        string = String(trim=False)
        self.assertFalse(string.trim)

    def test_utf_encoding(self):
        string = String()
        self.assertEquals(string.utf_encoding, "utf-8")

        string = String(utf_encoding="utf-16")
        self.assertEquals(string.utf_encoding, "utf-16")

    def test_blueprint(self):
        string = String(
            default="default",
            min_length=1,
            max_length=10,
            required=False,
            format="[a-z]{1, 5}",
            choices=["a", "b", "c"],
            utf_encoding="utf-16",
            description="Description",
            trim=False
        )

        blueprint = string.blueprint()
        self.assertEquals(blueprint["type"], "string")
        self.assertEquals(blueprint["constraints"]["default"], string.default)
        self.assertEquals(blueprint["constraints"]["min_length"], string.min_length)
        self.assertEquals(blueprint["constraints"]["max_length"], string.max_length)
        self.assertEquals(blueprint["constraints"]["required"], string.required)
        self.assertEquals(blueprint["constraints"]["format"], string.format)
        self.assertEquals(blueprint["constraints"]["utf_encoding"], string.utf_encoding)
        self.assertEquals(blueprint["constraints"]["description"], string.description)
        self.assertEquals(blueprint["constraints"]["trim"], string.trim)
