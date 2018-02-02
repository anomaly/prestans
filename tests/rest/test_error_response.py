import unittest

from prestans import exception
from prestans.rest import ErrorResponse
from prestans.serializer import JSON


class ErrorResponseTest(unittest.TestCase):

    def test_init(self):
        raised_exception = exception.NoEndpointError()
        json_serializer = JSON()

        error_response = ErrorResponse(raised_exception, json_serializer)

    def test_trace(self):
        pass

    def test_append_to_trace(self):
        pass

    def test_call(self):
        pass

    def test_str(self):
        pass
