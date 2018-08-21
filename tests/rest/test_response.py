import logging
import unittest

from prestans.rest import Response
from prestans.serializer import JSON
from prestans.serializer import XMLPlist


class ResponseInit(unittest.TestCase):

    def test_logger(self):
        logger = logging.basicConfig()

        response = Response(
            charset="utf=8",
            logger=logger,
            serializers=[],
            default_serializer=None
        )
        self.assertEquals(response.logger, logger)

    def test_serializers(self):
        logger = logging.basicConfig()

        response = Response(
            charset="utf=8",
            logger=logger,
            serializers=[JSON()],
            default_serializer=None
        )
        self.assertEquals(response.supported_mime_types, ["application/json"])
        self.assertEquals(response.supported_mime_types_str, "application/json")

        response = Response(
            charset="utf=8",
            logger=logger,
            serializers=[JSON(), XMLPlist()],
            default_serializer=None
        )
        self.assertEquals(response.supported_mime_types, ["application/json", "application/xml"])
        self.assertEquals(response.supported_mime_types_str, "application/json,application/xml")

    def test_default_serializer(self):
        json_ser = JSON()

        response = Response(
            charset="utf=8",
            logger=logging.basicConfig(),
            serializers=[json_ser],
            default_serializer=json_ser
        )
        self.assertEquals(response.default_serializer, json_ser)

    def test_prestans_version(self):
        response = Response(
            charset="utf=8",
            logger=logging.basicConfig(),
            serializers=[JSON()],
            default_serializer=None
        )
        from prestans import __version__
        self.assertTrue("Prestans-Version" in response.headers)
        self.assertEquals(response.headers["Prestans-Version"], __version__)


class ResponseMinify(unittest.TestCase):

    def test_default_false(self):
        response = Response(
            charset="utf=8",
            logger=logging.basicConfig(),
            serializers=[JSON()],
            default_serializer=None
        )
        self.assertFalse(response.minify)

    def test_set_false(self):
        response = Response(
            charset="utf=8",
            logger=logging.basicConfig(),
            serializers=[JSON()],
            default_serializer=None
        )
        response.minify = False
        self.assertFalse(response.minify)

    def test_set_true(self):
        response = Response(
            charset="utf=8",
            logger=logging.basicConfig(),
            serializers=[JSON()],
            default_serializer=None
        )
        response.minify = True
        self.assertTrue(response.minify)