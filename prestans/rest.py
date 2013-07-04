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

import webob
import re

import prestans.exceptions

#:
#: Wrappers around Request and Response to handle HTTP requests, these depend on
#: serializers to write read and write responses
#:

class Request(webob.Request):

    def __init__(self, environ, charset="utf-8"):

        webob.Request.__init__(self, environ=environ, charset=charset)


class Response(webob.Response):

    def __init__(self):
        pass


#:
#: RESTHandler defines specific end points, developers subclass this to
#: implement their end points.
#:
#: Also contains Blueprint handler
#:

class RequestHandler(object):

    def __init__(self, request=None, response=None, inflators, deflators, debug=False):

        self._request = request
        self._response = response
        self._debug = debug
        self._serializers = serializers
        self._inflators = inflators
        self._deflators = deflators

    def __call__(self, environ, start_response):

        return self._response(environ, start_response)


    def handler_will_run(self):
        #:
        #:
        #:
        return None

    def handler_did_run(self):
        #:
        #:
        #:
        return None

    def get(self, *args):
        raise prestans.exceptions.UnimplementedVerb("GET")

    def post(self, *args):
        raise prestans.exceptions.UnimplementedVerb("POST")

    def put(self, *args):
        raise prestans.exceptions.UnimplementedVerb("PUT")

    def patch(self, *args):
        raise prestans.exceptions.UnimplementedVerb("PATCH")

    def delete(self, *args):
        raise prestans.exceptions.UnimplementedVerb("DELETE")


#:
#:
#:

class BlueprintHandler(RequestHandler):
    pass


#:
#: Router infrastructure code to dispatch requests
#:

class RequestRouter(object):

    def __init__(self, routes, inflators, deflators, charset="utf-8", application_name="prestans", debug=False):

        self._application_name = application_name
        self._debug = debug
        self._charset = charset

        #:
        #: line 63, http://code.google.com/p/webapp-improved/source/browse/webapp2.py
        #:
        self._route_re = re.compile(r"""
                \<               # The exact character "<"
                ([a-zA-Z_]\w*)?  # The optional variable name
                (?:\:([^\>]*))?  # The optional :regex part
                \>               # The exact character ">"
                """, re.VERBOSE)

    @property
    def debug(self):
        return self._debug

    def add_route(self, route, handler_class):
        pass

    def __call__(self, environ, start_response):
        
        #: Check if the requested URL has a valid registered handler

        #: Run a request parser        

        return
