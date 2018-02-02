from datetime import datetime
from mock import patch
import unittest

from prestans import exception
from prestans.types import DateTime

NOW = datetime(2018, 2, 14, 12, 34, 11)
UTC_NOW = datetime(2018, 3, 21, 13, 35, 12)


class DateTimeUnitTest(unittest.TestCase):

    def test_default(self):
        default_none = DateTime()
        self.assertIsNone(default_none.default)

        default_now = DateTime(default=DateTime.NOW)
        self.assertEquals(default_now.default, DateTime.NOW)

        default_now_utc = DateTime(default=DateTime.UTC_NOW)
        self.assertEquals(default_now_utc.default, DateTime.UTC_NOW)

        default_time = DateTime(default=datetime(11, 11, 11))
        self.assertEquals(default_time.default, datetime(11, 11, 11))

        self.assertRaises(TypeError, DateTime, default="string")
        self.assertRaises(TypeError, DateTime, default=23)

    def test_required(self):
        required_default = DateTime()
        self.assertTrue(required_default.required)

        required_true = DateTime(required=True)
        self.assertTrue(required_true.required)

        required_false = DateTime(required=False)
        self.assertFalse(required_false.required)

    def test_format(self):
        default_format = DateTime()
        self.assertEquals(default_format.format, DateTime.DEFAULT_FORMAT)

        custom_format = DateTime(format="%H:%M:%S %p")
        self.assertEquals(custom_format.format, "%H:%M:%S %p")

    def test_description(self):
        datetime_type = DateTime()
        self.assertIsNone(datetime_type.description)

        datetime_type = DateTime(description="description")
        self.assertEquals(datetime_type.description, "description")

    def test_timezone(self):
        timezone_default = DateTime()
        self.assertFalse(timezone_default.timezone)

        timezone_false = DateTime()
        self.assertFalse(timezone_false.timezone)

        timezone_true = DateTime(timezone=True)
        self.assertTrue(timezone_true.timezone)

    def test_utc(self):
        utc_default = DateTime()
        self.assertFalse(utc_default.utc)

        utc_false = DateTime()
        self.assertFalse(utc_false.utc)

        utc_true = DateTime(utc=True)
        self.assertTrue(utc_true.utc)

    def test_blueprint(self):
        datetime_type = DateTime()
        blueprint = datetime_type.blueprint()
        self.assertEquals(blueprint["type"], "datetime")
        self.assertEquals(blueprint["constraints"]["default"], None)
        self.assertEquals(blueprint["constraints"]["required"], True)
        self.assertEquals(blueprint["constraints"]["format"], DateTime.DEFAULT_FORMAT)
        self.assertEquals(blueprint["constraints"]["description"], None)
        self.assertEquals(blueprint["constraints"]["timezone"], False)
        self.assertEquals(blueprint["constraints"]["utc"], False)

        datetime_type = DateTime(
            default=datetime(11, 11, 11),
            required=False,
            format="%H:%M:%S %p",
            description="description",
            timezone=True,
            utc=True
        )
        blueprint = datetime_type.blueprint()
        self.assertEquals(blueprint["type"], "datetime")
        self.assertEquals(blueprint["constraints"]["default"], datetime(11, 11, 11))
        self.assertEquals(blueprint["constraints"]["required"], False)
        self.assertEquals(blueprint["constraints"]["format"], "%H:%M:%S %p")
        self.assertEquals(blueprint["constraints"]["description"], "description")
        self.assertEquals(blueprint["constraints"]["timezone"], True)
        self.assertEquals(blueprint["constraints"]["utc"], True)

    def test_validate(self):
        # test that not required accepts None
        not_required = DateTime(required=False)
        self.assertEquals(not_required.validate(None), None)

        # test that required throws exception for None
        required = DateTime(required=True)
        self.assertRaises(exception.RequiredAttributeError, required.validate, None)

        # test that required accepts time value
        default_time = DateTime(required=True, default=datetime(2018, 11, 11, 11, 11, 11))
        self.assertEquals(default_time.validate(None), datetime(2018, 11, 11, 11, 11, 11))

        # test that required makes use of NOW constant
        with patch('prestans.types.datetime_prestans.datetime') as imported_datetime:
            imported_datetime.now.return_value = NOW

            default_now = DateTime(required=True, default=DateTime.NOW)
            self.assertEquals(default_now.validate(None), NOW)
            imported_datetime.now.assert_called()

        # test that not required makes use of NOW constant
        with patch('prestans.types.datetime_prestans.datetime') as imported_datetime:
            imported_datetime.now.return_value = NOW

            default_now = DateTime(required=False, default=DateTime.NOW)
            self.assertEquals(default_now.validate(None), NOW)
            imported_datetime.now.assert_called()

        # test that required makes use of UTC_NOW constant
        with patch('prestans.types.datetime_prestans.datetime') as imported_datetime:
            imported_datetime.utcnow.return_value = UTC_NOW

            default_utc_now = DateTime(required=True, default=DateTime.UTC_NOW)
            self.assertEquals(default_utc_now.validate(None), UTC_NOW)
            imported_datetime.utcnow.assert_called()

        # test that not required makes use of UTC_NOW constant
        with patch('prestans.types.datetime_prestans.datetime') as imported_datetime:
            imported_datetime.utcnow.return_value = UTC_NOW

            default_utc_now = DateTime(required=False, default=DateTime.UTC_NOW)
            self.assertEquals(default_utc_now.validate(None), UTC_NOW)
            imported_datetime.utcnow.assert_called()

        # test that default value is used when it is a datetime
        default_datetime = DateTime(required=False, default=datetime(2018, 1, 1, 10, 11, 12))
        self.assertEquals(default_datetime.validate(None), datetime(2018, 1, 1, 10, 11, 12))

        # test that invalid type is rejected
        invalid_type = DateTime()
        self.assertRaises(exception.ParseFailedError, invalid_type.validate, 345)

        # test that invalid string is rejected
        self.assertRaises(exception.ParseFailedError, DateTime().validate, "invalid")

        # test that valid string can be parsed
        self.assertEquals(DateTime().validate("2018-01-04 12:34:00"), datetime(2018, 1, 4, 12, 34, 00))

    def test_as_serializable(self):
        default_format = DateTime()
        self.assertRaises(exception.InvalidTypeError, default_format.as_serializable, "string")
        self.assertEquals(default_format.as_serializable(datetime(2018, 3, 20, 11, 12, 13)), "2018-03-20 11:12:13")

        custom_format = DateTime(format="%Y-%m-%d %H:%M:%S %p")
        self.assertRaises(exception.InvalidTypeError, custom_format.as_serializable, "string")
        self.assertEquals(custom_format.as_serializable(datetime(2018, 4, 15, 10, 12, 14)), "2018-04-15 10:12:14 AM")
