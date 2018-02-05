import unittest

from prestans.http import STATUS
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
        pass


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
        pass


class ExceptionRequestException(unittest.TestCase):

    def test_init(self):
        pass


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
        pass


class ExceptionDeSerializationFailedError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionAttributeFilterDiffers(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionInconsistentPersistentDataError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionDataValidationException(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionRequiredAttributeError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionParseFailedError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionLessThanMinimumError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionMoreThanMaximumError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionInvalidChoiceError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionMinimumLengthError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionMaximumLengthError(unittest.TestCase):

    def test_init(self):
        pass


class ExceptionInvalidTypeError(unittest.TestCase):

    def test_init(self):
        pass


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
        response = exception.ResponseException(STATUS.OK, "message")
        self.assertEquals(response.http_status, STATUS.OK)
        self.assertEquals(response.message, "message")


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
