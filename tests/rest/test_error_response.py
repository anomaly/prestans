import unittest

from prestans import exception
from prestans.http import STATUS
from prestans.rest import ErrorResponse
from prestans.serializer import JSON


class ErrorResponseTest(unittest.TestCase):

    def test_init(self):
        raised_exception = exception.NoEndpointError()
        json_serializer = JSON()

        error_response = ErrorResponse(raised_exception, json_serializer)
        self.assertEquals(error_response._exception, raised_exception)

    def test_call_default(self):
        raised_exception = exception.NoEndpointError()
        json_serializer = JSON()

        error_response = ErrorResponse(raised_exception, json_serializer)

        def start_response(status, headers):
            pass

        environ = {}

        self.assertEquals(
            error_response(environ, start_response),
            [b'{"code": 404, "message": "API does not provide this end-point", "trace": []}']
        )

    def test_call_custom(self):
        from prestans import types

        class CustomModel(types.Model):
            custom_message = types.String()

        custom_error = CustomModel()
        custom_error.custom_message = "custom"

        class CustomError(exception.ResponseException):

            def __init__(self, response_model=None):
                super(CustomError, self).__init__(STATUS.FORBIDDEN, "custom", response_model)

        raised_exception = CustomError(custom_error)
        json_serializer = JSON()

        error_response = ErrorResponse(raised_exception, json_serializer)

        def start_response(status, headers):
            pass

        environ = {}

        self.assertEquals(error_response(environ, start_response), [b'{"custom_message": "custom"}'])
