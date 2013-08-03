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

import re
import webob
import logging

import prestans
import prestans.http
import prestans.parser
import prestans.provider
import prestans.exception
import prestans.serializer
import prestans.deserializer

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
        self._attribute_filter = None

        self.charset = charset

    @property
    def method(self):
        return self.environ['REQUEST_METHOD']

    @property
    def logger(self):
        return self._logger

    @property
    def parsed_body(self):
        return self._parsed_body

    @property
    def supported_mime_types(self):
        return [deserializer.content_type() for deserializer in self._deserializers]

    @property
    def selected_deserializer(self):
        return self._selected_deserializer
        
    #: Used by content_type_set to set get a referencey to the serializer object
    def _set_deserializer_by_mime_type(self, mime_type):

        for deserializer in self._deserializers:
            if deserializer.content_type() == mime_type:
                self._selected_deserializer = deserializer
                return

        raise prestans.exception.UnsupportedVocabularyError()

    @property
    def attribute_filter(self):
        return self._attribute_filter

    @attribute_filter.setter
    def attribute_filter(self, value):
        """
        Attribute filter that used to parse the request_body. This must be set
        before the body_template parameter is set
        """
        self._response_attribute_filter = value

    @property
    def body_template(self):
        return self._body_template

    @body_template.setter
    def body_template(self, value):
        """
        Must be an instance of a prestans.types.DataCollection subclass; this is
        generally set during the RequestHandler lifecycle. Setting this spwans the
        parsing process of the body. If the HTTP verb is GET an AssertionError is
        thrown. Use with extreme caution.
        """

        if self.method == prestans.http.VERB.GET:
            raise AssertionError("body_template cannot be set for GET requests")

        if not isinstance(value, prestans.types.DataCollection):
            raise AssertionError("body_template must be an instance of prestans.types.DataCollection")

        self._body_template = value

        #: Get a deserializer based on the Content-Type header
        self._set_deserializer_by_mime_type(self.content_type)

        #: Parse the body using the deserializer
        unserialized_body = self.selected_deserializer.loads(self.body)

        #: Parse the body using the remplate and attribute_filter
        self._parsed_body = value.validate(unserialized_body, self.attribute_filter)

    @property
    def response_attribute_filter(self):
        """
        Prestans-Response-Attribute-Filter can contain a client's requested 
        definition for attributes required in the response. This should match
        the response_attribute_fitler_tempalte? 
        """
        return None



class Response(webob.Response):
    """
    Response is the writable HTTP response. It inherits and leverages 
    from webob.Response to do the heavy lifiting of HTTP Responses. It adds to
    weob.Response prestans customisations.

    Overrides content_type property to use prestans' serializers with the set body
    """

    def __init__(self, charset, logger, serializers):
        
        super(Response, self).__init__()

        self._logger = logger
        self._serializers = serializers
        self._selected_serializer = None
        self._template = None
        self._app_iter = None

        #: 
        #: IETF hash dropped the X- prefix for custom headers
        #: http://stackoverflow.com/q/3561381 
        #: http://tools.ietf.org/html/draft-saintandre-xdash-00
        #:
        self.headers.add('Prestans-Version', prestans.__version__)

    @property
    def logger(self):
        return self._logger

    @property
    def supported_mime_types(self):
        return [serializer.content_type() for serializer in self._serializers]

    @property
    def selected_serializer(self):
        return self._selected_serializer

    #: Used by content_type_set to set get a referencey to the serializer object
    def _set_serializer_by_mime_type(self, mime_type):

        for serializer in self._serializers:
            if serializer.content_type() == mime_type:
                self._selected_serializer = serializer
                return

        raise prestans.exception.UnsupportedVocabularyError()

    #:
    #: is an instance of prestans.types.DataType; mostly a subclass of 
    #: prestans.types.Model
    #:

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):

        if not isinstance(value, prestans.types.DataCollection):
            raise TypeError("template in response must be of type prestans.types.DataCollection or subclass")

        self._template = value


    #:
    #: Attribute filter rsetup
    #:

    @property
    def attribute_filter(self):
        return self._attribute_filter

    @attribute_filter.setter
    def attribute_filter(self, value):

        if not isinstance(value, prestans.parser.AttributeFilter):
            raise TypeError("attribue_filter in response must be of type prestans.types.AttributeFilter")

        self._attribute_filter = value

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
            raise prestans.exception.UnsupportedVocabularyError()

        #: Keep a reference to the selected serializer
        self._set_serializer_by_mime_type(value)

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
        Overridden response does not support md5, text or json properties. _app_iter
        is set using rules defined by prestans.

        body getter will return the validated prestans model.

        Webob does the heavy lifiting with headers. 
        """

        #: If template is null; return an empty iterable
        if self.template is None:
            return []

        return self._app_iter


    def _body__set(self, value):

        #: If not response template; we have to assume its NO_CONTENT
        #: hence do not allow setting the body
        if self.template is None:
            raise AssertionError("resposne template is None; handler can't return a response")

        #: value should be a subclass prestans.types.DataCollection
        if not issubclass(value.__class__, prestans.types.DataCollection):
            raise TypeError("%s is not a prestans.types.DataCollection subclass" % 
                value.__class__.__name__)

        #: Ensure that it matches the return type template
        if not value.__class__ == self.template.__class__:
            raise TypeError("body must of be type %s, given %s" % 
                (self.template.__class__.__name__, value.__class__.__name__))

        #: If it's an array then ensure that element_template matches up
        if isinstance(self.template, prestans.types.Array) and \
        not value.element_template == self.template.element_template:
            raise TypeError("array elements must of be type %s, given %s" % 
                (self.template.element_template.__class__.__name__, 
                    value.element_template.__class__.__name__))

        #: _app_iter assigned to value
        #: we need to serialize the contents before we know the length
        #: deffer the content_length property to be set by getter
        self._app_iter = value

    body = property(_body__get, _body__set, _body__set)

    def __call__(self, environ, start_response):
        """
        Overridden WSGI application interface
        """

        #: prestans' equivalent of webob.Response line 1022
        if self.template is None:
            headerlist = self._abs_headerlist(environ)
            start_response(self.status, headerlist)
            return webob.EmptyResponse(self._app_iter)

        #: Body should be of type DataCollection try; attempt calling
        #: as_seriable with available attribute_filter
        serializable_body = self._app_iter.as_serializable(attribute_filter=self.attribute_filter)

        #: attempt serializing via registered serializer
        stringified_body = self._selected_serializer.dumps(serializable_body)

        #: set content_length
        self.content_length = len(stringified_body)

        #: From webob.Response line 1021
        headerlist = self._abs_headerlist(environ)
        start_response(self.status, headerlist)

        return stringified_body


class ErrorResponse(webob.Response):
    """
    ErrorResponse is a specialised webob.Response, its responsible for writing
    out a message in the following format; using the currently selected serializer

      {
          "code": 404,
          "message": "This is an error message",
          "trace": [
            {
                "key": "value"
            }
          ]
      }
    """
    
    def __init__(self, exception, serializer):

        super(ErrorResponse, self).__init__()

        self._exception = exception
        self._serializer = serializer
        self._message = str(exception)
        self._trace = list()

        #: 
        #: IETF hash dropped the X- prefix for custom headers
        #: http://stackoverflow.com/q/3561381 
        #: http://tools.ietf.org/html/draft-saintandre-xdash-00
        #:
        self.headers.add('Prestans-Version', prestans.__version__)

        self.content_type = self._serializer.content_type()
        self.status = exception.http_status

    @property
    def trace(self):
        return self._trace

    def append_to_trace(self, trace_entry):
        """
        Use this to append to the stack trace
        """
        self._trace.append(trace_entry)

    def __call__(self, environ, start_response):

        #: From webob.Response line 1021
        headerlist = self._abs_headerlist(environ)
        start_response(self.status, headerlist)

        error_dict = dict()

        error_dict['code'] = self.status
        error_dict['message'] = self._message
        error_dict['trace'] = self._trace

        stringified_body = self._serializer.dumps(error_dict)
        self.content_length = len(stringified_body)

        return stringified_body



class RequestHandler(object):
    """
    RequestHandler is a callable that all API end-points must inherit from. 
    end-points are instantiated by RequestRouter as a match for a URL.

    This class should not be initialised directly. Subclasses should 
    override corresponding methods for HTTP verbs; get, post, delete, put, patch.
    """

    __provider_config__ = prestans.provider.Config()    
    __parser_config__ = prestans.parser.Config()

    def __init__(self, args, request, response, logger, debug=False):

        self._args = args
        self._request = request
        self._response = response
        self._logger = logger
        self._debug = debug

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

        try:

            request_method = self.request.method

            #: Ensure we support the HTTP verb
            if not prestans.http.VERB.is_supported_verb(self.request.method):
                pass

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
                raise prestans.exception.UnsupportedVocabularyError()

            #: If content_type is not acceptable it will raise UnsupportedVocabulary
            self.response.content_type = self.request.accept.best_match(_supportable_mime_types)

            #: Authentication
            # self.logger.error(self.__provider_config__.authentication)

            #: Configuration as provided by the API or default of a VerbConfig object
            verb_parser_config = self.__parser_config__.get_config_for_verb(request_method)

            #: Set the response template and attribute filter
            self.response.template = verb_parser_config.response_template
            self.response.attribute_filter = verb_parser_config.response_attribute_filter_template

            #: Parameter sets
            if verb_parser_config is not None and len(verb_parser_config.parameter_sets) > 0:
                pass

            #: Parse body
            if not request_method == prestans.http.VERB.GET and verb_parser_config is not None:
                self.request.attribute_filter = verb_parser_config.request_attribute_filter
                #: Setting this runs the parser for the body
                #: Request will determine which serializer to use based on Content-Type
                self.request.body_template = verb_parser_config.body_template

            #: Warm up
            self.handler_will_run()

            #:
            #: See if the handler supports the called method
            #: prestans sets a sensible HTTP status code
            #:
            if request_method == prestans.http.VERB.GET:
                self.response.status = prestans.http.STATUS.OK
                self.get(*self._args)
            elif request_method == prestans.http.VERB.HEAD:
                self.response.status = prestans.http.STATUS.NO_CONTENT
                self.head(*self._args)
            elif request_method == prestans.http.VERB.POST:
                self.response.status = prestans.http.STATUS.CREATED
                self.post(*self._args)
            elif request_method == prestans.http.VERB.PATCH:
                self.response.status = prestans.http.STATUS.ACCEPTED
                self.patch(*self._args)
            elif request_method == prestans.http.VERB.DELETE:
                self.response.status = prestans.http.STATUS.NO_CONTENT
                self.delete(*self._args)
            elif request_method == prestans.http.VERB.PUT:
                self.response.status = prestans.http.STATUS.ACCEPTED
                self.put(*self._args)

            #: Tear down
            self.handler_did_run()

            self.logger.info("handler %s.%s; callable excution ends" 
                % (self.__module__, self.__class__.__name__))

            return self.response(environ, start_response)

        except prestans.exception.UnimplementedVerb, exp:
            error_response = ErrorResponse(exp, self.response.selected_serializer)
            self.logger.error(exp)
            return error_response(environ, start_response)


    #:
    #: Placeholder functions for HTTP Verb; implementing handlers must override these
    #: if not overridden prestans returns a Not Implemented error
    #:

    def handler_will_run(self):
        return None

    def get(self, *args):
        raise prestans.exception.UnimplementedVerb("GET")

    def head(self, *args):
        raise prestans.exception.UnimplementedVerb("HEAD")

    def post(self, *args):
        raise prestans.exception.UnimplementedVerb("POST")

    def put(self, *args):
        raise prestans.exception.UnimplementedVerb("PUT")

    def patch(self, *args):
        raise prestans.exception.UnimplementedVerb("PATCH")

    def delete(self, *args):
        raise prestans.exception.UnimplementedVerb("DELETE")

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
            self._serializers = [prestans.serializer.JSON()]

        if deserializers is None:
            self._deserializers = [prestans.deserializer.JSON()]


    def __call__(self, environ, start_response):

        #: Say hello
        self._logger.info("%s exposes %i end-points; prestans %s; charset %s; debug %s" % (
            self._application_name, len(self._routes), prestans.__version__, self._charset, self._debug))

        #: Validate serailziers and deserialzers; are subclasses of prestans.serializer.Serializer
        _default_outgoing_mime_types = list()
        for serializer in self._serializers:

            if not isinstance(serializer, prestans.serializer.Base):
                self._logger.error("registered serializer %s.%s does not inherit from prestans.serializer.Serializer" % 
                    (serializer.__module__, serializer.__class__.__name__))

                #: Throw an error message

            _default_outgoing_mime_types.append(serializer.content_type())

        _default_incoming_mime_types = list()
        for deserializer in self._deserializers:

            if not isinstance(deserializer, prestans.deserializer.Base):
                self._logger.error("registered deserializer %s.%s does not inherit from prestans.serializer.DeSerializer" % 
                    (deserializer.__module__, deserializer.__class__.__name__))

            _default_incoming_mime_types.append(deserializer.content_type())

        #: Report on the acceptable mime types
        self._logger.info("generally accepts %s; speaks %s" % 
            (str(_default_outgoing_mime_types).strip("[]'"), str(_default_incoming_mime_types).strip("[]'")))

        #: Attempt to parse the HTTP request
        request = Request(environ=environ, charset=self._charset, logger=self._logger, 
            deserializers=self._deserializers)
        response = Response(charset=self._charset, logger=self._logger, serializers=self._serializers)

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

        except prestans.exception.UnsupportedVocabularyError, exp:
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
