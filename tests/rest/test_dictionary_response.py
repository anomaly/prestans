import logging
import unittest

from prestans.rest import DictionaryResponse
from prestans.serializer import JSON


class DictionaryResponseTest(unittest.TestCase):

    def test_body(self):
        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )
        self.assertEquals(dict_response.body, [])

        self.assertRaises(TypeError, setattr, dict_response, "body", "string")

        sample_dict = {
            "key": "value"
        }
        dict_response.body = sample_dict
        self.assertEquals(dict_response.body, sample_dict)

    def test_call(self):
        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )
        dict_response._set_serializer_by_mime_type("application/json")
        dict_response.body = {"key": "value"}

        def start_response(status, headerlist):
            pass

        response = dict_response({}, start_response)
        self.assertEquals(response, ['{"key": "value"}'])
        self.assertEquals(dict_response.content_length, 16)

        from prestans.serializer import Base

        class BadSerializer(Base):

            def dumps(self, serializable_object):
                return None

            def handler_body_type(self):
                raise NotImplementedError

            def content_type(self):
                return "bad/serializer"

        dict_response.register_serializers([BadSerializer()])
        dict_response._set_serializer_by_mime_type("bad/serializer")
        self.assertRaises(TypeError, dict_response, {}, start_response)

