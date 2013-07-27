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
    'ConfigurationException',
    'DataValidationException',
    'ParserException',
    'HandlerException',

    #: Configuration Exceptions
    'DirectUseNotAllowed',
    'ReservedWord',
    'UnimplementedVerb',
    'NotParserRuleSet',
    'NotParameterSet',
    'InvalidParameterSetAttribute',
    'InvalidDataType',
    'RequiresDataCollection',
    'RequiresModel',

    #: Parser Exceptions
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
        <html>
            <head>
                <title>prestans %s, unsupported media type</title>
            </head>
            <body>
                <h1>Unsupported media type</h1>
                <p>
                    You requested <span>%s</span> and we can support <span>%s</span>
                </p>
            </body>
        </html>
        """ % (prestans.__version__, user_accept_header, str(supported_mime_types).strip("[]'"))

        return error_response(environ, start_response)

class ConfigurationException(Exception):
    """
    ConfigurationExceptions are Exceptions raised if prestans was
    incorrectly configured. These exceptions are completely masked 
    for the requesting client and written out to error log.

    In production these Exceptions should never be raised. This 
    exception generally alludes that your API has a bug; prestans 
    will cease execution of your handler code.
    """
    
    def __init__(self):
        pass

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



    """
    pass

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
#: Configuration
#:

class DirectUseNotAllowedError(ConfigurationException):
    
    def __init__(self, method_name, class_name):
        self._class_name = class_name
        self._method_name = method_name


class ReservedWord(ConfigurationException):
    
    def __init__(self, word):
        self._word = word

class UnimplementedVerb(ConfigurationException):

    def __init__(self, verb_name):
        self._http_status = prestans.http.STATUS.METHOD_NOT_ALLOWED
        self._message = "end point does not speak %s" % (verb_name)

class NotParserRuleSet(ConfigurationException):
    pass

class NotParameterSet(ConfigurationException):
    pass

class InvalidParameterSetAttribute(ConfigurationException):
    pass

class InvalidDataType(ConfigurationException):
    
    def __init__(self, attribute_name, expected_type):
        pass

class RequiresDataCollection(ConfigurationException):
    pass

class RequiresModel(ConfigurationException):
    pass


#:
#: Parser Exception
#:

class NoSetMatched(ParserException):
    pass

class BodyTemplateParse(ParserException):
    pass

class EmptyBody(ParserException):
    pass


#:
#: Data Validation
#: 

class RequiredAttribute(DataValidationException):
    pass

class ParseFailed(DataValidationException):
    
    def __init__(self, value, data_type):
        pass

class InvalidValue(DataValidationException):
    
    def __init__(self, value):
        pass

class LessThanMinimum(DataValidationException):
    
    def __init__(self, value, allowed_min):
        pass

class MoreThanMaximum(DataValidationException):

    def __init__(self, value, allowed_max):
        pass

class InvalidChoice(DataValidationException):

    def __init__(self, value, allowed_choices):
        pass

class UnacceptableLength(DataValidationException):
    
    def __init__(self, value, minimum, maximum):
        pass

class InvalidType(DataValidationException):
    
    def __init__(self, value, type_name):
        pass

class InvalidCollection(DataValidationException):

    def __init__(self, value):
        pass

class MissingParameter(DataValidationException):
    pass

class InvalidFormat(DataValidationException):
    
    def __init__(self, value):
        pass

class InvalidMetaValue(DataValidationException):
    pass

class UnregisteredAdapter(DataValidationException):
    pass

class NotImplemented(DataValidationException):
    pass

class SerializationFailed(DataValidationException):
    pass


#:
#: The following excepetions are used by REST handlers to indicate 
#: commonly defined scenarios when dealing with data. BaseHandler traps 
#: these and generates an appropriate error message for the end user.
#:

class ServiceUnavailable(HandlerException):
    pass

class BadRequest(HandlerException):
    pass

class Conflict(HandlerException):
    pass

class NotFound(HandlerException):
    pass

class Unauthorized(HandlerException):
    pass

class MovedPermanently(HandlerException):
    pass

class PaymentRequired(HandlerException):
    pass

class Forbidden(HandlerException):
    pass