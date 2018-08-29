import unittest

from prestans.http import STATUS
from prestans.http import VERB
from prestans import exception


class ExceptionBase(unittest.TestCase):

    def test_http_status(self):
        base_value = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEquals(base_value.http_status, STATUS.OK)

        base_value.http_status = STATUS.NO_CONTENT
        self.assertEquals(base_value.http_status, STATUS.NO_CONTENT)

    def test_stack_trace(self):
        base = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEquals(base.stack_trace, [])

    def test_push_trace(self):
        pass

    def test_message(self):
        base_value = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEquals(base_value.message, "message")

    def test_str(self):
        base = exception.Base(http_status=STATUS.OK, message="message")
        self.assertEquals(base.http_status, STATUS.OK)
        self.assertEquals(str(base.message), "message")


class ExceptionUnsupportedVocabularyError(unittest.TestCase):

    def test_init(self):
        unsupported_vocabulary_error = exception.UnsupportedVocabularyError(
            accept_header="accept",
            supported_types=["a", "b", "c"]
        )
        self.assertEquals(unsupported_vocabulary_error.http_status, STATUS.NOT_IMPLEMENTED)
        self.assertEquals(unsupported_vocabulary_error.message, "Unsupported vocabulary in the Accept header")

        stack_trace = [{
            "accept_header": "accept",
            "supported_types": ["a", "b", "c"]
        }]
        self.assertEquals(unsupported_vocabulary_error.stack_trace, stack_trace)


class ExceptionUnsupportedContentTypeError(unittest.TestCase):

    def test_init(self):
        unsupported_content_type = exception.UnsupportedContentTypeError("text/plain", "application/json")
        self.assertEquals(unsupported_content_type.http_status, STATUS.NOT_IMPLEMENTED)
        self.assertEquals(unsupported_content_type.message, "Unsupported Content-Type in Request")

        stack_trace = [{
            "requested_type": "text/plain",
            "supported_types": "application/json"
        }]

        self.assertEquals(unsupported_content_type.stack_trace, stack_trace)


class ExceptionValidationError(unittest.TestCase):

    def test_init(self):
        validation_error = exception.ValidationError(
            message="message",
            attribute_name="attribute",
            value="value",
            blueprint={"key": "value"}
        )
        self.assertEquals(validation_error.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(validation_error.message, "message")
        self.assertEquals(validation_error.stack_trace, [
            {
                "attribute_name": "attribute",
                "value": "value",
                "message": "message",
                "blueprint": {"key": "value"}
            }
        ])
        self.assertEquals(str(validation_error), "attribute message")


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

        self.assertEquals(handler_exception.http_status, STATUS.FORBIDDEN)
        self.assertEquals(handler_exception.message, "message")
        self.assertEquals(handler_exception.request, request)
        self.assertEquals(handler_exception.log_message, 'GET https://localhost:8080/url chrome "message"')
        self.assertEquals(str(handler_exception), 'GET https://localhost:8080/url chrome "message"')

        handler_exception_without_request = exception.HandlerException(STATUS.NOT_FOUND, "message")
        self.assertEquals(handler_exception_without_request.http_status, STATUS.NOT_FOUND)
        self.assertEquals(handler_exception_without_request.message, "message")
        self.assertEquals(handler_exception_without_request.log_message, "message")
        self.assertEquals(str(handler_exception_without_request), "message")


class ExceptionRequestException(unittest.TestCase):

    def test_init(self):
        request_exception = exception.RequestException(STATUS.BAD_REQUEST, "bad request")
        self.assertEquals(request_exception.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(request_exception.message, "bad request")


class ExceptionUnimplementedVerbError(unittest.TestCase):

    def test_init(self):
        unimplemented_verb = exception.UnimplementedVerbError("GET")
        self.assertEquals(unimplemented_verb.http_status, STATUS.NOT_IMPLEMENTED)
        self.assertEquals(unimplemented_verb.message, "API does not implement the HTTP Verb")
        self.assertEquals(unimplemented_verb.stack_trace, [{"verb": "GET"}])


class ExceptionNoEndpointError(unittest.TestCase):

    def test_init(self):
        no_endpoint = exception.NoEndpointError()
        self.assertEquals(no_endpoint.http_status, STATUS.NOT_FOUND)
        self.assertEquals(no_endpoint.message, "API does not provide this end-point")


class ExceptionAuthenticationError(unittest.TestCase):

    def test_init(self):
        authentication = exception.AuthenticationError()
        self.assertEquals(authentication.http_status, STATUS.UNAUTHORIZED)
        self.assertEquals(authentication.message, "Authentication Error; service is only available to authenticated")

        authentication_custom = exception.AuthenticationError("Custom message")
        self.assertEquals(authentication_custom.http_status, STATUS.UNAUTHORIZED)
        self.assertEquals(authentication_custom.message, "Custom message")


class ExceptionAuthorizationError(unittest.TestCase):

    def test_init(self):
        authorization = exception.AuthorizationError("Role")
        self.assertEquals(authorization.http_status, STATUS.FORBIDDEN)
        self.assertEquals(authorization.message, "Role is not allowed to access this resource")


class ExceptionSerializationFailedError(unittest.TestCase):

    def test_init(self):
        serialization_failed_error = exception.SerializationFailedError("format")
        self.assertEquals(serialization_failed_error.http_status, STATUS.NOT_FOUND)
        self.assertEquals(serialization_failed_error.message, "Serialization failed: format")
        self.assertEquals(str(serialization_failed_error), "Serialization failed: format")


class ExceptionDeSerializationFailedError(unittest.TestCase):

    def test_init(self):
        deserialization_failed_error = exception.DeSerializationFailedError("format")
        self.assertEquals(deserialization_failed_error.http_status, STATUS.NOT_FOUND)
        self.assertEquals(deserialization_failed_error.message, "DeSerialization failed: format")
        self.assertEquals(str(deserialization_failed_error), "DeSerialization failed: format")


class ExceptionAttributeFilterDiffers(unittest.TestCase):

    def test_init(self):
        attribute_filter_differs = exception.AttributeFilterDiffers(["cat", "dog"])
        self.assertEquals(attribute_filter_differs.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(
            attribute_filter_differs.message,
            "attribute filter contains attributes (cat, dog) that are not part of template"
        )


class ExceptionInconsistentPersistentDataError(unittest.TestCase):

    def test_init(self):
        error = exception.InconsistentPersistentDataError("name", "error message")
        self.assertEquals(error.http_status, STATUS.INTERNAL_SERVER_ERROR)
        self.assertEquals(error.message, "Data Adapter failed to validate stored data on the server")
        self.assertEquals(
            str(error),
            "DataAdapter failed to adapt name, Data Adapter failed to validate stored data on the server"
        )
        self.assertEquals(error.stack_trace, [{'exception_message': "error message", 'attribute_name': "name"}])


class ExceptionDataValidationException(unittest.TestCase):

    def test_init(self):
        exp = exception.DataValidationException("message")
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "message")


class ExceptionRequiredAttributeError(unittest.TestCase):

    def test_init(self):
        exp = exception.RequiredAttributeError()
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "attribute is required and does not provide a default value")


class ExceptionParseFailedError(unittest.TestCase):

    def test_init(self):
        default_msg = exception.ParseFailedError()
        self.assertEquals(default_msg.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(default_msg.message, "Parser Failed")

        custom_msg = exception.ParseFailedError("custom")
        self.assertEquals(custom_msg.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(custom_msg.message, "custom")


class ExceptionLessThanMinimumError(unittest.TestCase):

    def test_init(self):
        exp = exception.LessThanMinimumError(3, 5)
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "3 is less than the allowed minimum of 5")


class ExceptionMoreThanMaximumError(unittest.TestCase):

    def test_init(self):
        exp = exception.MoreThanMaximumError(5, 3)
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "5 is more than the allowed maximum of 3")


class ExceptionInvalidChoiceError(unittest.TestCase):

    def test_init(self):
        exp = exception.InvalidChoiceError(3, [1, 2, 5])
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "value 3 is not one of these choices 1, 2, 5")


class ExceptionMinimumLengthError(unittest.TestCase):

    def test_init(self):
        exp = exception.MinimumLengthError("dog", 5)
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "length of value: dog has to be greater than 5")


class ExceptionMaximumLengthError(unittest.TestCase):

    def test_init(self):
        exp = exception.MaximumLengthError("dog", 2)
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "length of value: dog has to be less than 2")


class ExceptionInvalidTypeError(unittest.TestCase):

    def test_init(self):
        exp = exception.InvalidTypeError("str", "int")
        self.assertEquals(exp.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(exp.message, "data type str given, expected int")


class ExceptionMissingParameterError(unittest.TestCase):

    def test_init(self):
        missing_parameter = exception.MissingParameterError()
        self.assertEquals(missing_parameter.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(missing_parameter.message, "missing parameter")


class ExceptionInvalidFormatError(unittest.TestCase):

    def test_init(self):
        invalid_format = exception.InvalidFormatError("cat")
        self.assertEquals(invalid_format.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(invalid_format.message, "invalid value cat provided")


class ExceptionInvalidMetaValueError(unittest.TestCase):

    def test_init(self):
        invalid_meta_value = exception.InvalidMetaValueError()
        self.assertEquals(invalid_meta_value.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(invalid_meta_value.message, "invalid meta value")


class ExceptionUnregisteredAdapterError(unittest.TestCase):

    def test_init(self):
        unregistered_adapter = exception.UnregisteredAdapterError("namespace.Model")
        self.assertEquals(unregistered_adapter.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(unregistered_adapter.message, "no registered adapters for data model namespace.Model")


class ExceptionResponseException(unittest.TestCase):

    def test_init(self):
        from prestans.types import Model
        class MyModel(Model):
            pass

        my_model = MyModel()
        response = exception.ResponseException(STATUS.OK, "message", my_model)
        self.assertEquals(response.http_status, STATUS.OK)
        self.assertEquals(response.message, "message")
        self.assertEquals(response.response_model, my_model)

        self.assertRaises(TypeError, exception.ResponseException, STATUS.INTERNAL_SERVER_ERROR, "message", "string")


class ExceptionServiceUnavailable(unittest.TestCase):

    def test_init(self):
        service_unavailable = exception.ServiceUnavailable()
        self.assertEquals(service_unavailable.http_status, STATUS.SERVICE_UNAVAILABLE)
        self.assertEquals(service_unavailable.message, "Service Unavailable")


class ExceptionBadRequest(unittest.TestCase):

    def test_init(self):
        bad_request = exception.BadRequest()
        self.assertEquals(bad_request.http_status, STATUS.BAD_REQUEST)
        self.assertEquals(bad_request.message, "Bad Request")


class ExceptionConflict(unittest.TestCase):

    def test_init(self):
        conflict = exception.Conflict()
        self.assertEquals(conflict.http_status, STATUS.CONFLICT)
        self.assertEquals(conflict.message, "Conflict")


class ExceptionNotFound(unittest.TestCase):

    def test_init(self):
        not_found = exception.NotFound()
        self.assertEquals(not_found.http_status, STATUS.NOT_FOUND)
        self.assertEquals(not_found.message, "Not Found")


class ExceptionUnauthorized(unittest.TestCase):

    def test_init(self):
        unauthorized = exception.Unauthorized()
        self.assertEquals(unauthorized.http_status, STATUS.UNAUTHORIZED)
        self.assertEquals(unauthorized.message, "Unauthorized")


class ExceptionMovedPermanently(unittest.TestCase):

    def test_init(self):
        moved_permanently = exception.MovedPermanently()
        self.assertEquals(moved_permanently.http_status, STATUS.MOVED_PERMANENTLY)
        self.assertEquals(moved_permanently.message, "Moved Permanently")


class ExceptionPaymentRequired(unittest.TestCase):

    def test_init(self):
        payment_required = exception.PaymentRequired()
        self.assertEquals(payment_required.http_status, STATUS.PAYMENT_REQUIRED)
        self.assertEquals(payment_required.message, "Payment Required")


class ExceptionForbidden(unittest.TestCase):

    def test_init(self):
        forbidden = exception.Forbidden()
        self.assertEquals(forbidden.http_status, STATUS.FORBIDDEN)
        self.assertEquals(forbidden.message, "Forbidden")


class ExceptionInternalServerError(unittest.TestCase):

    def test_init(self):
        internal_server_error = exception.InternalServerError()
        self.assertEquals(internal_server_error.http_status, STATUS.INTERNAL_SERVER_ERROR)
        self.assertEquals(internal_server_error.message, "Internal Server Error")
