import unittest

from prestans import exception
from prestans.types import String


class StringUnitTest(unittest.TestCase):

    def test_required(self):
        required_default = String()
        self.assertTrue(required_default.required)

        required_true = String(required=True)
        self.assertTrue(required_true.required)

        required_false = String(required=False)
        self.assertFalse(required_false.required)

    def test_default(self):
        default_default = String()
        self.assertIsNone(default_default.default)

        default_value = String(required=True, default="orange")
        self.assertEquals(default_value.default, "orange")

    def test_min_less_than_max(self):
        self.assertRaises(ValueError, String, min_length=2, max_length=1)

    def test_non_positive_min_length(self):
        self.assertRaises(ValueError, String, min_length=-1)

    def test_min_length(self):
        string = String(min_length=5, max_length=7)
        self.assertEquals(string.min_length, 5)
        self.assertRaises(exception.MinimumLengthError, string.validate, "1234")
        self.assertEqual(string.validate("12345"), "12345")

    def test_non_positive_max_length(self):
        self.assertRaises(ValueError, String, max_length=-1)

    def test_max_length(self):
        string = String(min_length=5, max_length=7)
        self.assertEquals(string.max_length, 7)
        self.assertRaises(exception.MaximumLengthError, string.validate, "123456789")
        self.assertEqual(string.validate("1234567"), "1234567")

    def test_format(self):
        format_string = "[0-9]{2}[a-z]{5}[0-9]{3}"
        string = String(format=format_string)
        self.assertEquals(string.format, format_string)
        self.assertRaises(exception.InvalidFormatError, string.validate, "cat")
        self.assertRaises(exception.InvalidFormatError, string.validate, "ab45678as")
        self.assertEqual(string.validate("12abcde123"), "12abcde123")
        self.assertEqual(string.validate("89uwxyz789"), "89uwxyz789")

    def test_choices(self):
        choices = ["apple", "banana"]
        string = String(choices=choices)
        self.assertEquals(string.choices, choices)
        self.assertRaises(exception.InvalidChoiceError, string.validate, "orange")
        self.assertRaises(exception.InvalidChoiceError, string.validate, "grape")

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

    def test_validate(self):

        # test required
        self.assertRaises(exception.RequiredAttributeError, String(required=True).validate, None)
        self.assertRaises(exception.RequiredAttributeError, String(required=True).validate, "")
        self.assertEqual(String(required=True).validate("apple"), "apple")

        # test not required
        self.assertEqual(String(required=False).validate("apple"), "apple")
        self.assertEqual(String(required=False).validate(""), "")
        self.assertEqual(String(required=False).validate(None), None)

        # test invalid types
        self.assertEqual(String().validate("orange"), "orange")
        self.assertEqual(String().validate(1), "1")
        self.assertEqual(String().validate(1.0), "1.0")
        self.assertEqual(String().validate(True), "True")

        # test default required
        self.assertEqual(String(required=True, default="orange").validate(None), "orange")
        self.assertEqual(String(required=True, default="orange").validate("apple"), "apple")

        # test default not required
        self.assertEquals(String(required=False, default="orange").validate(None), "orange")
        self.assertEquals(String(required=False, default="orange").validate("apple"), "apple")

        # test unicode encode
        self.assertEquals(String().validate(u"unicode"), u"unicode")

        # test str parse
        self.assertEquals(String().validate("string"), "string")

        # test int
        self.assertEquals(String().validate(1234), "1234")

        # check custom str which is broken
        class Custom(object):

            def __str__(self):
                return None

        self.assertRaises(exception.ParseFailedError, String().validate, Custom())
