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
import logging

import prestans.exceptions
import prestans.serializers
import prestans.deserializers

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

    def __init__(self, request, response, serializers, deserializers, logger, debug=False):

        self._request = request
        self._response = response
        self._debug = debug
        self._logger = logger
        self._serializers = serializers
        self._deserializers = deserializers

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response

    def __call__(self, environ, start_response):

        return self._response(environ, start_response)


    def handler_will_run(self):
        return None

    def handler_did_run(self):
        return None

    #:
    #: Placeholder functions
    #:
    #:

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

    def __init__(self, routes, serializers=None, deserializers=None, charset="utf-8", application_name="prestans", logger=None, debug=False):

        self._application_name = application_name
        self._debug = debug
        self._routes = routes
        self._charset = charset

        #: Are formats prestans handlers can send data back as
        self._serializers = serializers
        #: Are formats prestans handlers can accept data as
        self._deserializers = deserializers

        #:
        #: Init the default logger if one's not provided, this allows users to configure their own
        #: http://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
        #:
        if logger is None:
            self._logger = logging.getLogger("prestans.%s" % application_name)
        else:
            self._logger = logger

        #: If serializers and deserialers aren't provided, prestans runs as a JSON app
        if serializers is None:
            self._serializers = [prestans.serializers.JSON()]

        if deserializers is None:
            self._deserializers = [prestans.serializers.JSON()]

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

    def __call__(self, environ, start_response):

        #: Say hello
        self._logger.info("%s exposes %i end-points; prestans %s; charset %s; debug %s" % (
            self._application_name, len(self._routes), prestans.__version__, self._charset, self._debug))

        #: Validate serailziers and deserialzers; are subclasses of prestans.serializers.Serializer
        _default_outgoing_mime_types = list()
        for serializer in self._serializers:

            if not isinstance(serializer, prestans.serializers.Serializer):
                self._logger.error("registered serializer %s.%s does not inherit from prestans.serializers.Serializer" % 
                    (serializer.__module__, serializer.__class__.__name__))

                #: Throw an error message

            _default_outgoing_mime_types.append(serializer.content_type())

        _default_incoming_mime_types = list()
        for deserializer in self._deserializers:

            if not isinstance(deserializer, prestans.deserializers.DeSerializer):
                self._logger.error("registered deserializer %s.%s does not inherit from prestans.serializers.Serializer" % 
                    (deserializer.__module__, deserializer.__class__.__name__))

            _default_incoming_mime_types.append(deserializer.content_type())

        #: Report on the acceptable mime types
        self._logger.info("generally accepts %s; speaks %s" % 
            (str(_default_outgoing_mime_types).strip("[]'"), str(_default_incoming_mime_types).strip("[]'")))

        #: Attempt to parse the HTTP request
        request = Request(environ, self._charset)

        #: Check if the requested URL has a valid registered handler
        # for regexp, handler_class in self._parsed_handler_map:
        #     pass

        #: Run a request parser
    
        #: Say Goodbye
        return "prestans v2 returns nothing at the moment"


