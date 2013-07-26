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

import prestans
import prestans.http
import prestans.exceptions
import prestans.serializers
import prestans.deserializers

class Request(webob.Request):
    """
    Request is parsed REST Request; it's inherits and relies on Webob.Request to
    do the heavy lifiting of parsing HTTP requests. It adds on top parsing of 
    REST bodies and parameter sets based on rules set by the prestans app.

    It's responsible for making sense of the prestans headers and making them
    available to the RequestHandler
    """

    def __init__(self, environ, charset, logger, deserializers):

        super(Request, self).__init__(environ=environ, charset=charset)
        self._logger = logger
        self._deserializers = deserializers

    @property
    def supported_mime_types(self):
        return [deserializer.content_type() for deserializer in self._deserializers]

    @property
    def method(self):
        return self.environ['REQUEST_METHOD']

    @property
    def attribute_filter(self):
        #: Return a attribute filter if set in the request header
        pass


class Response(webob.Response):
    """
    Response is the writable HTTP response. It inherits and leverages 
    from webob.Response to do the heavy lifiting of HTTP Responses. It adds to
    weob.Response prestans customisations.

    Overrides content_type property to use prestans' serializers with the set body
    """

    def __init__(self, logger, serializers):
        
        super(Response, self).__init__()

        self._logger = logger
        self._serializers = serializers
        self._selected_serializer = None

        #: 
        #: IETF hash dropped the X- prefix for custom headers
        #: http://stackoverflow.com/q/3561381 
        #: http://tools.ietf.org/html/draft-saintandre-xdash-00
        #:
        self.headers.add('Prestans-Version', prestans.__version__)

    @property
    def supported_mime_types(self):
        return [serializer.content_type() for serializer in self._serializers]

    #:
    #: content_type; overrides webob.Resposne line 606
    #:

    def _content_type__get(self):
        """
        Get/set the Content-Type header (or None), *without* the
        charset or any parameters.

        If you include parameters (or ``;`` at all) when setting the
        content_type, any existing parameters will be deleted;
        otherwise they will be preserved.
        """
        header = self.headers.get('Content-Type')
        if not header:
            return None
        return header.split(';', 1)[0]

    def _content_type__set(self, value):

        #: Check to see if response can support the requested mime type
        if value not in self.supported_mime_types:
            raise prestans.exceptions.UnsupportedVocabulary()

        #: Keep a reference to the selected serializer

        if not value:
            self._content_type__del()
            return
        if ';' not in value:
            header = self.headers.get('Content-Type', '')
            if ';' in header:
                params = header.split(';', 1)[1]
                value += ';' + params
        self.headers['Content-Type'] = value

    def _content_type__del(self):
        self.headers.pop('Content-Type', None)

    content_type = property(_content_type__get, _content_type__set,
                            _content_type__del, doc=_content_type__get.__doc__)


    #:
    #: body; overrides webob.Response line 324
    #:

    def _body__get(self):
        """
        The body of the response, as a ``str``.  This will read in the
        entire app_iter if necessary.
        """
        app_iter = self._app_iter
#         try:
#             if len(app_iter) == 1:
#                 return app_iter[0]
#         except:
#             pass
        if isinstance(app_iter, list) and len(app_iter) == 1:
            return app_iter[0]
        if app_iter is None:
            raise AttributeError("No body has been set")
        try:
            body = b''.join(app_iter)
        finally:
            iter_close(app_iter)
        if isinstance(body, text_type):
            raise _error_unicode_in_app_iter(app_iter, body)
        self._app_iter = [body]
        if len(body) == 0:
            # if body-length is zero, we assume it's a HEAD response and
            # leave content_length alone
            pass # pragma: no cover (no idea why necessary, it's hit)
        elif self.content_length is None:
            self.content_length = len(body)
        elif self.content_length != len(body):
            raise AssertionError(
                "Content-Length is different from actual app_iter length "
                "(%r!=%r)"
                % (self.content_length, len(body))
            )
        return body

    def _body__set(self, value=b''):
        if not isinstance(value, bytes):
            if isinstance(value, text_type):
                msg = ("You cannot set Response.body to a text object "
                       "(use Response.text)")
            else:
                msg = ("You can only set the body to a binary type (not %s)" %
                       type(value))
            raise TypeError(msg)
        if self._app_iter is not None:
            self.content_md5 = None
        self._app_iter = [value]
        self.content_length = len(value)


    body = property(_body__get, _body__set, _body__set)


class ErrorResponse(webob.Response):
    """
    ErrorResposne is used by exceptions to return

    """
    
    def __init__(self, exception):
        self._exception = exception

class RequestHandler(object):
    """
    RequestHandler is a callable that all API end-points must inherit from. 
    end-points are instantiated by RequestRouter as a match for a URL.

    This class should not be initialised directly. Subclasses should 
    override corresponding methods for HTTP verbs; get, post, delete, put, patch.
    """

    class CONSTANT:
        """
        Supporting constants for RequestHandler callable
        """

        SUPPORTED_VERBS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def __init__(self, args, request, response, logger, debug=False):

        self._args = args
        self._request = request
        self._response = response
        self._debug = debug
        self._logger = logger

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response

    @property
    def logger(self):
        return self._logger

    def __call__(self, environ, start_response):

        self.logger.info("handler %s.%s; callable excution start" 
            % (self.__module__, self.__class__.__name__))

        self.logger.info("setting default response to %s" % self.request.accept)

        #: Ensure we support the HTTP verb
        if not self.request.method in RequestHandler.CONSTANT.SUPPORTED_VERBS:
            pass

        #: Authentication

        #: Parse body

        #: Parse Parameter Set

        #:
        #: Auto set the return serializer based on Accept headers
        #: http://docs.webob.org/en/latest/reference.html#header-getters
        #:

        #: Intersection of requested types and supported types tells us if we
        #: can infact respond in one of the requess formats
        _supportable_mime_types = set(self.request.accept.best_matches()).intersection(
            set(self.response.supported_mime_types))

        if not _supportable_mime_types and len(_supportable_mime_types) < 1:
            self.logger.error("unsupported mime type in request; accept header reads %s" % 
                self.request.accept)
            raise prestans.exceptions.UnsupportedVocabulary()

        #: If content_type is not acceptable it will raise UnsupportedVocabulary
        self.response.content_type = self.request.accept.best_match(_supportable_mime_types)

        #: Warm up
        self.handler_will_run()

        #:
        #: See if the handler supports the called method
        #: prestans sets a sensible HTTP status code
        #:
        if self.request.method == prestans.http.VERB.GET:
            self.response.status = prestans.http.STATUS.OK
            self.get(*self._args)
        elif self.request.method == prestans.http.VERB.POST:
            self.response.status = prestans.http.STATUS.CREATED
            rest_handler.post(*self._args)
        elif self.request.method == prestans.http.VERB.PATCH:
            self.response.status = prestans.http.STATUS.ACCEPTED
            self.patch(*self._args)
        elif self.request.method == prestans.http.VERB.DELETE:
            self.response.status = prestans.http.STATUS.NO_CONTENT
            self.delete(*self._args)
        elif self.request.method == prestans.http.VERB.PUT:
            self.response.status = prestans.http.STATUS.ACCEPTED
            self.put(*self._args)

        #: Tear down
        self.handler_did_run()

        self.logger.info("handler %s.%s; callable excution ends" 
            % (self.__module__, self.__class__.__name__))

        return self.response(environ, start_response)

    #:
    #: Placeholder functions for HTTP Verb; implementing handlers must override these
    #: if not overridden prestans returns a Not Implemented error
    #:

    def handler_will_run(self):
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

    def handler_did_run(self):
        return None


#:
#:
#:

class BlueprintHandler(RequestHandler):
    pass


class RequestRouter(object):
    """
    RequestRouter is a specialised WSGI router that primarily maps URLs to Handlers. 
    All registered end-points must inherit from RequestHandler.

    RequestRouter sets the most likely response format based on Accept Headers. If
    no supported response format is found; RequestRouter sends back an HTML error.

    If the requested URL is not handled with the API; RequestRouter presents the
    client with a standardised error message.

    """

    def __init__(self, routes, serializers=None, deserializers=None, charset="utf-8", 
        application_name="prestans", logger=None, debug=False):

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
            self._deserializers = [prestans.deserializers.JSON()]


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
                self._logger.error("registered deserializer %s.%s does not inherit from prestans.serializers.DeSerializer" % 
                    (deserializer.__module__, deserializer.__class__.__name__))

            _default_incoming_mime_types.append(deserializer.content_type())

        #: Report on the acceptable mime types
        self._logger.info("generally accepts %s; speaks %s" % 
            (str(_default_outgoing_mime_types).strip("[]'"), str(_default_incoming_mime_types).strip("[]'")))

        #: Attempt to parse the HTTP request
        request = Request(environ=environ, charset=self._charset, logger=self._logger, 
            deserializers=self._deserializers)
        response = Response(logger=self._logger, serializers=self._serializers)

        #: Initialise the Route map
        route_map = self._init_route_map(self._routes)

        try:

            #: Check if the requested URL has a valid registered handler
            for regexp, handler_class in route_map:

                match = regexp.match(request.path)

                #: If we've found a match; ensure its a handler subclass and return it's callable
                if match:

                    request_handler = handler_class(args=match.groups(), request=request, response=response, 
                        logger=self._logger, debug=self._debug)

                    return request_handler(environ, start_response)

            #: Request does not have a matched handler
            return "No matching handler for this URL"

        except prestans.exceptions.UnsupportedVocabulary, exp:
            return exp.as_error_response(environ, start_response, 
                request.accept, _default_outgoing_mime_types)


    #:    
    #: @todo Update regular expressions to support webapp2 like routes
    #: the followign code was originally taken from webapp
    #:
    def _init_route_map(self, routes):

        parsed_handler_map = []
        handler_name = None
        
        for regexp, handler in routes:

            try:
                handler_name = handler.__name__
            except AttributeError:
                pass

            #: Patch regular expression if its incomplete 
            if not regexp.startswith('^'):
                regexp = '^' + regexp
            if not regexp.endswith('$'):
                regexp += '$'
                
            compiled_regex = re.compile(regexp)
            parsed_handler_map.append((compiled_regex, handler))
            
        return parsed_handler_map
