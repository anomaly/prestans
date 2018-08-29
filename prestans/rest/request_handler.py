import inspect

from prestans import exception
from prestans.http import STATUS
from prestans.http import VERB
from prestans import parser
from prestans import provider
from prestans.rest import ErrorResponse
from prestans import types


class RequestHandler(object):
    """
    RequestHandler is a callable that all API end-points must inherit from.
    end-points are instantiated by RequestRouter as a match for a URL.

    This class should not be initialised directly. Subclasses should
    override corresponding methods for HTTP verbs; get, post, delete, put, patch.
    """

    __provider_config__ = None
    __parser_config__ = None

    def __init__(self, args, kwargs, request, response, logger, debug):

        if self.__provider_config__ is None:
            self.__provider_config__ = provider.Config()
        if self.__parser_config__ is None:
            self.__parser_config__ = parser.Config()

        self._args = args
        self._kwargs = kwargs
        self._request = request
        self._response = response
        self._logger = logger
        self._debug = debug

        # initialization used elsewhere
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
            VERB.GET,
            VERB.HEAD,
            VERB.POST,
            VERB.PUT,
            VERB.PATCH,
            VERB.DELETE,
            VERB.OPTIONS
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
        """
        Auto set the return serializer based on Accept headers
        http://docs.webob.org/en/latest/reference.html#header-getters

        Intersection of requested types and supported types tells us if we
        can in fact respond in one of the request formats
        """
        best_accept_match = self.request.accept.best_match(
            self.response.supported_mime_types,
            default_match=self.response.default_serializer.content_type()
        )

        self.logger.info("%s determined as best match for accept header: %s" % (
            best_accept_match,
            self.request.accept
        ))

        # if content_type is not acceptable it will raise UnsupportedVocabulary
        self.response.content_type = best_accept_match

    def __call__(self, environ, start_response):

        self.logger.info("handler %s.%s; callable execution start" % (self.__module__, self.__class__.__name__))

        try:
            # register additional serializers and de-serializers
            self.request.register_deserializers(self.register_deserializers())
            self.response.register_serializers(self.register_serializers())

            request_method = self.request.method

            # ensure we support the HTTP verb
            if not VERB.is_supported_verb(self.request.method):
                unimplemented_verb_error = exception.UnimplementedVerbError(self.request.method)
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

                response_attr_filter_template = verb_parser_config. \
                    response_attribute_filter_template

                # minification support for response attribute filters
                rewrite_template_model = None
                if self.request.is_minified is True:

                    if isinstance(self.response.template, types.Array):
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

                    if not isinstance(parameter_set, parser.ParameterSet):
                        raise TypeError("%s not a subclass of ParameterSet" % parameter_set.__class__.__name__)

                    try:
                        validated_parameter_set = parameter_set.validate(self.request)

                        if validated_parameter_set is not None:
                            self.request.parameter_set = validated_parameter_set
                            break

                    except exception.DataValidationException as exp:
                        self.logger.error(exp)
                        error_response = ErrorResponse(exp, self.response.selected_serializer)
                        return error_response(environ, start_response)

            # parse body
            if not request_method == VERB.GET and verb_parser_config is not None:
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
                if request_method == VERB.GET:
                    self.get(*self._args, **self._kwargs)
                elif request_method == VERB.HEAD:
                    self.head(*self._args, **self._kwargs)
                elif request_method == VERB.POST:
                    self.post(*self._args, **self._kwargs)
                elif request_method == VERB.PUT:
                    self.put(*self._args, **self._kwargs)
                elif request_method == VERB.PATCH:
                    self.patch(*self._args, **self._kwargs)
                elif request_method == VERB.DELETE:
                    self.delete(*self._args, **self._kwargs)
                elif request_method == VERB.OPTIONS:
                    self.options(*self._args, **self._kwargs)
            except (exception.PermanentRedirect, exception.TemporaryRedirect) as exp:
                self._redirect(exp.url, exp.http_status)
            # re-raise all prestans exceptions
            except exception.Base as exp:
                if isinstance(exception, exception.HandlerException):
                    exp.request = self.request

                raise exp
            # handle any non-prestans exceptions
            except Exception as exp:
                self.handler_raised_exception(exp)
            # always run the tear down method
            finally:
                self.handler_did_run()

            self.logger.info("handler %s.%s; callable execution ends" % (
                self.__module__,
                self.__class__.__name__
            ))

            return self.response(environ, start_response)

        except exception.UnimplementedVerbError as exp:
            self.logger.error(exp)
            error_response = ErrorResponse(exp, self.response.selected_serializer)
            return error_response(environ, start_response)

    def register_serializers(self):
        return []

    def register_deserializers(self):
        return []

    def handler_will_run(self):
        return None

    def handler_did_run(self):
        return None

    #:
    #: Default handler for a raised exception return service unavailable
    #:
    def handler_raised_exception(self, exp):
        if self.debug:
            raise exp
        else:
            self.logger.error("handler %s.%s; exception raised: %s" % (
                self.__module__,
                self.__class__,
                exp
            ))
            raise exception.ServiceUnavailable()

    #:
    #: Placeholder functions for HTTP Verb; implementing handlers must override these
    #: if not overridden prestans returns a Not Implemented error
    #:

    def get(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.GET)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def head(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.HEAD)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def post(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.POST)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def put(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.PUT)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def patch(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.PATCH)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def delete(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.DELETE)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def options(self, *args, **kwargs):
        unimplemented_verb_error = exception.UnimplementedVerbError(VERB.OPTIONS)
        unimplemented_verb_error.request = self.request
        raise unimplemented_verb_error

    def _redirect(self, url, status=STATUS.TEMPORARY_REDIRECT):
        self._response.status = status
        self._response.headers.add("Location", url)

    def redirect(self, url, status=STATUS.TEMPORARY_REDIRECT):

        self.logger.warn("direct use of %s.%s has been deprecated please raise an exception instead" % (
            self.__module__,
            "redirect"
        ))

        self._redirect(url, status)
