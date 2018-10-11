from datetime import date
from mock import patch
import unittest

from prestans import exception
from prestans.types import Date

TODAY = date(2018, 2, 14)


class DateUnitTest(unittest.TestCase):

    def test_default(self):
        default_none = Date()
        self.assertIsNone(default_none.default)

        default_now = Date(default=Date.TODAY)
        self.assertEqual(default_now.default, Date.TODAY)

        default_time = Date(default=date(11, 11, 11))
        self.assertEqual(default_time.default, date(11, 11, 11))

        self.assertRaises(TypeError, Date, default="string")
        self.assertRaises(TypeError, Date, default=23)

    def test_required(self):
        required_default = Date()
        self.assertTrue(required_default.required)

        required_true = Date(required=True)
        self.assertTrue(required_true.required)

        required_false = Date(required=False)
        self.assertFalse(required_false.required)

    def test_format(self):
        format_default = Date()
        self.assertEqual(format_default.format, Date.DEFAULT_FORMAT)

        format_custom = Date(format="%Y/%m/%d")
        self.assertEqual(format_custom.format, "%Y/%m/%d")

    def test_description(self):
        description_default = Date()
        self.assertIsNone(description_default.description)

        description_value = Date(description="description")
        self.assertEqual(description_value.description, "description")

    def test_blueprint(self):
        date_type = Date()
        blueprint = date_type.blueprint()
        self.assertEqual(blueprint["type"], "date")
        self.assertEqual(blueprint["constraints"]["default"], None)
        self.assertEqual(blueprint["constraints"]["required"], True)
        self.assertEqual(blueprint["constraints"]["format"], Date.DEFAULT_FORMAT)
        self.assertEqual(blueprint["constraints"]["description"], None)

        date_type = Date(
            default=date(2018, 11, 4),
            required=False,
            format="%H:%M:%S %p",
            description="description"
        )
        blueprint = date_type.blueprint()
        self.assertEqual(blueprint["type"], "date")
        self.assertEqual(blueprint["constraints"]["default"], date(2018, 11, 4))
        self.assertEqual(blueprint["constraints"]["required"], False)
        self.assertEqual(blueprint["constraints"]["format"], "%H:%M:%S %p")
        self.assertEqual(blueprint["constraints"]["description"], "description")

    def test_validate(self):
        # test that not required accepts None
        not_required = Date(required=False)
        self.assertEqual(not_required.validate(None), None)

        # test that required throws exception for None
        required = Date(required=True)
        self.assertRaises(exception.RequiredAttributeError, required.validate, None)

        # test that required accepts date value
        default_date = Date(required=True, default=date(2018, 11, 11))
        self.assertEqual(default_date.validate(None), date(2018, 11, 11))

        # test that required makes use of NOW constant
        with patch('prestans.types.date.date') as imported_datetime:
            imported_datetime.today.return_value = TODAY

            default_now = Date(required=True, default=Date.TODAY)
            self.assertEqual(default_now.validate(None), TODAY)
            imported_datetime.today.assert_called()

        # test that not required makes use of NOW constant
        with patch('prestans.types.date.date') as imported_datetime:
            imported_datetime.today.return_value = TODAY

            default_now = Date(required=False, default=Date.TODAY)
            self.assertEqual(default_now.validate(None), TODAY)
            imported_datetime.today.assert_called()

        # test that default value is used when it is a date
        default_datetime = Date(required=False, default=date(2018, 1, 1))
        self.assertEqual(default_datetime.validate(None), date(2018, 1, 1))

        # test that invalid type is rejected
        invalid_type = Date()
        self.assertRaises(exception.ParseFailedError, invalid_type.validate, 345)

        # test that invalid string is rejected
        self.assertRaises(exception.ParseFailedError, Date().validate, "invalid")

        # test that valid string can be parsed
        self.assertEqual(Date().validate("2018-01-04"), date(2018, 1, 4))

    def test_as_serializable(self):
        default_format = Date()
        self.assertRaises(exception.InvalidTypeError, default_format.as_serializable, "string")
        self.assertEqual(default_format.as_serializable(date(2018, 3, 20)), "2018-03-20")

        custom_format = Date(format="%Y/%m/%d")
        self.assertRaises(exception.InvalidTypeError, custom_format.as_serializable, "string")
        self.assertEqual(custom_format.as_serializable(date(2018, 4, 15)), "2018/04/15")
