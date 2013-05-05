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
    'ParameterSet', 
    'ParserRuleSet', 
    'RequestParser', 
    'NotParserRuleSetObjectException', 
    'NotParameterSetObjectException']

import inspect
import string

import .exceptions

#:
#:
#:

class ParameterSet(object):
    pass


#:
#:
#:

class AttributeFilter(object):
    pass

#:
#:
#:

class ParserRuleSet(object):
    pass

#:
#:
#:

class RequestParser(object):
    
    GET     = None
    POST    = None
    PUT     = None
    PATCH   = None
    DELETE  = None

    def parse(self, request, response, environ):
        """
        If the implementing request parser does not specify a parser for a method, None is returned, 
        this completely bypasses the parsing process.
        
        The implementing request parser must assign an instance of %ParserRuleSet for each HTTP method.
        
        RequestParser will attempt use those rules to parse the input and assign them to the passed in
        request object. It returns True or False.

        self The object pointer
        response object
        request The request to parse

        """
        
        request_method = request.get_request_method()

        if not self.__class__.__dict__.has_key(request_method) or self.__class__.__dict__[request_method] is None:
            """ 
            Default rule set is None, ignores parsing for Pameters and Body 
            """
            return
        
        if not isinstance(self.__class__.__dict__[request_method], ParserRuleSet):
            """ 
            Handles the developer not assinging an object of type ParserRuleSet 
            """
            raise NotParserRuleSetObjectException(request_method + " does not have a valid ParserRuleSet")
        
        parser_rule_set = self.__class__.__dict__[request_method]

        #: Parse parameters or None if nothing matched
        request.parameter_set = parser_rule_set._parameter_set_for_request(request)
        
        #: Parse request body
        request.parsed_body_model = parser_rule_set._parsed_body_for_request(request, environ)

        #: Parse the field filter list
        response.attribute_filter = parser_rule_set._parse_attribute_filter(request)