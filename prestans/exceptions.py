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

#:
#: The following Exceptions are used internally by the prestans framework to indicate
#: parsing, and implemtnation errors.
#:
#: Some of them do not produce an error mesasge for the client, instead they write to
#: the log and terminate the REST application. Those exceptions that terminate the
#: application should never be shipped.
#:

class Base(Exception):

    def __init__(self, message, Errors):

        Exception.__init__(self, message)
        self.Errors = Errors

#:
#: Configuration
#:

class Configuration(Base):
    pass

class DataValidation(Base):
    pass


#:
#: Configuration
#:

class DirectUseNotAllowed(Configuration):
    pass

class ReservedWord(Configuration):
    pass

class NotParserRuleSet(Configuration):
    pass

class NotParameterSet(Configuration):
    pass

class InvalidParameterSetAttribute(Configuration):
    pass

class InvalidDataType(Configuration):
    pass    

class RequiresDataCollection(Configuration):
    pass

class RequiresModel(Configuration):
    pass


#:
#: Data Validation
#: 

class RequiredAttribute(DataValidation):
    pass

class ParseFailed(DataValidation):
    
    def __init__(self, value, data_type):
        pass

class InvalidValue(DataValidation):
    
    def __init__(self, value):
        pass

class LessThanMinimum(DataValidation):
    
    def __init__(self, value, allowed_min):
        pass

class MoreThanMaximum(DataValidation):

    def __init__(self, value, allowed_max):
        pass

class InvalidChoice(DataValidation):

    def __init__(self, value, allowed_choices):
        pass

class UnacceptableLength(DataValidation):
    
    def __init__(self, value, minimum, maximum):
        pass

class InvalidType(DataValidation):
    
    def __init__(self, value, type_name):
        pass

class InvalidCollection(DataValidation):
    pass

class MissingParameter(DataValidation):
    pass

class InvalidFormat(DataValidation):
    pass

class InvalidMetaValue(DataValidation):
    pass

class UnregisteredAdapter(DataValidation):
    pass

class NotImplemented(DataValidation):
    pass

class SerializationFailed(DataValidation):
    pass

#:
#: Parser Exception
#:

class NoSetMatched(Exception):
    pass

class BodyTemplateParse(Exception):
    pass

class EmptyBody(Exception):
    pass


#:
#: The following excepetions are used by REST handlers to indicate commonly defined
#: scenarios when dealing with data. BaseHandler traps these and generates an appropriate
#: error message for the end user.
#:

class RESTOperation(Exception):
    """
    Extends from the Base exception to make available a HTTP status code, these
    are thrown if an unacceptable REST operation is performed. 

    E.g a client attempts to access data they are not allowed to.
    """
    pass

class ServiceUnavailable(RESTOperation):
    pass

class BadRequest(RESTOperation):
    pass

class Conflict(RESTOperation):
    pass

class NotFound(RESTOperation):
    pass

class Unauthorized(RESTOperation):
    pass

class Forbidden(RESTOperation):
    pass