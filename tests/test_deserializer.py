import json
import plistlib
import unittest

from prestans.deserializer import Base
from prestans.deserializer import JSON
from prestans.deserializer import XMLPlist
from prestans import exception


class DeserializerBaseUnitTest(unittest.TestCase):

    def test_loads(self):
        self.assertRaises(NotImplementedError, Base().loads, None)

    def test_content_type(self):
        self.assertRaises(NotImplementedError, Base().content_type)


class DeserializerJSONUnitTest(unittest.TestCase):

    @unittest.skip
    def test_loads_success(self):
        self.assertEqual(JSON().loads("{}"), json.loads("{}"))
        self.assertEqual(JSON().loads({"key": "value"}), json.loads({"key": "value"}))

    def test_loads_fail(self):
        self.assertRaises(exception.DeSerializationFailedError, JSON().loads, "string")

    def test_content_type(self):
        self.assertEquals(JSON().content_type(), "application/json")


class DeserializerPListUnitTest(unittest.TestCase):

    @unittest.skip
    def test_loads_success(self):
        empty_object = {}
        key_value_object = {"key": "value"}

        self.assertEqual(XMLPlist().loads(plistlib.writePlistToString(empty_object)), empty_object)
        self.assertEqual(XMLPlist().loads(
            plistlib.writePlistToString(key_value_object)),
            plistlib.writePlistToString(key_value_object)
        )

    def test_loads_fail(self):
        self.assertRaises(exception.DeSerializationFailedError, XMLPlist().loads, "string")

    def test_content_type(self):
        self.assertEquals(XMLPlist().content_type(), "application/xml")
