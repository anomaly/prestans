#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
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

__all__ = ['STATUS', 'METHOD', 'Request', 'Response', 'Logger', 'RESTApplication', 'JSONRESTApplication']

## @package prestans.rest Provides the REST application model
#

import cgi
import logging
import os
import re
import sys
import traceback
import urlparse

import webob

import wsgiref.handlers
import wsgiref.headers
import wsgiref.util

import prestans.types
import prestans.parsers
import prestans.handlers
import prestans.serializers
import prestans.throttle

# Regular expression constants
_RE_FIND_GROUPS = re.compile('\(.*?\)')
_RE_CHARSET     = re.compile(r';\s*charset=([^;\s]*)', re.I)

## @brief Meta class provides status codes and messages for REST services
#
# @ingroup constants
#
class STATUS:
    OK                      = { "CODE": 200, "MESSAGE": "OK" }
    CREATED                 = { "CODE": 201, "MESSAGE": "Created" }
    ACCEPTED                = { "CODE": 202, "MESSAGE": "Accepted" }
    NO_CONTENT              = { "CODE": 204, "MESSAGE": "No Content" }
    NOT_MODIFIED            = { "CODE": 304, "MESSAGE": "Not Modified" }
    BAD_REQUEST             = { "CODE": 400, "MESSAGE": "Bad Request" }
    UNAUTHORIZED            = { "CODE": 401, "MESSAGE": "Unauthorized" }
    FORBIDDEN               = { "CODE": 403, "MESSAGE": "Forbidden" }
    NOT_FOUND               = { "CODE": 404, "MESSAGE": "Not Found" }
    CONFLICT                = { "CODE": 409, "MESSAGE": "Conflict" }
    GONE                    = { "CODE": 410, "MESSAGE": "Gone" }
    INTERNAL_SERVER_ERROR   = { "CODE": 500, "MESSAGE": "Internal Server Error" }
    SERVICE_UNAVAILABLE     = { "CODE": 503, "MESSAGE": "Service Unavailable" }

    @classmethod
    def as_header_string(cls, http_status):
        return "%i %s" % (http_status['CODE'], http_status['MESSAGE'])


## @brief Meta class for HTTP methods
#
# @ingroup constants
#   
class METHOD:
    
    GET     = "GET"
    POST    = "POST"
    PUT     = "PUT"
    PATCH   = "PATCH"
    DELETE  = "DELETE"


## @brief Base exception for REST errors
#
#  @ingroup exception
#
class RESTException(Exception):

    def __str__(self):
        return self._message

## @brief Server capability disabled preventing REST handlers from finishing tasks
#
#  @ingroup exception
#
#  Raised when a resource like the database is unavailable on the server and a REST service
#  in unable to finish it's task as expected.
#
class ServiceUnavailableException(RESTException):
    
    def __init__(self, message=None):
        self.STATUS = STATUS.SERVICE_UNAVAILABLE
        if message is None:
            self._message = "Service Unavailable"
        else:
            self._message = "Service Unavailable: %s" % message

## @brief Can be raised by a REST Handler for generic resource integrity issues
#
#  @ingroup exception
#
#  These exceptions are handled by RESTApplication providing the client with
#  a unifrom set of messages for permission issues for Expcetions.
#
#  Caller is expceted to provide an error message
#  
class BadRequestException(RESTException):
    
    def __init__(self, message=None):
        self.STATUS = STATUS.BAD_REQUEST
        if message is None:
            self._message = "Bad Request"
        else:
            self._message = "Bad Request: %s" % (message) 

## @brief Can be raised by a REST Handler for generic resource integrity issues
#
#  @ingroup exception
#
#  These exceptions are handled by RESTApplication providing the client with
#  a unifrom set of messages for permission issues for Exceptions.
#
#  Caller is excepted to provide an error message
#  
class ConflictException(RESTException):
    
    def __init__(self, message=None):
        self.STATUS = STATUS.CONFLICT
        if message is None:
            self._message = "Conflict"
        else:
            self._message = "Conflict: %s" % (message) 
      
## @brief Can be raised by a REST Handler if the resource does not exist
#
#  @ingroup exception
#
#  These exceptions are handled by RESTApplication providing the client with
#  a unifrom set of messages for all missing entities.
#  
class NotFoundException(RESTException):

    def __init__(self, message=None):
        self.STATUS = STATUS.NOT_FOUND
        
        if message is None:
            self._message = "Not Found"
        else:
            self._message = "Not Found: %s" % (message)
            

## @brief Can be raised by a REST Handler if a resource exists but should not be accessed by the current user
#
#  @ingroup exception
#
#  These exceptions are handled by RESTApplication providing the client with
#  a unifrom set of messages for permission issues for Expcetions.
#  
class UnauthorizedException(RESTException):

    def __init__(self, message=None):
        self.STATUS = STATUS.UNAUTHORIZED
        if message is None:
            self._message = "Unauthorized"
        else:
            self._message = "Unauthorized: %s" % (message)

## @brief Can be raised by a REST Handler for a forbidden resource or action
#
#  @ingroup exception
#
#  These exceptions are handled by RESTApplication providing the client with
#  a unifrom set of messages for permission issues for Expcetions.
#  
class ForbiddenException(RESTException):

    def __init__(self, message=None):
        self.STATUS = STATUS.FORBIDDEN
        if message is None:
            self._message = "Forbidden"
        else:
            self._message = "Forbidden: %s" % (message)

## @brief Represents a REST request, includes headers, parsed parameters, parsed Body.
#
# An instance of Request is available in the RequestHandler instance.
#
class Request(webob.Request):
    
    parameter_set = None
    parsed_body_model = None
    
    ## @brief Constructor
    # 
    #  @param self The object pointer
    #  @param environ
    #  @param serializer
    #
    def __init__(self, environ, serializer):
        
        match = _RE_CHARSET.search(environ.get('CONTENT_TYPE', ''))
        if match:
            charset = match.group(1).lower()
        else:
            charset = 'utf-8'

        webob.Request.__init__(self, environ)

        self._serializer = serializer
        self._response_field_list = None
        self._parameter_set = None
        self._parsed_body_model = None    
    
    ## @brief Return the HTTP request method for the current request
    #
    #  This is required by WebOb, this should not be turned into a property 
    #
    def get_request_method(self):
        return self.environ['REQUEST_METHOD']

    ## @brief return a unserialized _response_attribute_list or none
    #
    def get_unserialized_attribute_filter_list(self):

        if self.get("_response_attribute_list"):
            attribute_list_configuration = self.get("_response_attribute_list")
            return self._serializer.loads(attribute_list_configuration)

        return None

    
    ## @brief Return the unserialized body
    #
    # @param self The object pointer
    #
    def get_unserialized_body(self):
        """ Can't see request.body """
        return self._serializer.loads(self.body)

    ## @brief Fetch url parameter for given name
    #
    #  @param self The object pointer
    #  @param argument_name
    #  @param default_value
    #
    def get(self, argument_name, default_value=None):
        
        param_value = self.get_all(argument_name)
        if len(param_value) > 0:
            return param_value[0]
        
        return default_value

    ## @brief Fetch all url parameters for given name
    #
    # Based on Google Appengine's code base
    #
    # @param self The object pointer
    # @param argument_name
    # @param default_value
    #
    def get_all(self, argument_name, default_value=None):
        
        if self.charset:
            argument_name = argument_name.encode(self.charset)
        
        if default_value is None:
            default_value = []

        param_value = self.params.getall(argument_name)

        if param_value is None or len(param_value) == 0:
            return default_value

        for index in xrange(len(param_value)):
            if isinstance(param_value[index], cgi.FieldStorage):
                param_value[index] = param_value[index].value
                
        return param_value
    
    
    ## @brief has_parameter_key
    #
    # @param self The object pointer
    # @param parameter_key
    #   
    def has_parameter_key(self, parameter_key):
        return self.params.has_key(parameter_key)
        
    """ Properties """

    def _get_response_field_list(self):
        return self._response_field_list

    def _set_response_field_list(self, value):
        self._response_field_list = value

    def _del_response_field_list(self):
        del self._response_field_list

    response_field_list = property(_get_response_field_list,
                                   _set_response_field_list,
                                   _del_response_field_list,
                                   "Response field list")

    def _get_arguments(self):
        return list(set(self.params.keys()))
        
    arguments = property(_get_arguments)
        
    def _get_parameter_set(self):
        return self._parameter_set
    
    def _set_parameter_set(self, value):
        self._parameter_set = value
        
    def _del_parameter_set(self):
        del self._parameter_set
        
    parameter_set = property(_get_parameter_set, 
                             _set_parameter_set, 
                             _del_parameter_set, 
                             "Matched Parameter Set")
    
    def _get_parsed_body_model(self):
        return self._parsed_body_model
        
    def _set_parsed_body_model(self, value):
        self._parsed_body_model = value
        
    def _del_parsed_body_model(self):
        del self._parsed_body_model
        
    parsed_body_model = property(_get_parsed_body_model, 
                                 _set_parsed_body_model, 
                                 _del_parsed_body_model, 
                                 "Parsed Body Model")


## @brief Represents a REST response
#
class Response(object):

    ## @brief Constructor
    #
    # @param self The object pointer
    # @param serializer
    #
    def __init__(self, serializer):

        self.headers = wsgiref.headers.Headers([])

        self._status_code = STATUS.NOT_FOUND
        self._body = {}     
        self._serializer = serializer
        self._request = None
        self._attribute_filter = None
        
        """ Initialize fixed headers for JSON response """
        self.headers.add_header('Content-Type', self._serializer.get_content_type())
        self.headers.add_header('Cache-Control', 'no-cache')
        
    ## @brief Headers using WSGI headers
    #
    def get_headers(self):
        return self.headers.items()

    ## @brief Adds or updates a body attribute
    #
    # Body attributes must be serialized as a dictionary to assist serializers create the
    # HTTP body. If the provide value is a prestans type then the framework will take care
    # of reducing it down to a python type.
    #
    # Python values are stored as is in the dictionary.
    #
    def set_body_attribute(self, name, value):
        self._body[name] = value

    ## @brief Returns a serialized string that can be sent back to the client
    #
    def serialized_body(self):
        
        serializable_body = None
        if issubclass(self._body.__class__, prestans.types.DataCollection):
            serializable_body = self._body.as_serializable(attribute_filter=self.attribute_filter)
        else:
            serializable_body = dict()
            for key, value in self._body.iteritems():
                if issubclass(value.__class__, prestans.types.DataCollection):
                    serializable_body[key] = value.as_serializable(attribute_filter=self.attribute_filter)
                else:
                    serializable_body[key] = value
        
        return self._serializer.dumps(serializable_body)
    
    ## @brief returns True if the body has one or more element(s)
    #   
    def has_body(self):
        return issubclass(self._body.__class__, prestans.types.DataCollection) or len(self._body) > 0
        
    ## @brief Creates a default body wiht an error code a message string
    #
    def make_default_response(self, code=None, message=None):
        
        if not code:
            code = self._status_code['CODE']
            
        if not message:
            message = self._status_code['MESSAGE']
        self._body = {}
        self.set_body_attribute('code', code)
        self.set_body_attribute('message', message)
        
    ## @brief Keeps a handle to the current request object
    #
    def set_request(self, request):
        self._request = request

    """ Properties """

    def _get_http_status(self):
        return self._status_code

    def _set_http_status(self, value):
        self._status_code = value
        
    http_status = property(_get_http_status, _set_http_status)
    
    def _get_body(self):
        return self._body
        
    def _set_body(self, body_dictionary):
        self._body = body_dictionary
        
    body = property(_get_body, 
                    _set_body)

    def _get_attribute_filter(self):
        return self._attribute_filter

    def _set_attribute_filter(self, value):
        self._attribute_filter = value

    attribute_filter = property(_get_attribute_filter, _set_attribute_filter)

## @brief Provides the base implementation for a RESTApplication, this is never instantiated, look at JSONRESTApplication
#
# prestans is a WSGI compliant framework. It was originally tested under the Google
# AppEngine platform, but will work under any WSGI compliant platform. 
#
# RESTApplications expects to get a list of URLs and handles to prestans.handlers.RESTHandler
# sub-classes that responds to this request.
#
class RESTApplication(object):
    
    ## @brief Parses the request using the serializer
    #
    @classmethod
    def make_request(self, environ):
        raise Exception("RESTApplication class used directly, use serializer specific implementation")

    ## @brief Serializes Python objects for delivery over HTTP via the serializer
    #
    @classmethod
    def make_response(self):
        raise Exception("RESTApplication class used directly, use serializer specific implementation")
    
    ## @brief Constructor must be provided a set of URL handlers mapped to RequestHandler subclasses
    #
    def __init__(self, 
                 url_handler_map=[], 
                 application_name="prestans", 
                 debug=False,
                 allow_status_code_override=False):

        self._url_handler_map = url_handler_map
        self._parsed_handler_map = self._init_url_maps(url_handler_map)
        self._application_name = application_name
        self._debug = debug
        self._allow_status_code_override = allow_status_code_override
        self._request = None
        
    ## @brief Wrapper for Pyton logging error level message
    #
    def _log_error(self, message):
        logging.error("[%s] %s %s - %s" % 
                      (self._application_name, self._request.get_request_method(), self._request.path, message))

    ## @brief Wrapper for Python logging warning level message
    #
    def _log_warn(self, message):
        logging.warning("[%s] %s %s - %s" % 
                        (self._application_name, self._request.get_request_method(), self._request.path, message))

    ## @brief Callable middleware WSGI application
    #
    #  This method establishes the lifecycle of the REST application, the lifecycle runs the validator
    #  calls the appropriate HTTP method int he handler and finally handles exceptions to provide an
    #  acceptable serializable response to the client.
    #
    def __call__(self, environ, start_response):

        # Overriden by the implementing class 
        self._request = self.__class__.make_request(environ)

        response = self.__class__.make_response()
        # Pass a refer to the request for use with as_serializable 
        response.set_request(self._request)

        request_method = self._request.get_request_method()
        
        rest_handler = None
        current_request_args = ()

        for regexp, handler_class in self._parsed_handler_map:
            # 1. Determine if we have a handler for the URL, if not spit out an error message 

            match = regexp.match(self._request.path)
            if match:
                rest_handler = handler_class(request=self._request, 
                                             response=response, 
                                             debug=self._debug)
                current_request_args = match.groups()
                
            
        if not rest_handler or not issubclass(rest_handler.__class__, prestans.handlers.RESTRequestHandler):

            # Stop if there isn't a rest handler / 404 Not Found 
            self._log_error('No valid registered REST handler at this URL')
            
            response.http_status = STATUS.NOT_FOUND
            response.make_default_response(message="Invalid valid URL handler registered for this endpoint")
            start_response(STATUS.as_header_string(response.http_status), response.get_headers())
            return [response.serialized_body()]
            
        if not request_method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            
            # For non conformed REST requests, send an Internal server error 
            self._log_error('Not a valid HTTP method for a REST API')

            return self._send_response(
                error_code=STATUS.INTERNAL_SERVER_ERROR, 
                message="Requested method is not a valid REST method", 
                response=response)        
        
        if self._allow_status_code_override and rest_handler.__class__.status_code_override is not None:
            
            # Overrides the status code, used for testing 
            overridden_method = rest_handler.__class__.status_code_override.get_method(request_method)
            
            if overridden_method is not None:

                return self._send_response(
                    error_code=overridden_method.get_status_code(), 
                    message="prestans status override mode is currently enabled", 
                    response=response)

        if rest_handler.__class__.throttle_provider is not None:
            
            # See if the client is throttled 
            is_throttled = rest_handler.throttle_provider.is_throttled()
            if is_throttled:
                return self._send_response(
                    error_code=STATUS.FORBIDDEN, 
                    message="client has been throttled, try again in a while", 
                    response=response)

        
        if rest_handler.__class__.request_parser:
            # 2. Use the Handler's parser to parse the input 
            request_parser = rest_handler.__class__.request_parser
            try:
            
                validation_result = request_parser.parse(self._request, response, environ)
            
            except (prestans.parsers.NotParserRuleSetObjectException, 
                    prestans.parsers.NotParameterSetObjectException, 
                    prestans.parsers.InvalidDataTypeException, 
                    prestans.parsers.RequiresDataCollectionException, 
                    prestans.parsers.BodyTemplateParseException, 
                    prestans.parsers.EmptyBodyException, 
                    prestans.serializers.UnserializationFailedException, 
                    prestans.parsers.ReservedWordException), exp:
            
                self._log_error(str(exp))
                return self._send_response(
                    error_code=STATUS.BAD_REQUEST, 
                    message=str(exp), 
                    response=response)
                                
        try:
            
            # Allows apps to prep an environment that a handler has access to
            rest_handler.handler_will_run()

            # Exception for Blueprint handler
            if rest_handler.__class__ == prestans.handlers.BlueprintHandler:
                # Discovery requires a reference to the handler map
                rest_handler.handler_map = self._url_handler_map
                response.http_status = STATUS.OK
                # Discovery can only respond to GET and accept regrex input
                rest_handler.get()
            else:
                # 3. Execute appropriate method based on the call type
                if request_method == METHOD.GET:
                    response.http_status = STATUS.OK
                    rest_handler.get(*current_request_args)
                elif request_method == METHOD.POST:
                    response.http_status = STATUS.CREATED
                    rest_handler.post(*current_request_args)
                elif request_method == METHOD.PATCH:
                    self.http_status = STATUS.ACCEPTED
                    rest_handler.patch(*current_request_args)
                elif request_method == METHOD.DELETE:
                    self.http_status = STATUS.NO_CONTENT
                    rest_handler.delete(*current_request_args)
                elif request_method == METHOD.PUT:
                    self.http_status = STATUS.ACCEPTED
                    rest_handler.put(*current_request_args)
                
            # Allows users to clean up after the handler has run
            rest_handler.handler_did_run()

        except (BadRequestException, 
                NotFoundException, 
                UnauthorizedException,
                ForbiddenException, 
                ServiceUnavailableException,
                ConflictException), exp:

            # Converts resource level exceptions into messages for the client
            self._log_error(str(exp))

            return self._send_response(
                error_code=exp.STATUS, 
                message=str(exp), 
                response=response)

        except prestans.handlers.NotImplementedException, exp:

            # Gracefully fails if a handler does not implement a HTTP method
            self._log_error(str(exp))

            return self._send_response(
                error_code=STATUS.FORBIDDEN, 
                message=str(exp), 
                response=response)

        # Output a warning about an empty response unless the user meant it
        if not response.has_body() and response.http_status['CODE'] != STATUS.NO_CONTENT['CODE']:
            self._log_warn("empty response from REST handler")
            
            response.http_status = STATUS.OK
            response.make_default_response(message='REST Handler returned no content')
            
        start_response(STATUS.as_header_string(response.http_status), response.get_headers())
        return [response.serialized_body()]


    ## @brief Wrapper to create response for error codes
    #
    def _send_response(self, error_code, message, response):
        response.http_status = error_code
        response.make_default_response(message=message)
        start_response(STATUS.as_header_string(response.http_status), response.get_headers())
        return [response.serialized_body()]


    ## @brief Processes the regular expressions passed in to the Application and reconstructs the handler map.
    #
    #  @private
    #
    def _init_url_maps(self, url_handler_map):
        parsed_handler_map = []
        handler_name = None
        
        for regexp, handler in url_handler_map:

            try:
                handler_name = handler.__name__
            except AttributeError:
                pass

            """ Patch regular expression if its incomplete """
            if not regexp.startswith('^'):
                regexp = '^' + regexp
            if not regexp.endswith('$'):
                regexp += '$'
                
            compiled_regex = re.compile(regexp)
            parsed_handler_map.append((compiled_regex, handler))
            
        return parsed_handler_map

    
## @brief REST Application Gateway that speaks JSON
#
class JSONRESTApplication(RESTApplication):

    @classmethod
    def make_request(self, environ):
        rest_request = Request(environ, 
                               serializer=prestans.serializers.JSONSerializer)
        return rest_request

    @classmethod
    def make_response(self):
        rest_response = Response(serializer=prestans.serializers.JSONSerializer)
        return rest_response

## @brief REST Application Gateway that speaks YAML
#
class YAMLRESTApplication(RESTApplication):

    @classmethod
    def make_request(self, environ):
        rest_request = Request(environ, 
                               serializer=prestans.serializers.YAMLSerializer)
        return rest_request

    @classmethod
    def make_response(self):
        rest_response = Response(serializer=prestans.serializers.YAMLSerializer)
        return rest_response

