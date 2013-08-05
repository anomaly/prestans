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
    'UnimplementedVerb',
    'NotImplemented',
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
    
    def as_error_response(self, environ, start_response, user_accept_header, supported_mime_types):

        import webob
        error_response = webob.Response()

        error_response.status = prestans.http.STATUS.UNSUPPORTED_MEDIA_TYPE
        error_response.content_type = "text/html"
        error_response.body = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <title>prestans %s, unsupported media type</title>
                 <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.0-rc1/css/bootstrap.min.css">
            </head>
            <body>
                <div class="alert alert-danger alert-block">
                    <h4>Unsupported media type</h4>
                    <p>
                    The request contained an <code>Accept</code> header of
                    <code>%s</code>
                    the end-point registered at this URL can speak
                    <code>%s</code>
                    </p>
                    
                    <p class="help-block">
                    <a target="_blank" href="https://github.com/prestans/prestans">prestans</a> 
                    %s, Copyright &copy 2013 <a href="http://etk.com.au">Eternity Technologies</a></p>
                </div>
            </body>
        </html>
        """ % (prestans.__version__, user_accept_header, 
            str(supported_mime_types).strip("[]'"), prestans.__version__)

        return error_response(environ, start_response)

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

class UnimplementedVerb(ParserException):

    def __init__(self, verb_name):
        self._http_status = prestans.http.STATUS.METHOD_NOT_ALLOWED
        self._message = "API end-point does not implement the %s verb" % (verb_name)

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

class NotImplementedError(DataValidationException):
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