from datetime import time
from mock import patch
import unittest

from prestans import exception
from prestans.types import Time

NOW = time(12, 34, 11)
UTC_NOW = time(13, 35, 12)


class TimeUnitTest(unittest.TestCase):

    def test_default(self):
        default_none = Time()
        self.assertIsNone(default_none.default)

        default_now = Time(default=Time.NOW)
        self.assertEqual(default_now.default, Time.NOW)

        default_now_utc = Time(default=Time.UTC_NOW)
        self.assertEqual(default_now_utc.default, Time.UTC_NOW)

        default_time = Time(default=time(11, 11, 11))
        self.assertEqual(default_time.default, time(11, 11, 11))

        self.assertRaises(TypeError, Time, default="string")
        self.assertRaises(TypeError, Time, default=23)

    def test_required(self):
        time_type = Time()
        self.assertTrue(time_type.required)

        time_type = Time(required=True)
        self.assertTrue(time_type.required)

    def test_not_required(self):
        time_type = Time(required=False)
        self.assertFalse(time_type.required)

    def test_format(self):
        default_format = Time()
        self.assertEqual(default_format.format, Time.DEFAULT_FORMAT)

        custom_format = Time(format="%H:%M:%S %p")
        self.assertEqual(custom_format.format, "%H:%M:%S %p")

    def test_description(self):
        time_type = Time()
        self.assertIsNone(time_type.description)

        time_type = Time(description="description")
        self.assertEqual(time_type.description, "description")

    def test_blueprint(self):
        time_type = Time()
        blueprint = time_type.blueprint()
        self.assertEqual(blueprint["type"], "time")
        self.assertEqual(blueprint["constraints"]["default"], time_type.default)
        self.assertEqual(blueprint["constraints"]["required"], time_type.required)
        self.assertEqual(blueprint["constraints"]["format"], time_type.format)
        self.assertEqual(blueprint["constraints"]["description"], time_type.description)

        time_type = Time(default=time(11, 11, 11), required=False, format="%H:%M:%S %p", description="description")
        blueprint = time_type.blueprint()
        self.assertEqual(blueprint["type"], "time")
        self.assertEqual(blueprint["constraints"]["default"], time(11, 11, 11))
        self.assertEqual(blueprint["constraints"]["required"], False)
        self.assertEqual(blueprint["constraints"]["format"], "%H:%M:%S %p")
        self.assertEqual(blueprint["constraints"]["description"], "description")

    def test_validate(self):

        # test that not required accepts None
        not_required = Time(required=False)
        self.assertEqual(not_required.validate(None), None)

        # test that required throws exception for None
        required = Time(required=True)
        self.assertRaises(exception.RequiredAttributeError, required.validate, None)

        # test that required accepts time value
        default_time = Time(required=True, default=time(11, 11, 11))
        self.assertEqual(default_time.validate(None), time(11, 11, 11))

        # test that required makes use of NOW constant
        with patch('prestans.types.time_prestans.datetime') as datetime:
            datetime.now.return_value = NOW

            default_now = Time(required=True, default=Time.NOW)
            self.assertEqual(default_now.validate(None), NOW)
            datetime.now.assert_called()

        # test that not required makes use of NOW constant
        with patch('prestans.types.time_prestans.datetime') as datetime:
            datetime.now.return_value = NOW

            default_now = Time(required=False, default=Time.NOW)
            self.assertEqual(default_now.validate(None), NOW)
            datetime.now.assert_called()

        # test that required makes use of UTC_NOW constant
        with patch('prestans.types.time_prestans.datetime') as datetime:
            datetime.utcnow.return_value = UTC_NOW

            default_utc_now = Time(required=True, default=Time.UTC_NOW)
            self.assertEqual(default_utc_now.validate(None), UTC_NOW)
            datetime.utcnow.assert_called()

        # test that not required makes use of UTC_NOW constant
        with patch('prestans.types.time_prestans.datetime') as datetime:
            datetime.utcnow.return_value = UTC_NOW

            default_utc_now = Time(required=False, default=Time.UTC_NOW)
            self.assertEqual(default_utc_now.validate(None), UTC_NOW)
            datetime.utcnow.assert_called()

        # test that invalid type is rejected
        invalid_type = Time()
        self.assertRaises(exception.ParseFailedError, invalid_type.validate, 345)

        # test that invalid string is rejected
        self.assertRaises(exception.ParseFailedError, Time().validate, "invalid")

        # test that valid string can be parsed
        self.assertEqual(Time().validate("12:34:00"), time(12, 34, 00))

    def test_as_serializable(self):
        default_format = Time()
        self.assertRaises(exception.InvalidTypeError, default_format.as_serializable, "string")
        self.assertEqual(default_format.as_serializable(time(11, 34, 1)), "11:34:01")

        custom_format = Time(format="%H:%M:%S %p")
        self.assertRaises(exception.InvalidTypeError, custom_format.as_serializable, "string")
        self.assertEqual(custom_format.as_serializable(time(10, 51, 13)), "10:51:13 AM")
