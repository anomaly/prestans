import logging
import unittest

from prestans.rest import DictionaryResponse
from prestans.serializer import JSON


class DictionaryResponseBody(unittest.TestCase):

    def test_empty_body_returns_empty_list(self):
        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )
        self.assertEquals(dict_response.body, [])

    def test_non_dict_body_raises_type_error(self):
        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )
        self.assertRaises(TypeError, setattr, dict_response, "body", "string")

    def test_dict_body_is_correctly_set(self):
        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )

        sample_dict = {
            "key": "value"
        }
        dict_response.body = sample_dict
        self.assertEquals(dict_response.body, sample_dict)


class DictionaryResponseCall(unittest.TestCase):

    def test_call_with_non_dictionary_body_raises_type_error(self):
        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )
        dict_response._set_serializer_by_mime_type("application/json")

        def start_response(status, headerlist):
            pass

        self.assertRaises(TypeError, dict_response.__call__, environ={}, start_response=start_response)

    def test_call_with_dictionary(self):
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

    def test_call_serializer_returns_non_string_type_raises_type_error(self):
        from prestans.serializer import Base

        dict_response = DictionaryResponse(
            charset="utf-8",
            logger=logging.getLogger(),
            serializers=[JSON()],
            default_serializer=JSON()
        )
        dict_response._set_serializer_by_mime_type("application/json")
        dict_response.body = {"key": "value"}

        class BadSerializer(Base):

            def dumps(self, serializable_object):
                return None

            def handler_body_type(self):
                raise NotImplementedError

            def content_type(self):
                return "bad/serializer"

        def start_response(status, headerlist):
            pass

        bad_serializer = BadSerializer()

        dict_response.register_serializers([bad_serializer])
        dict_response._set_serializer_by_mime_type("bad/serializer")
        self.assertEquals(dict_response.selected_serializer, bad_serializer)
        self.assertRaises(TypeError, dict_response.__call__, environ={}, start_response=start_response)
