import unittest

from prestans.http import STATUS
from prestans.http import VERB
from prestans import exception


class ExceptionBase(unittest.TestCase):

    def test_http_status(self):
        base_value = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEqual(base_value.http_status, STATUS.OK)

        base_value.http_status = STATUS.NO_CONTENT
        self.assertEqual(base_value.http_status, STATUS.NO_CONTENT)

    def test_stack_trace(self):
        base = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEqual(base.stack_trace, [])

    def test_push_trace(self):
        pass

    def test_message(self):
        base_value = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEqual(base_value.message, "message")

    def test_str(self):
        base = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEqual(base.http_status, STATUS.OK)
        self.assertEqual(str(base.message), "message")


class ExceptionUnsupportedVocabularyError(unittest.TestCase):

    def test_init(self):
        unsupported_vocabulary_error = exception.UnsupportedVocabularyError(
            accept_header="accept",
            supported_types=["a", "b", "c"]
        )
        self.assertEqual(unsupported_vocabulary_error.http_status, STATUS.NOT_IMPLEMENTED)
        self.assertEqual(unsupported_vocabulary_error.message, "Unsupported vocabulary in the Accept header")

        stack_trace = [{
            "accept_header": "accept",
            "supported_types": ["a", "b", "c"]
        }]
        self.assertEqual(unsupported_vocabulary_error.stack_trace, stack_trace)


class ExceptionUnsupportedContentTypeError(unittest.TestCase):

    def test_init(self):
        unsupported_content_type = exception.UnsupportedContentTypeError("text/plain", "application/json")
        self.assertEqual(unsupported_content_type.http_status, STATUS.NOT_IMPLEMENTED)
        self.assertEqual(unsupported_content_type.message, "Unsupported Content-Type in Request")

        stack_trace = [{
            "requested_type": "text/plain",
            "supported_types": "application/json"
        }]

        self.assertEqual(unsupported_content_type.stack_trace, stack_trace)


class ExceptionValidationError(unittest.TestCase):

    def test_init(self):
        validation_error = exception.ValidationError(
            message="message",
            attribute_name="attribute",
            value="value",
            blueprint={"key": "value"}
        )
        self.assertEqual(validation_error.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(validation_error.message, "message")
        self.assertEqual(validation_error.stack_trace, [
            {
                "attribute_name": "attribute",
                "value": "value",
                "message": "message",
                "blueprint": {"key": "value"}
            }
        ])
        self.assertEqual(str(validation_error), "attribute message")


class ExceptionHandlerException(unittest.TestCase):

    def test_init(self):
        from prestans.rest import Request
        import logging
        logging.basicConfig()
        self.logger = logging.getLogger("prestans")

        from prestans.deserializer import JSON
        charset = "utf-8"
        serializers = [JSON()]
        default_serializer = JSON()

        request_environ = {
            "REQUEST_METHOD": VERB.GET,
            "PATH_INFO": "/url",
            "HTTP_USER_AGENT": "chrome",
            "wsgi.url_scheme": "https",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8080"
        }

        request = Request(
            environ=request_environ,
            charset=charset,
            logger=self.logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        handler_exception = exception.HandlerException(STATUS.FORBIDDEN, "message")
        handler_exception.request = request

        self.assertEqual(handler_exception.http_status, STATUS.FORBIDDEN)
        self.assertEqual(handler_exception.message, "message")
        self.assertEqual(handler_exception.request, request)
        self.assertEqual(handler_exception.log_message, 'GET https://localhost:8080/url chrome "message"')
        self.assertEqual(str(handler_exception), 'GET https://localhost:8080/url chrome "message"')

        handler_exception_without_request = exception.HandlerException(STATUS.NOT_FOUND, "message")
        self.assertEqual(handler_exception_without_request.http_status, STATUS.NOT_FOUND)
        self.assertEqual(handler_exception_without_request.message, "message")
        self.assertEqual(handler_exception_without_request.log_message, "message")
        self.assertEqual(str(handler_exception_without_request), "message")


class ExceptionRequestException(unittest.TestCase):

    def test_init(self):
        request_exception = exception.RequestException(STATUS.BAD_REQUEST, "bad request")
        self.assertEqual(request_exception.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(request_exception.message, "bad request")


class ExceptionUnimplementedVerbError(unittest.TestCase):

    def test_init(self):
        unimplemented_verb = exception.UnimplementedVerbError("GET")
        self.assertEqual(unimplemented_verb.http_status, STATUS.NOT_IMPLEMENTED)
        self.assertEqual(unimplemented_verb.message, "API does not implement the HTTP Verb")
        self.assertEqual(unimplemented_verb.stack_trace, [{"verb": "GET"}])


class ExceptionNoEndpointError(unittest.TestCase):

    def test_init(self):
        no_endpoint = exception.NoEndpointError()
        self.assertEqual(no_endpoint.http_status, STATUS.NOT_FOUND)
        self.assertEqual(no_endpoint.message, "API does not provide this end-point")


class ExceptionAuthenticationError(unittest.TestCase):

    def test_init(self):
        authentication = exception.AuthenticationError()
        self.assertEqual(authentication.http_status, STATUS.UNAUTHORIZED)
        self.assertEqual(authentication.message, "Authentication Error; service is only available to authenticated")

        authentication_custom = exception.AuthenticationError("Custom message")
        self.assertEqual(authentication_custom.http_status, STATUS.UNAUTHORIZED)
        self.assertEqual(authentication_custom.message, "Custom message")


class ExceptionAuthorizationError(unittest.TestCase):

    def test_init(self):
        authorization = exception.AuthorizationError("Role")
        self.assertEqual(authorization.http_status, STATUS.FORBIDDEN)
        self.assertEqual(authorization.message, "Role is not allowed to access this resource")


class ExceptionSerializationFailedError(unittest.TestCase):

    def test_init(self):
        serialization_failed_error = exception.SerializationFailedError("format")
        self.assertEqual(serialization_failed_error.http_status, STATUS.NOT_FOUND)
        self.assertEqual(serialization_failed_error.message, "Serialization failed: format")
        self.assertEqual(str(serialization_failed_error), "Serialization failed: format")


class ExceptionDeSerializationFailedError(unittest.TestCase):

    def test_init(self):
        deserialization_failed_error = exception.DeSerializationFailedError("format")
        self.assertEqual(deserialization_failed_error.http_status, STATUS.NOT_FOUND)
        self.assertEqual(deserialization_failed_error.message, "DeSerialization failed: format")
        self.assertEqual(str(deserialization_failed_error), "DeSerialization failed: format")


class ExceptionAttributeFilterDiffers(unittest.TestCase):

    def test_init(self):
        attribute_filter_differs = exception.AttributeFilterDiffers(["cat", "dog"])
        self.assertEqual(attribute_filter_differs.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(
            attribute_filter_differs.message,
            "attribute filter contains attributes (cat, dog) that are not part of template"
        )


class ExceptionInconsistentPersistentDataError(unittest.TestCase):

    def test_init(self):
        error = exception.InconsistentPersistentDataError("name", "error message")
        self.assertEqual(error.http_status, STATUS.INTERNAL_SERVER_ERROR)
        self.assertEqual(error.message, "Data Adapter failed to validate stored data on the server")
        self.assertEqual(
            str(error),
            "DataAdapter failed to adapt name, Data Adapter failed to validate stored data on the server"
        )
        self.assertEqual(error.stack_trace, [{'exception_message': "error message", 'attribute_name': "name"}])


class ExceptionDataValidationException(unittest.TestCase):

    def test_init(self):
        exp = exception.DataValidationException("message")
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "message")


class ExceptionRequiredAttributeError(unittest.TestCase):

    def test_init(self):
        exp = exception.RequiredAttributeError()
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "attribute is required and does not provide a default value")


class ExceptionParseFailedError(unittest.TestCase):

    def test_init(self):
        default_msg = exception.ParseFailedError()
        self.assertEqual(default_msg.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(default_msg.message, "Parser Failed")

        custom_msg = exception.ParseFailedError("custom")
        self.assertEqual(custom_msg.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(custom_msg.message, "custom")


class ExceptionLessThanMinimumError(unittest.TestCase):

    def test_init(self):
        exp = exception.LessThanMinimumError(3, 5)
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "3 is less than the allowed minimum of 5")


class ExceptionMoreThanMaximumError(unittest.TestCase):

    def test_init(self):
        exp = exception.MoreThanMaximumError(5, 3)
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "5 is more than the allowed maximum of 3")


class ExceptionInvalidChoiceError(unittest.TestCase):

    def test_init(self):
        exp = exception.InvalidChoiceError(3, [1, 2, 5])
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "value 3 is not one of these choices 1, 2, 5")


class ExceptionMinimumLengthError(unittest.TestCase):

    def test_init(self):
        exp = exception.MinimumLengthError("dog", 5)
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "length of value: dog has to be greater than 5")


class ExceptionMaximumLengthError(unittest.TestCase):

    def test_init(self):
        exp = exception.MaximumLengthError("dog", 2)
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "length of value: dog has to be less than 2")


class ExceptionInvalidTypeError(unittest.TestCase):

    def test_init(self):
        exp = exception.InvalidTypeError("str", "int")
        self.assertEqual(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(exp.message, "data type str given, expected int")


class ExceptionMissingParameterError(unittest.TestCase):

    def test_init(self):
        missing_parameter = exception.MissingParameterError()
        self.assertEqual(missing_parameter.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(missing_parameter.message, "missing parameter")


class ExceptionInvalidFormatError(unittest.TestCase):

    def test_init(self):
        invalid_format = exception.InvalidFormatError("cat")
        self.assertEqual(invalid_format.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(invalid_format.message, "invalid value cat provided")


class ExceptionInvalidMetaValueError(unittest.TestCase):

    def test_init(self):
        invalid_meta_value = exception.InvalidMetaValueError()
        self.assertEqual(invalid_meta_value.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(invalid_meta_value.message, "invalid meta value")


class ExceptionUnregisteredAdapterError(unittest.TestCase):

    def test_init(self):
        unregistered_adapter = exception.UnregisteredAdapterError("namespace.Model")
        self.assertEqual(unregistered_adapter.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(unregistered_adapter.message, "no registered adapters for data model namespace.Model")


class ExceptionResponseException(unittest.TestCase):

    def test_init(self):
        from prestans.types import Model
        class MyModel(Model):
            pass

        my_model = MyModel()
        response = exception.ResponseException(STATUS.OK, "message", my_model)
        self.assertEqual(response.http_status, STATUS.OK)
        self.assertEqual(response.message, "message")
        self.assertEqual(response.response_model, my_model)

        self.assertRaises(TypeError, exception.ResponseException, STATUS.INTERNAL_SERVER_ERROR, "message", "string")


class ExceptionServiceUnavailable(unittest.TestCase):

    def test_init(self):
        service_unavailable = exception.ServiceUnavailable()
        self.assertEqual(service_unavailable.http_status, STATUS.SERVICE_UNAVAILABLE)
        self.assertEqual(service_unavailable.message, "Service Unavailable")


class ExceptionBadRequest(unittest.TestCase):

    def test_init(self):
        bad_request = exception.BadRequest()
        self.assertEqual(bad_request.http_status, STATUS.BAD_REQUEST)
        self.assertEqual(bad_request.message, "Bad Request")


class ExceptionConflict(unittest.TestCase):

    def test_init(self):
        conflict = exception.Conflict()
        self.assertEqual(conflict.http_status, STATUS.CONFLICT)
        self.assertEqual(conflict.message, "Conflict")


class ExceptionNotFound(unittest.TestCase):

    def test_init(self):
        not_found = exception.NotFound()
        self.assertEqual(not_found.http_status, STATUS.NOT_FOUND)
        self.assertEqual(not_found.message, "Not Found")


class ExceptionUnauthorized(unittest.TestCase):

    def test_init(self):
        unauthorized = exception.Unauthorized()
        self.assertEqual(unauthorized.http_status, STATUS.UNAUTHORIZED)
        self.assertEqual(unauthorized.message, "Unauthorized")


class ExceptionMovedPermanently(unittest.TestCase):

    def test_init(self):
        moved_permanently = exception.MovedPermanently()
        self.assertEqual(moved_permanently.http_status, STATUS.MOVED_PERMANENTLY)
        self.assertEqual(moved_permanently.message, "Moved Permanently")


class ExceptionPaymentRequired(unittest.TestCase):

    def test_init(self):
        payment_required = exception.PaymentRequired()
        self.assertEqual(payment_required.http_status, STATUS.PAYMENT_REQUIRED)
        self.assertEqual(payment_required.message, "Payment Required")


class ExceptionForbidden(unittest.TestCase):

    def test_init(self):
        forbidden = exception.Forbidden()
        self.assertEqual(forbidden.http_status, STATUS.FORBIDDEN)
        self.assertEqual(forbidden.message, "Forbidden")


class ExceptionInternalServerError(unittest.TestCase):

    def test_init(self):
        internal_server_error = exception.InternalServerError()
        self.assertEqual(internal_server_error.http_status, STATUS.INTERNAL_SERVER_ERROR)
        self.assertEqual(internal_server_error.message, "Internal Server Error")
