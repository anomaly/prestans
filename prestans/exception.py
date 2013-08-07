# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
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
#      * Neither the name of Eternity Technologies nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ETERNITY TECHNOLOGIES BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__all__ = [
    'UnsupportedVocabularyError',
    'DataValidationException',
    'ParserException',
    'HandlerException',

    #: Parser Exceptions
    'NoEndpointError',
    'SerializationFailed',
    'NoSetMatched',
    'BodyTemplateParse',
    'EmptyBody',

    #: Data Validation
    'RequiredAttribute',
    'ParseFailed',
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
    'Forbidden'
]

import prestans
import prestans.http

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

class UnsupportedVocabularyError(Exception):
    """
    Called if none of the requested vocabularies are supported by the API
    this error message is sent as an HTML document. This exception is the
    only one that breaks serialisation rules.
    """

    def __init__(self, mime_type):
        self._mime_type = mime_type
    
class UnsupportedContentTypeError(Exception):
    
    def __init__(self, mime_type):
        self._mime_type = mime_type

class DataValidationException(Exception):
    """
    DataValidationException are Exceptions raised if prestans fails
    to validate data inbound or out using rules defined in Models.

    These contains a stack trace to indicate the depth of the error.
    E.g Model has Sub Model that has attribute which failed to validate.

    Each exception uses an HTTP status code and is sent to the client.
    """
    pass

class ParserException(Exception):
    """
    ParserException are Exceptions raised if prestans fails to parse
    a request; these generally revolve around the Content-Types or 
    missing payload. Specific parsing messages are of type DataValidationException
    """
    
    @property
    def http_status(self):
        return self._http_status

    @http_status.setter
    def http_staths(self, value):
        self._http_status = value

    def __str__(self):
        return self._message

class HandlerException(Exception):
    """
    HandlerExceptions are Exceptions that are raised by handlers of the
    REST application. REST encourages the use different error codes to
    denote what the error is.

    E.g Use 404 to denote that a reqeusted doesn't exists on the server.

    If one of these exceptions do not match your user case; you are free
    construct your own error message and use an error code from outlined
    in prestans.http

    """
    pass


#:
#: Parser Exception
#:

class UnimplementedVerbError(ParserException):

    def __init__(self, verb_name):
        self._http_status = prestans.http.STATUS.NOT_ALLOWED
        self._message = "End-point doesn't implement %s" % verb_name

class NoEndpointError(ParserException):

    def __init__(self):
        self._http_status = prestans.http.STATUS.NOT_FOUND
        self._message = "API does not provide this end-point"

class NoSetMatched(ParserException):
    pass

class BodyTemplateParseError(ParserException):
    pass

class EmptyBody(ParserException):
    pass


#:
#: Data Validation
#: 

class RequiredAttributeError(DataValidationException):
    pass

class ParseFailed(DataValidationException):
    
    def __init__(self, value, data_type):
        pass

class InvalidValueError(DataValidationException):
    
    def __init__(self, value):
        pass

class LessThanMinimumError(DataValidationException):
    
    def __init__(self, value, allowed_min):
        pass

class MoreThanMaximumError(DataValidationException):

    def __init__(self, value, allowed_max):
        pass

class InvalidChoiceError(DataValidationException):

    def __init__(self, value, allowed_choices):
        pass

class UnacceptableLengthError(DataValidationException):
    
    def __init__(self, value, minimum, maximum):
        pass

class InvalidType(DataValidationException):
    
    def __init__(self, value, type_name):
        pass

class InvalidCollectionError(DataValidationException):

    def __init__(self, value):
        pass

class MissingParameterError(DataValidationException):
    pass

class InvalidFormatError(DataValidationException):
    
    def __init__(self, value):
        pass

class InvalidMetaValueError(DataValidationException):
    pass

class UnregisteredAdapterError(DataValidationException):
    pass

class SerializationFailedError(DataValidationException):
    pass

class DeSerializationFailedError(DataValidationException):
    pass


#:
#: The following excepetions are used by REST handlers to indicate 
#: commonly defined scenarios when dealing with data. BaseHandler traps 
#: these and generates an appropriate error message for the end user.
#:

class ServiceUnavailable(HandlerException):
    
    def __init__(self, service_name):
        self._http_status = prestans.http.STATUS.SERVICE_UNAVAILABLE
        self._service_name = service_name

class BadRequest(HandlerException):

    def __init__(self):
        self._http_status = prestans.http.STATUS.BAD_REQUEST

class Conflict(HandlerException):

    def __init__(self):
        self._http_status = prestans.http.STATUS.CONFLICT

class NotFound(HandlerException):

    def __init__(self):
        self._http_status = prestans.http.STATUS.NOT_FOUND

class Unauthorized(HandlerException):

    def __init__(self):
        self._http_status = prestans.http.STATUS.UNAUTHORIZED

class MovedPermanently(HandlerException):

    def __init__(self):
        self._http_status = prestans.http.STATUS.MOVED_PERMANENTLY

class PaymentRequired(HandlerException):
    pass

class Forbidden(HandlerException):
    pass