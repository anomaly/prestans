# -*- coding: utf-8 -*-
#
#  prestans, A WSGI compliant REST micro-framework
#  http://prestans.org
#
#  Copyright (c) 2017, Anomaly Software Pty Ltd.
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
#      * Neither the name of Anomaly Software nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ANOMALY SOFTWARE BE LIABLE FOR ANY
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
import inspect

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

    def __init__(self, environ, charset, logger, deserializers, default_deserializer):

        super(Request, self).__init__(environ=environ, charset=charset)
        self._logger = logger
        self._deserializers = deserializers
        self._default_deserializer = default_deserializer
        self._attribute_filter = None
        self._selected_deserializer = None
        self._parameter_set = None

        self._charset = charset

        self._body_template = None
        self._parsed_body = None

    @property
    def method(self):
        return self.environ['REQUEST_METHOD']

    @property
    def logger(self):
        return self._logger

    @property
    def parsed_body(self):

        if self.body_template is None:
            raise AttributeError("access to request.parsed_body is not \
                allowed when body_tempalte is set to None")

        return self._parsed_body

    @property
    def supported_mime_types(self):
        return [deserializer.content_type() for deserializer in self._deserializers]

    @property
    def supported_mime_types_str(self):
        return ''.join(str(mime_type) + ',' for mime_type in self.supported_mime_types)[:-1]

    @property
    def selected_deserializer(self):
        return self._selected_deserializer

    @property
    def default_deserializer(self):
        return self._default_deserializer

    #: Used by content_type_set to set get a referencey to the serializer object
    def set_deserializer_by_mime_type(self, mime_type):

        for deserializer in self._deserializers:
            if deserializer.content_type() == mime_type:
                self._selected_deserializer = deserializer
                return

        raise prestans.exception.UnsupportedContentTypeError(mime_type, self.supported_mime_types_str)

    @property
    def attribute_filter(self):
        return self._attribute_filter

    @attribute_filter.setter
    def attribute_filter(self, value):
        """
        Attribute filter that used to parse the request_body. This must be set
        before the body_template parameter is set
        """
        self._attribute_filter = value

    @property
    def parameter_set(self):
        """
        Accessor for parameter_set
        """
        return self._parameter_set

    @parameter_set.setter
    def parameter_set(self, value):
        """
        Mutators for parameter_set
        """
        self._parameter_set = value

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

        if value is None:
            self.logger.warn("body_template is None, parsing will be ignored")
            return

        if not isinstance(value, prestans.types.DataCollection):
            raise AssertionError("body_template must be an instance of \
                prestans.types.DataCollection")

        self._body_template = value

        #: Get a deserializer based on the Content-Type header
        #: Do this here so the handler gets a chance to setup extra serializers
        self.set_deserializer_by_mime_type(self.content_type)

        #: Parse the body using the deserializer
        unserialized_body = self.selected_deserializer.loads(self.body)

        #: Parse the body using the template and attribute_filter
        self._parsed_body = value.validate(unserialized_body, self.attribute_filter, self.is_minified)

    def register_deserializers(self, deserializers):

        for deserializer in self._deserializers:

            if not isinstance(deserializer, prestans.deserializer.Base):
                raise TypeError("registered deserializer %s.%s does not \
                    inherit from prestans.serializer.DeSerializer" % \
                    (deserializer.__module__, deserializer.__class__.__name__))

        self._deserializers = self._deserializers + deserializers


    def get_response_attribute_filter(self, template_filter, template_model=None):
        """
        Prestans-Response-Attribute-List can contain a client's requested
        definition for attributes required in the response. This should match
        the response_attribute_filter_template?
        """

        if template_filter is None or not 'Prestans-Response-Attribute-List' in self.headers:
            return None

        #: Header not set results in a None
        attribute_list_str = self.headers['Prestans-Response-Attribute-List']

        #: Deserialize the header contents using the selected header
        json_deserializer = prestans.deserializer.JSON()
        attribute_list_dictionary = json_deserializer.loads(attribute_list_str)

        #: Construct an AttributeFilter
        attribute_filter = prestans.parser.AttributeFilter(
            from_dictionary=attribute_list_dictionary,
            template_model=template_model
        )

        #: Check template? Do this even through we might have template_model
        #: in case users have made a custom filter
        evaluated_filter = attribute_filter.conforms_to_template_filter(template_filter)

        return evaluated_filter

    @property
    def is_minified(self):

        if not 'Prestans-Minification' in self.headers:
            return False

        return self.headers['Prestans-Minification'].upper() == "ON"


class Response(webob.Response):
    """
    Response is the writable HTTP response. It inherits and leverages
    from webob.Response to do the heavy lifting of HTTP Responses. It adds to
    webob.Response prestans customisations.

    Overrides content_type property to use prestans' serializers with the set body
    """

    def __init__(self, charset, logger, serializers, default_serializer):

        super(Response, self).__init__()

        self._logger = logger
        self._serializers = serializers
        self._default_serializer = default_serializer
        self._selected_serializer = None
        self._template = None
        self._app_iter = []
        self._minify = False
        self._attribute_filter = None
        self._template = None
        self._charset = charset

        #:
        #: IETF hash dropped the X- prefix for custom headers
        #: http://stackoverflow.com/q/3561381
        #: http://tools.ietf.org/html/draft-saintandre-xdash-00
        #:
        self.headers.add('Prestans-Version', prestans.__version__)

    @property
    def minify(self):
        return self._minify

    @minify.setter
    def minify(self, value):
        self._minify = value

    @property
    def logger(self):
        return self._logger

    @property
    def supported_mime_types(self):
        return [serializer.content_type() for serializer in self._serializers]

    @property
    def supported_mime_types_str(self):
        return ''.join(str(mime_type) + ',' for mime_type in self.supported_mime_types)[:-1]

    @property
    def selected_serializer(self):
        return self._selected_serializer

    @property
    def default_serializer(self):
        return self._default_serializer

    #: Used by content_type_set to set get a referencey to the serializer object
    def _set_serializer_by_mime_type(self, mime_type):

        for serializer in self._serializers:
            if serializer.content_type() == mime_type:
                self._selected_serializer = serializer
                return

        raise prestans.exception.UnsupportedVocabularyError(mime_type,\
            self.supported_mime_types_str)

    #:
    #: is an instance of prestans.types.DataType; mostly a subclass of
    #: prestans.types.Model
    #:

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):

        if value is not None and (not isinstance(value, prestans.types.DataCollection) and
           not isinstance(value, prestans.types.BinaryResponse)):
            raise TypeError("template in response must be of type prestans.types.DataCollection or subclass")

        self._template = value

    #:
    #: Attribute filter setup
    #:

    @property
    def attribute_filter(self):
        return self._attribute_filter

    @attribute_filter.setter
    def attribute_filter(self, value):

        if value is not None and not isinstance(value, prestans.parser.AttributeFilter):
            raise TypeError("attribue_filter in response must be of \
                type prestans.types.AttributeFilter")

        self._attribute_filter = value

    #:
    #: content_type; overrides webob.Response line 606
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
        if not isinstance(self._app_iter, prestans.types.BinaryResponse) and value not in self.supported_mime_types:
            raise prestans.exception.UnsupportedVocabularyError(value, self.supported_mime_types_str)

        #: Keep a reference to the selected serializer
        if not isinstance(self._app_iter, prestans.types.BinaryResponse):
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

    content_type = property(
        _content_type__get,
        _content_type__set,
        _content_type__del,
        doc=_content_type__get.__doc__
    )


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
            raise AssertionError("response_template is None; handler can't return a response")

        #: value should be a subclass prestans.types.DataCollection
        if not isinstance(value, prestans.types.DataCollection) and \
        not isinstance(value, prestans.types.BinaryResponse):
            raise TypeError("%s is not a prestans.types.DataCollection \
                or prestans.types.BinaryResponse subclass" % value.__class__.__name__)

        #: Ensure that it matches the return type template
        if not value.__class__ == self.template.__class__:
            raise TypeError("body must of be type %s, given %s" %\
                (self.template.__class__.__name__, value.__class__.__name__))

        #: If it's an array then ensure that element_template matches up
        if isinstance(self.template, prestans.types.Array) and \
        not isinstance(value.element_template, self.template.element_template.__class__):
            raise TypeError("array elements must of be \
                type %s, given %s" % (self.template.element_template.__class__.__name__,\
                    value.element_template.__class__.__name__))

        #: _app_iter assigned to value
        #: we need to serialize the contents before we know the length
        #: deffer the content_length property to be set by getter
        self._app_iter = value

    body = property(_body__get, _body__set, _body__set)

    def register_serializers(self, serializers):
        """
        Adds extra serializers; generally registered during the handler lifecycle
        """
        for serializer in serializers:

            if not isinstance(serializer, prestans.serializer.Base):
                raise TypeError("registered serializer %s.%s does not inherit from \
                    prestans.serializer.Serializer" % (serializer.__module__,\
                        serializer.__class__.__name__))

        self._serializers = self._serializers + serializers

    def __call__(self, environ, start_response):
        """
        Overridden WSGI application interface
        """

        #: prestans' equivalent of webob.Response line 1022
        if self.template is None or self.status_code == prestans.http.STATUS.NO_CONTENT:

            start_response(self.status, self.headerlist)

            if self.template is not None:
                self.logger.warn("handler returns No Content but has a \
                    response_template; set template to None")

            return []

        #: Ensure what we are able to serialize is serializable
        if not isinstance(self._app_iter, prestans.types.DataCollection) and\
         not isinstance(self._app_iter, prestans.types.BinaryResponse):

            if isinstance(self._app_iter, list):
                type = "list"
            else:
                type = self._app_iter.__name__

            raise TypeError("handler returns content of type %s; not a prestans.types.DataCollection subclass" % type)

        if isinstance(self._app_iter, prestans.types.DataCollection):

            #: See if attribute filter is completely invisible
            if self.attribute_filter is not None:

                #: Warning to say nothing is visible
                if not self.attribute_filter.are_any_attributes_visible():
                    self.logger.warn("attribute_filter has all the attributes turned \
                        off, handler will return an empty response")

                #: Warning to say none of the fields match
                model_attribute_filter = None
                if isinstance(self._app_iter, prestans.types.Array):
                    model_attribute_filter = prestans.parser.AttributeFilter.\
                    from_model(self._app_iter.element_template)
                elif isinstance(self._app_iter, prestans.types.Model):
                    model_attribute_filter = prestans.parser.AttributeFilter.\
                    from_model(self._app_iter)

                if model_attribute_filter is not None:
                    try:
                        model_attribute_filter.conforms_to_template_filter(self.attribute_filter)
                    except prestans.exception.AttributeFilterDiffers as exception:
                        exception.request = self.request
                        self.logger.warn("%s" %  exception)

            #: Body should be of type DataCollection try; attempt calling
            #: as_seriable with available attribute_filter
            serializable_body = self._app_iter.as_serializable(self.attribute_filter, self.minify)

            #: attempt serializing via registered serializer
            stringified_body = self._selected_serializer.dumps(serializable_body)

            if not isinstance(stringified_body, str):
                raise TypeError("%s dumps must return a python str \
                    not %s" % (self._selected_serializer.__class__.__name__, \
                        stringified_body.__class__.__name__))

            #: set content_length
            self.content_length = len(stringified_body)

            start_response(self.status, self.headerlist)
            return [stringified_body]

        elif isinstance(self._app_iter, prestans.types.BinaryResponse):

            if self._app_iter.content_length == 0 or \
            self._app_iter.mime_type == None or \
            self._app_iter.file_name == None:
                self.logger.warn("Failed to write binar response with content_length \
                    %i; mime_type %s; file_name %s" % (self._app_iter.content_length, \
                        self._app_iter.mime_type, self._app_iter.file_name))
                self.status = prestans.http.STATUS.INTERNAL_SERVER_ERROR
                self.content_type = "text/plain"
                return []

            #: Content type
            self.content_type = self._app_iter.mime_type

            #: Add content disposition header
            if self._app_iter.as_attachment:
                self.headers.add('Content-Disposition', \
                    "attachment; filename=\"%s\"" % self._app_iter.file_name)
            else:
                self.headers.add('Content-Disposition', \
                    "inline; filename=\"%s\"" % self._app_iter.file_name)

            #: Write out response
            self.content_length = self._app_iter.content_length

            start_response(self.status, self.headerlist)
            return [self._app_iter.contents]

        else:
            raise AssertionError("prestans failed to write a binary or textual response")

    def __str__(self):
        #: Overridden so webob's __str__ skips serializing the body
        super(Response, self).__str__(skip_body=True)

#:
#: DictionaryResponse serializes dictionaries using the selected_serializer
#:

class DictionaryResponse(Response):

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
        return self._app_iter


    def _body__set(self, value):

        #: value should be a subclass prestans.types.DataCollection
        if not isinstance(value, dict):
            raise TypeError("%s is not a dictionary" %\
                value.__class__.__name__)

        #: _app_iter assigned to value
        #: we need to serialize the contents before we know the length
        #: deffer the content_length property to be set by getter
        self._app_iter = value

    body = property(_body__get, _body__set, _body__set)

    def __call__(self, environ, start_response):

        start_response(self.status, self.headerlist)

        #: attempt serializing via registered serializer
        stringified_body = self._selected_serializer.dumps(self.body)

        if not isinstance(stringified_body, str):
            raise TypeError("%s dumps must return a python str not %s" %\
                (self._selected_serializer.__class__.__name__,\
                    stringified_body.__class__.__name__))

        #: set content_length
        self.content_length = len(stringified_body)

        return [stringified_body]

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
        self._message = exception.message
        self._stack_trace = exception.stack_trace
        self._trace = None

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

        # we have received a custom error response model, use it instead
        if isinstance(self._exception, prestans.exception.ResponseException) and self._exception.response_model:
            stringified_body = self._serializer.dumps(self._exception.response_model.as_serializable())
        # pack into default format for error response
        else:
            error_dict = dict()

            error_dict['code'] = self.status_int
            error_dict['message'] = self._message
            error_dict['trace'] = self._stack_trace

            stringified_body = self._serializer.dumps(error_dict)

        self.content_length = len(stringified_body)

        start_response(self.status, self.headerlist)
        return [stringified_body]

    def __str__(self):
        #: Overridden so webob's __str__ skips serializing the body
        super(ErrorResponse, self).__str__(skip_body=True)

#:
#: Base Request handler; all handlers must subclass this
#:


class RequestHandler(object):
    """
    RequestHandler is a callable that all API end-points must inherit from.
    end-points are instantiated by RequestRouter as a match for a URL.

    This class should not be initialised directly. Subclasses should
    override corresponding methods for HTTP verbs; get, post, delete, put, patch.
    """

    __provider_config__ = None
    __parser_config__ = None

    def __init__(self, args, request, response, logger, debug):

        if self.__provider_config__ is None:
            self.__provider_config__ = prestans.provider.Config()
        if self.__parser_config__ is None:
            self.__parser_config__ = prestans.parser.Config()


        self._args = args
        self._request = request
        self._response = response
        self._logger = logger
        self._debug = debug

        #: Initalization used elsewhere
        self.provider_authentication = None

    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response

    @property
    def logger(self):
        return self._logger

    @property
    def debug(self):
        return self._debug

    def blueprint(self):

        handler_blueprint = dict()

        signature_map = [
            prestans.http.VERB.GET,
            prestans.http.VERB.HEAD,
            prestans.http.VERB.POST,
            prestans.http.VERB.PUT,
            prestans.http.VERB.PATCH,
            prestans.http.VERB.DELETE
        ]

        #: Provider configuration
        provider_blueprint = None

        if self.__class__.__provider_config__ is not None:
            provider_blueprint = self.__class__.__provider_config__.blueprint()

        handler_blueprint['provider_config'] = provider_blueprint

        # Make a list of methods supported by this handler
        for http_verb in signature_map:

            http_verb_lower = http_verb.lower()
            local_function_handle = getattr(self, http_verb_lower).__func__

            # Ignore if the local signature is the same as the base method
            if local_function_handle is getattr(RequestHandler, http_verb_lower).__func__:
                continue

            verb_blueprint = dict()

            # Docstring
            verb_blueprint['description'] = inspect.getdoc(local_function_handle)

            # Arguments, get the first set of parameters for the
            # function handle and ignore echoing self
            verb_blueprint['arguments'] = inspect.getargspec(local_function_handle)[0][1:]

            #: Parser configuration
            parser_blueprint = None

            if self.__class__.__parser_config__ is not None and \
            self.__class__.__parser_config__.get_config_for_verb(http_verb) is not None:

                parser_config = self.__class__.__parser_config__.get_config_for_verb(http_verb)
                parser_blueprint = parser_config.blueprint()

            verb_blueprint['parser_config'] = parser_blueprint

            handler_blueprint[http_verb] = verb_blueprint

        return handler_blueprint

    def _setup_serializers(self):

        #:
        #: Auto set the return serializer based on Accept headers
        #: http://docs.webob.org/en/latest/reference.html#header-getters
        #:

        #: Intersection of requested types and supported types tells us if we
        #: can in fact respond in one of the request formats
        best_accept_match = self.request.accept.best_match(
            self.response.supported_mime_types,
            default_match=self.response.default_serializer.content_type()
        )

        if best_accept_match is None:
            self.logger.error("unsupported mime type in request; accept header reads %s" %\
                self.request.accept)
            raise prestans.exception.UnsupportedVocabularyError(
                self.request.accept,
                self.response.supported_mime_types_str
            )

        #: If content_type is not acceptable it will raise UnsupportedVocabulary
        self.response.content_type = best_accept_match

    def __call__(self, environ, start_response):

        self.logger.info("handler %s.%s; callable execution start" % (self.__module__, self.__class__.__name__))
        self.logger.info("setting default response to %s" % self.request.accept)

        try:
            #: Register additional serializers and de-serializers
            self.request.register_deserializers(self.register_deserializers())
            self.response.register_serializers(self.register_serializers())

            request_method = self.request.method

            #: Ensure we support the HTTP verb
            if not prestans.http.VERB.is_supported_verb(self.request.method):
                unimplemented_verb_error = prestans.exception.UnimplementedVerbError(self.request.method)
                unimplemented_verb_error.request = self.request
                raise unimplemented_verb_error

            #: Setup serializers
            self._setup_serializers()

            #: Authentication
            if self.__provider_config__.authentication is not None:
                self.__provider_config__.authentication.debug = self.debug
                self.provider_authentication = self.__provider_config__.authentication
                self.provider_authentication.request = self.request

            #: Configuration as provided by the API or default of a VerbConfig object
            verb_parser_config = self.__parser_config__.get_config_for_verb(request_method)

            #: Dress up the request and response with verb configuration
            if verb_parser_config is not None and verb_parser_config.response_template is not None:

                #: Set the response template and attribute filter
                self.response.template = verb_parser_config.response_template

                response_attr_filter_template = verb_parser_config.\
                response_attribute_filter_template

                #: Minification support for response attribute filters
                rewrite_template_model = None
                if self.request.is_minified is True:

                    if isinstance(self.response.template, prestans.types.Array):
                        rewrite_template_model = self.response.template.element_template
                    else:
                        rewrite_template_model = self.response.template

                #: Response attribute filter
                self.response.attribute_filter = self.request.get_response_attribute_filter(
                    response_attr_filter_template,
                    rewrite_template_model
                )

                #: If the header is omitted then we ensure the response has a default template
                #: at this point we can assume that we are going to sent down a response
                if self.response.attribute_filter is None:
                    self.response.attribute_filter = response_attr_filter_template

            #: Parameter sets
            if verb_parser_config is not None and len(verb_parser_config.parameter_sets) > 0:

                for parameter_set in verb_parser_config.parameter_sets:

                    if not isinstance(parameter_set, prestans.parser.ParameterSet):
                        raise TypeError("%s not a subclass of ParameterSet" % parameter_set.__class__.__name__)

                    try:
                        validated_parameter_set = parameter_set.validate(self.request)
                        
                        if validated_parameter_set is not None:
                            self.request.parameter_set = validated_parameter_set
                            break

                    except prestans.exception.DataValidationException as exp:
                        self.logger.error(exp)
                        error_response = ErrorResponse(exp, self.response.selected_serializer)
                        return error_response(environ, start_response)

            #: Parse body
            if not request_method == prestans.http.VERB.GET and verb_parser_config is not None:
                self.request.attribute_filter = verb_parser_config.request_attribute_filter
                #: Setting this runs the parser for the body
                #: Request will determine which serializer to use based on Content-Type
                self.request.body_template = verb_parser_config.body_template

            #: Warm up
            self.handler_will_run()

            try:
                #:
                #: See if the handler supports the called method
                #: prestans sets a sensible HTTP status code
                #:
                if request_method == prestans.http.VERB.GET:
                    self.get(*self._args)
                elif request_method == prestans.http.VERB.HEAD:
                    self.head(*self._args)
                elif request_method == prestans.http.VERB.POST:
                    self.post(*self._args)
                elif request_method == prestans.http.VERB.PUT:
                    self.put(*self._args)
                elif request_method == prestans.http.VERB.PATCH:
                    self.patch(*self._args)
                elif request_method == prestans.http.VERB.DELETE:
                    self.delete(*self._args)
            #: Re-raise all prestans exceptions
            except prestans.exception.Base as exception:
                if issubclass(exception.__class__, prestans.exception.HandlerException):
                    exception.request = self.request

                raise exception
            #: Handle any non-prestans exceptions
            except Exception as exp:
                if self.debug:
                    raise
                else:
                    self.logger.exception("handler %s.%s; exception raised: %s" % (\
                        self.__module__,
                        self.__class__,
                        exp
                    ))
                    raise prestans.exception.ServiceUnavailable()
            #: Always run the tear down method
            finally:
                self.handler_did_run()

            self.logger.info("handler %s.%s; callable execution ends" % \
                (self.__module__, self.__class__.__name__))

            return self.response(environ, start_response)

        except prestans.exception.UnimplementedVerbError as exp:
            self.logger.error(exp)
            error_response = ErrorResponse(exp, self.response.selected_serializer)
            return error_response(environ, start_response)

    def register_serializers(self):
        return []

    def register_deserializers(self):
        return []

    #:
    #: Placeholder functions for lifecycle methods
    #:

    def handler_will_run(self):
        return None

    def handler_did_run(self):
        return None

    #:
    #: Placeholder functions for HTTP Verb; implementing handlers must override these
    #: if not overridden prestans returns a Not Implemented error
    #:

    def get(self, *args):
        unimplemented_verb_error = prestans.exception.UnimplementedVerbError(prestans.http.VERB.GET)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def head(self, *args):
        unimplemented_verb_error = prestans.exception.UnimplementedVerbError(prestans.http.VERB.HEAD)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def post(self, *args):
        unimplemented_verb_error = prestans.exception.UnimplementedVerbError(prestans.http.VERB.POST)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def put(self, *args):
        unimplemented_verb_error = prestans.exception.UnimplementedVerbError(prestans.http.VERB.PUT)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def patch(self, *args):
        unimplemented_verb_error = prestans.exception.UnimplementedVerbError(prestans.http.VERB.PATCH)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def delete(self, *args):
        unimplemented_verb_error = prestans.exception.UnimplementedVerbError(prestans.http.VERB.DELETE)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def redirect(self, url, status=prestans.http.STATUS.TEMPORARY_REDIRECT):

        self._response.status = status
        self._response.headers.add("Location", url)


#:
#: Generates a blueprint of the handler and serializes it using the requested
#: Accept header.
#:

class BlueprintHandler(RequestHandler):

    def __init__(self, args, request, response, logger, debug, route_map):

        super(BlueprintHandler, self).__init__(args, request, response, logger, debug)
        self._route_map = route_map

    def _create_blueprint(self):

        blueprint_groups = dict()

        # Intterogate each handler
        for regexp, handler_class in self.route_map:

            # Ignore discovery handler
            if issubclass(handler_class, BlueprintHandler):
                continue

            handler_blueprint = dict()
            handler_blueprint['url'] = regexp
            handler_blueprint['handler_class'] = handler_class.__name__
            handler_blueprint['description'] = inspect.getdoc(handler_class)
            handler_blueprint['supported_methods'] = handler_class(self._args, self.request,\
                self.response, self.logger, self.debug).blueprint()

            if not handler_class.__module__ in blueprint_groups:
                blueprint_groups[handler_class.__module__] = []
            # Make a new group per module if one doesnt' exist

            blueprint_groups[handler_class.__module__].append(handler_blueprint)

        return blueprint_groups

    @property
    def route_map(self):
        return self._route_map

    @route_map.setter
    def route_map(self, value):
        self._route_map = value

    def __call__(self, environ, start_response):

        #: Setup serializers
        self._setup_serializers()

        self.response.status = prestans.http.STATUS.OK

        self.response.body = self._create_blueprint()

        return self.response(environ, start_response)


#:
#: Maps URLs to handlers classes and routes requests based on patterns
#: this is used to init a prestans application
#:

class RequestRouter(object):
    """
    RequestRouter is a specialised WSGI router that primarily maps URLs to Handlers.
    All registered end-points must inherit from RequestHandler.

    RequestRouter sets the most likely response format based on Accept Headers. If
    no supported response format is found; RequestRouter sends back an HTML error.

    If the requested URL is not handled with the API; RequestRouter presents the
    client with a standardised error message.

    """

    def __init__(self, routes, serializers=None, default_serializer=None, deserializers=None,
                 default_deserializer=None, charset="utf-8", application_name="prestans",
                 logger=None, debug=False, description=None):

        self._application_name = application_name
        self._debug = debug
        self._routes = routes
        self._charset = charset
        self._description = description

        #: Are formats prestans handlers can send data back as
        self._serializers = serializers
        self._default_serializer = default_serializer
        #: Are formats prestans handlers can accept data as
        self._deserializers = deserializers
        self._default_deserializer = default_deserializer

        #:
        #: Init the default logger if one's not provided, this allows users to configure their own
        #: http://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
        #:
        if logger is None:
            logging.basicConfig()
            self._logger = logging.getLogger("prestans.%s" % application_name)
        else:
            self._logger = logger

        #: Set logger level, API can override this
        if self._debug == True:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.ERROR)

        #: If serializers and deserialers aren't provided, prestans runs as a JSON app
        if serializers is None:
            self._serializers = [prestans.serializer.JSON()]

        if default_serializer is None:
            self._default_serializer = prestans.serializer.JSON()

        #: Deserializers

        if deserializers is None:
            self._deserializers = [prestans.deserializer.JSON()]

        if default_deserializer is None:
            self._default_deserializer = prestans.deserializer.JSON()

    @property
    def logger(self):
        return self._logger

    @property
    def description(self):
        return self._description

    @property
    def charset(self):
        return self._charset

    @property
    def debug(self):
        return self._debug

    @property
    def application_name(self):
        return self._application_name

    def __call__(self, environ, start_response):

        #: Say hello
        self.logger.info("%s exposes %i end-points; prestans %s; charset %s; debug %s" % \
            (self._application_name, len(self._routes), prestans.__version__, \
                self._charset, self._debug))

        #: Validate serializers and deserializers; are subclasses of prestans.serializer.Serializer
        _default_outgoing_mime_types = list()
        for serializer in self._serializers:

            if not isinstance(serializer, prestans.serializer.Base):
                raise TypeError("registered serializer %s.%s does not \
                    inherit from prestans.serializer.Serializer" % (serializer.__module__, \
                        serializer.__class__.__name__))

            _default_outgoing_mime_types.append(serializer.content_type())

        _default_incoming_mime_types = list()
        for deserializer in self._deserializers:

            if not isinstance(deserializer, prestans.deserializer.Base):
                raise TypeError(
                    "registered deserializer %s.%s does not inherit from \
                    prestans.serializer.DeSerializer"\
                     % (deserializer.__module__, deserializer.__class__.__name__))

            _default_incoming_mime_types.append(deserializer.content_type())

        #: Report on the acceptable mime types
        self._logger.info("generally accepts %s; speaks %s" %\
            (str(_default_outgoing_mime_types).strip("[]'"),\
                str(_default_incoming_mime_types).strip("[]'")))

        #: Attempt to parse the HTTP request
        request = Request(environ=environ, charset=self._charset, \
            logger=self._logger, deserializers=self._deserializers, \
            default_deserializer=self._default_deserializer)

        #: Initialise the Route map
        route_map = self._init_route_map(self._routes)

        try:

            #: Check if the requested URL has a valid registered handler
            for regexp, handler_class in route_map:

                # if not 'PATH_INFO' in environ.keys():

                match = regexp.match(environ.get("PATH_INFO", "")) # if absent, can assume to be empty string # https://www.python.org/dev/peps/pep-3333/#environ-variables

                #: If we've found a match; ensure its a handler subclass and return it's callable
                if match:

                    if issubclass(handler_class, BlueprintHandler):

                        response = DictionaryResponse(charset=self._charset, logger=self._logger,\
                            serializers=self._serializers, \
                            default_serializer=self._default_deserializer)

                        request_handler = handler_class(args=match.groups(), \
                            request=request, response=response,\
                            logger=self._logger, debug=self._debug, route_map=self._routes)

                    else:

                        response = Response(charset=self._charset, logger=self._logger, \
                            serializers=self._serializers, \
                            default_serializer=self._default_deserializer)

                        response.minify = request.is_minified

                        request_handler = handler_class(args=match.groups(), request=request, \
                            response=response, logger=self._logger, debug=self._debug)

                    return request_handler(environ, start_response)

            #: Request does not have a matched handler
            no_endpoint = prestans.exception.NoEndpointError()
            no_endpoint.request = request
            raise no_endpoint

        except prestans.exception.Base as exp:
            self.logger.error(exp)
            error_response = ErrorResponse(exp, self._default_serializer)
            return error_response(environ, start_response)

    def _init_route_map(self, routes):

        parsed_handler_map = []

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
