# -*- coding: utf-8 -*-
#
#  prestans, A WSGI compliant REST micro-framework
#  http://prestans.org
#
#  Copyright (c) 2015, Anomaly Software Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Anomaly Software nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ANOMALY SOFTWARE BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__all__ = [
    'UnsupportedVocabularyError',
    'UnsupportedContentTypeError',
    'ValidationError',
    'DataValidationException',
    'ParserException',
    'HandlerException',

    #: Parser Exceptions
    'NoEndpointError',
    'SerializationFailed',

    #: Data Validation
    'RequiredAttributeError',
    'ParseFailedError',
    'InvalidValue',
    'LessThanMinimum',
    'MoreThanMaximum',
    'InvalidChoice',
    'UnacceptableLength',
    'InvalidType',
    'InvalidCollection',
    'MissingParameter',
    'InvalidFormat',
    'InvalidMetaValue',
    'UnregisteredAdapter',

    #: Handler exceptions
    'ServiceUnavailable',
    'BadRequest',
    'Conflict',
    'NotFound',
    'Unauthorized',
    'MovedPermanently',
    'PaymentRequired',
    'Forbidden'
]

import prestans
import prestans.http

class Base(Exception):

    def __init__(self, http_status, message):

        self._http_status = http_status
        self._message = message
        self._stack_trace = list()

    @property
    def http_status(self):
        return self._http_status

    @http_status.setter
    def http_status(self, value):
        self._http_status = value

    @property
    def stack_trace(self):
        return self._stack_trace

    def push_trace(self, trace_object):
        self._stack_trace.append(trace_object)

    @property
    def message(self):
        return self._message

    def __unicode__(self):
        return unicode(self._message)

    def __str__(self):
        return unicode(self._message).encode('utf-8')

#:
#: These are top level exceptions that layout tell prestans how
#: the resulting messages are written out to the either the client
#: or the logger
#:
#: None of these exceptions are used directly, look at the sections
#: for usable exceptions.
#:
#: According to PEP 008 all exceptions that are error should have
#: the Error suffix e.g UnsupportedVocabularyError
#: http://www.python.org/dev/peps/pep-0008/#exception-names
#:

class UnsupportedVocabularyError(Base):
    """
    Called if none of the requested vocabularies are supported by the API
    this error message is sent as an HTML document. This exception is the
    only one that breaks serialisation rules.
    """

    def __init__(self, accept_header, supported_types):

        _code = prestans.http.STATUS.NOT_IMPLEMENTED
        _message = "Unsupported vocabulary in the Accept header"
        super(UnsupportedVocabularyError, self).__init__(_code, _message)

        self.push_trace({ 
            'accept_header': str(accept_header),
            'supported_types': supported_types
            })
    
class UnsupportedContentTypeError(Base):
    
    def __init__(self, requested_mime_type, content_type):

        _code = prestans.http.STATUS.NOT_IMPLEMENTED
        _message = "Unsupported Content-Type in Request"
        super(UnsupportedContentTypeError, self).__init__(_code, _message)

        self.push_trace({ 
            'requested_type': requested_mime_type,
            'supported_types': content_type
            })

class ValidationError(Base):
    """
    DataValidationException are Exceptions raised if prestans fails
    to validate data inbound or out using rules defined in Models.

    These contains a stack trace to indicate the depth of the error.
    E.g Model has Sub Model that has attribute which failed to validate.

    Each exception uses an HTTP status code and is sent to the client.
    """
    def __init__(self, message, attribute_name, value, blueprint):

        super(ValidationError, self).__init__(prestans.http.STATUS.BAD_REQUEST, message)
        self._attribute_name = attribute_name
        self._value = str(value)

        self.append_validation_trace(blueprint)

    def append_validation_trace(self, blueprint):
        self.push_trace({
            'attribute_name': self._attribute_name,
            'value': self._value,
            'message': self._message,
            'blueprint': blueprint
            })

    #:
    #: The following are overridden to ensure sensible logging messages
    #:

    def __unicode__(self):
        _loggable_message = "%s %s" % (self._attribute_name, self._message)
        return unicode(_loggable_message)

    def __str__(self):
        _loggable_message = "%s %s" % (self._attribute_name, self._message)
        return unicode(_loggable_message).encode('utf-8')

class ParserException(Base):
    """
    ParserException are Exceptions raised if prestans fails to parse
    a request; these generally revolve around the Content-Types or 
    missing payload. Specific parsing messages are of type DataValidationException
    """
    def __init__(self, code, message):
        super(ParserException, self).__init__(code, message)

class HandlerException(Base):
    """
    HandlerExceptions are Exceptions that are raised by handlers of the
    REST application. REST encourages the use different error codes to
    denote what the error is.

    E.g Use 404 to denote that a reqeusted doesn't exists on the server.

    If one of these exceptions do not match your user case; you are free
    construct your own error message and use an error code from outlined
    in prestans.http
    """
    def __init__(self, code, message):
        super(HandlerException, self).__init__(code, message)

#:
#: Parser Exception
#:

class UnimplementedVerbError(ParserException):

    def __init__(self, verb_name):

        _code = prestans.http.STATUS.NOT_IMPLEMENTED
        _message = "API does not implement the HTTP Verb"
        super(UnimplementedVerbError, self).__init__(_code, _message)

        self.push_trace({ 
            'verb': verb_name,
            })

class NoEndpointError(ParserException):

    def __init__(self):

        _code = prestans.http.STATUS.NOT_FOUND
        _message = "API does not provide this end-point"
        super(NoEndpointError, self).__init__(_code, _message)

class AuthenticationError(ParserException):

    def __init__(self, message=None):

        _code = prestans.http.STATUS.UNAUTHORIZED
    
        _message = message
        if _message is None:
            _message = "Authentication Error; service is only available to authenticated"
    
        super(AuthenticationError, self).__init__(_code, _message)

class AuthorizationError(ParserException):

    def __init__(self, role_name):

        _code = prestans.http.STATUS.FORBIDDEN
        _message = "%s is not allowed to access this resource"
        super(AuthorizationError, self).__init__(_code, _message)


class SerializationFailedError(ParserException):

    def __init__(self, format):

        _code = prestans.http.STATUS.NOT_FOUND
        _message = "Serialization failed: %s" % format
        super(SerializationFailedError, self).__init__(_code, _message)

class DeSerializationFailedError(ParserException):
    
    def __init__(self, format):

        _code = prestans.http.STATUS.NOT_FOUND
        _message = "DeSerialization failed: %s" % format
        super(DeSerializationFailedError, self).__init__(_code, _message)

class AttributeFilterDiffers(ParserException):
    """
    AttributeFilter initialised from request input does not conform to
    the configured template.
    """

    def __init__(self, attribute_list):

        _code = prestans.http.STATUS.BAD_REQUEST
        _message = "attribute filter does not contain attributes (%s) that are not part of template" % (', '.join(attribute_list))
        super(AttributeFilterDiffers, self).__init__(_code, _message)

        self.push_trace({ 
            'rejected_attribute_list': attribute_list,
            })

class InconsistentPersistentDataError(Base):
    """
    Raised by Data Adapters if validation of stored data fails. Extra information is
    written out to the server log and the client is returned a 500 response.

    Practical expectation is that this should not occur; however if REST rules have 
    changed since the instantiation of the system.
    """

    def __init__(self, attribute_name, exception_message):
        _code = prestans.http.STATUS.INTERNAL_SERVER_ERROR
        _message = "Data Adapter failed to validate stored data on the server"
        super(InconsistentPersistentDataError, self).__init__(_code, _message)

        self._attribute_name = attribute_name

        self.push_trace({
            'exception_message': exception_message,
            'attribute_name': attribute_name
            })

    def __str__(self):
        return "DataAdapter failed to adapt %s, %s" % (self._attribute_name, self.message)

#:
#: Data Validation
#: 

class DataValidationException(Base):

    def __init__(self, message):
        super(DataValidationException, self).__init__(prestans.http.STATUS.BAD_REQUEST, message)

class RequiredAttributeError(DataValidationException):

    def __init__(self, attribute_name=None):
        _message = "attribute is required and does not provide a default value"
        super(RequiredAttributeError, self).__init__(_message)

class ParseFailedError(DataValidationException):
    
    def __init__(self, message="Parser Failed"):
        _message = message
        super(ParseFailedError, self).__init__(_message)

class LessThanMinimumError(DataValidationException):
    
    def __init__(self, value, allowed_min):
        _message = "%i is less than the allowed minimum of %i" % (value, allowed_min)
        super(LessThanMinimumError, self).__init__(_message)

class MoreThanMaximumError(DataValidationException):

    def __init__(self, value, allowed_max):
        _message = "%i is more than the allowed maximum %i" % (value, allowed_max)
        super(MoreThanMaximumError, self).__init__(_message)

class InvalidChoiceError(DataValidationException):

    def __init__(self, value, allowed_choices):
        _message = "value is not one of these choices %s" % str(allowed_choices).strip('[]')
        super(InvalidChoiceError, self).__init__(_message)

class UnacceptableLengthError(DataValidationException):
    
    def __init__(self, value, minimum, maximum):
        _message = "value has to be %i and %i" % (minimum, maximum)
        super(UnacceptableLengthError, self).__init__(_message)

class InvalidType(DataValidationException):
    
    def __init__(self, value, type_name):
        _message = "invalid data type %s" % type_name
        super(InvalidType, self).__init__(_message)

class MissingParameterError(DataValidationException):

    def __init__(self):
        _message = "missing parameter"
        super(MissingParameterError, self).__init__(_message)

class InvalidFormatError(DataValidationException):
    
    def __init__(self, value):
        _message = "invalid value %s provided" % value
        super(InvalidFormatError, self).__init__(_message)

class InvalidMetaValueError(DataValidationException):

    def __init__(self):
        _message = "invalid meta value"
        super(InvalidMetaValueError, self).__init__(_message)

class UnregisteredAdapterError(DataValidationException):

    def __init__(self):
        _message = "no registered adapters for data model"
        super(UnregisteredAdapterError, self).__init__(_message)

#:
#: The following excepetions are used by REST handlers to indicate 
#: commonly defined scenarios when dealing with data. BaseHandler traps 
#: these and generates an appropriate error message for the end user.
#:

class ServiceUnavailable(HandlerException):
    
    def __init__(self, message="This service is currently unavailable"):
        _code = prestans.http.STATUS.SERVICE_UNAVAILABLE
        super(ServiceUnavailable, self).__init__(_code, message)

class BadRequest(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.BAD_REQUEST
        super(BadRequest, self).__init__(_code, message)

class Conflict(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.CONFLICT
        super(Conflict, self).__init__(_code, message)

class NotFound(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.NOT_FOUND
        super(NotFound, self).__init__(_code, message)

class Unauthorized(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.UNAUTHORIZED
        super(Unauthorized, self).__init__(_code, message)

class MovedPermanently(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.MOVED_PERMANENTLY
        super(MovedPermanently, self).__init__(_code, message)

class PaymentRequired(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.PAYMENT_REQUIRED
        super(PaymentRequired, self).__init__(_code, message)

class Forbidden(HandlerException):

    def __init__(self, message):
        _code = prestans.http.STATUS.FORBIDDEN
        super(Forbidden, self).__init__(_code, message)
