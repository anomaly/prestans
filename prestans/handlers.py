#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2012, Eternity Technologies Pty Ltd.
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

__all__ = ['RESTRequestHandler', 'NotImplementedException']

import prestans.rest

## @package prestans.handlers Handlers are called once a request has been parsed and verified

## @brief Exception thrown when a function has not been overidden 
#
# @ingroup exception
#
class NotImplementedException(Exception):
    pass

## @brief 
#
class StatusCodeOverride(object):

    GET     = None
    POST    = None
    PUT     = None
    DELETE  = None
    
    ## @brief returns the request method of the current handler
    #
    def get_method(self, request_method):
        return self.__class__.__dict__.get(request_method)
            
            
## @brief
#
class StatusCodeOverrideMethod(object):

    ## @brief Constructor
    #
    # @param self The object pointer
    # @param status_code Status code to return for this method
    #
    def __init__(self, status_code=None):
        self._status_code = status_code
        
    def get_status_code(self):
        return self._status_code


## @brief Base request handler
#
# It implements core functions used by the framework on all handlers.
# This class should never be instantiated directly, it should always be overridden.
#   
# Subclassing this you can trust that self.request is parsed and well defined.
# It's exactly how you expect your input, otherwise the framework would have raised an
# Exception and prompted the client with an appropriate message.
#   
# self.response is passed in by the framework, this is what you use to write out
# your response. Once you are done with it, simply return and the framework will
# run the appropriate serializer on it.
#
# If you do not implement a method, by default the framework throws an expception.
#
class RESTRequestHandler:
    """ This Request Handler does not provide a human readable definition """

    request_parser = None
    auth_context = None
    cache_provider = None
    throttle_provider = None
    debug_handler = None
    
    ## @brief Constructor
    #
    # @param self The object pointer
    # @param request
    # @param response
    # @param debug
    #
    def __init__(self, request=None, response=None, debug=False):
        
        self.request = request
        self.response = response
        self.debug = debug

    ## @brief returns a dictionary of discoverable elements
    def discover(self):
        
        blueprint = dict()

        # Request Parser

        # Auth Context

        return blueprint


    ## @brief Called before the the associated request function is called
    # 
    # Implementing this method in your handler is completely optional, this is 
    # generally used to prep persistent storage environments etc
    #
    def handler_will_run(self):
        pass

    ## @brief Called after the associated request has finished executing
    # 
    # Implementing this method in your handler is completely optional, this is 
    # generally used to clean up persistent storage environments etc
    #
    def handler_did_run(self):
        pass
        
    ##  @brief GET method handler
    #
    # @param self The object pointer
    # @param args
    #
    def get(self, *args):
        raise NotImplementedException(self.__class__.__name__ + ' does not implement the GET method')
    
    ## @brief POST method handler
    #
    # @param self The object pointer
    # @param args
    #
    def post(self, *args):
        raise NotImplementedException(self.__class__.__name__ + ' does not implement the POST method')
    
    ## @brief PUT method handler
    #
    # @param self The object pointer
    # @param args
    #
    def put(self, *args):
        raise NotImplementedException(self.__class__.__name__ + ' does not implement the PUT method')

    ## @brief PATCH method handler
    #
    # @param self The object pointer
    # @param args
    #
    def patch(self, *args):
        raise NotImplementedException(self.__class__.__name__ + ' does not implement the PATCH method')
    
    ## @brief DELETE method handler
    #
    # @param self The object pointer
    # @param args
    #
    def delete(self, *args):
        raise NotImplementedException(self.__class__.__name__ + ' does not implement the DELETE method')
        
    ## @brief Called by Cache handler to obtain a Key for the Cache
    #
    # @param self a reference to the object itself
    # @param request_method Current request method, keys can differ based on the method
    #
    #
    def get_cache_key(self, request_method):
        return None


## @brief
#
class DiscoveryHandler(RESTRequestHandler):

    ## @brief 
    #
    # @param self the object pointer
    #
    def get(self):
        
        self.response.status_code = prestans.rest.STATUS.OK
