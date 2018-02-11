import json
import plistlib
import sys
import unittest

from prestans import exception
from prestans.serializer import Base
from prestans.serializer import JSON
from prestans.serializer import XMLPlist
from prestans.types import DataCollection


class SerializerBaseUnitTest(unittest.TestCase):

    def test_dumps(self):
        self.assertRaises(NotImplementedError, Base().dumps, None)

    def test_handler_body_type(self):
        self.assertRaises(NotImplementedError, Base().handler_body_type)

    def test_content_type(self):
        self.assertRaises(NotImplementedError, Base().content_type)


class SerializerJSONUnitTest(unittest.TestCase):

    def test_dumps_success(self):
        self.assertEqual(JSON().dumps({}), json.dumps({}))
        self.assertEqual(JSON().dumps({"key": "value"}), json.dumps({"key": "value"}))

    def test_dumps_fail(self):
        class PythonObject(object):
            pass

        self.assertRaises(exception.SerializationFailedError, JSON().dumps, PythonObject)

    def test_handler_body_type(self):
        self.assertEquals(JSON().handler_body_type(), DataCollection)

    def test_content_type(self):
        self.assertEquals(JSON().content_type(), "application/json")


class SerializerPListUnitTest(unittest.TestCase):

    @unittest.skipIf(sys.version_info >= (3,), "python2 only")
    def test_dumps_success_py2(self):
        self.assertEqual(XMLPlist().dumps({}), plistlib.writePlistToString({}))
        self.assertEqual(XMLPlist().dumps({"key": "value"}), plistlib.writePlistToString({"key": "value"}))

    @unittest.skipIf(sys.version_info < (3,), "python3 only")
    def test_dumps_success_py3(self):
        self.assertEqual(XMLPlist().dumps({}), plistlib.dumps({}))
        self.assertEqual(XMLPlist().dumps({"key": "value"}), plistlib.dumps({"key": "value"}))

    @unittest.skipIf(sys.version_info >= (3,), "python2 only")
    def test_dumps_fail_py2(self):
        class PythonObject(object):
            pass

        self.assertRaises(exception.SerializationFailedError, XMLPlist().dumps, PythonObject)

    @unittest.skipIf(sys.version_info < (3,), "python3 only")
    def test_dumps_fail_py3(self):
        class PythonObject(object):
            pass

        self.assertRaises(exception.SerializationFailedError, XMLPlist().dumps, PythonObject)

    def test_handler_body_type(self):
        self.assertEquals(XMLPlist().handler_body_type(), DataCollection)

    def test_content_type(self):
        self.assertEquals(XMLPlist().content_type(), "application/xml")
