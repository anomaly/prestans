import logging
import re

from prestans import __version__
from prestans import deserializer
from prestans import exception
from prestans.rest import BlueprintHandler
from prestans.rest import ErrorResponse
from prestans.rest import DictionaryResponse
from prestans.rest import Request
from prestans.rest import Response
from prestans import serializer


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

        # are formats prestans handlers can send data back as
        self._serializers = serializers
        self._default_serializer = default_serializer
        # are formats prestans handlers can accept data as
        self._deserializers = deserializers
        self._default_deserializer = default_deserializer

        # init the default logger if one's not provided, this allows users to configure their own
        # http://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
        if logger is None:
            logging.basicConfig()
            self._logger = logging.getLogger("prestans.%s" % application_name)
        else:
            self._logger = logger

        # set logger level, API can override this
        if self._debug:
            self._logger.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.ERROR)

        # if serializers and deserializers aren't provided, prestans runs as a JSON app
        if serializers is None:
            self._serializers = [serializer.JSON()]

        if default_serializer is None:
            self._default_serializer = serializer.JSON()

        # deserializers
        if deserializers is None:
            self._deserializers = [deserializer.JSON()]

        if default_deserializer is None:
            self._default_deserializer = deserializer.JSON()

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

        # say hello
        self.logger.info("%s exposes %i end-points; prestans %s; charset %s; debug %s" % (
            self._application_name, len(self._routes), __version__,
            self._charset, self._debug
        ))

        # validate serializers and deserializers; are subclasses of prestans.serializer.Base
        _default_outgoing_mime_types = list()
        for available_serializer in self._serializers:

            if not isinstance(available_serializer, serializer.Base):
                msg = "registered serializer %s.%s does not inherit from prestans.serializer.Serializer" % (
                    available_serializer.__module__,
                    available_serializer.__class__.__name__
                )
                raise TypeError(msg)

            _default_outgoing_mime_types.append(available_serializer.content_type())

        _default_incoming_mime_types = list()
        for available_deserializer in self._deserializers:

            if not isinstance(available_deserializer, deserializer.Base):
                msg = "registered deserializer %s.%s does not inherit from prestans.serializer.DeSerializer" % (
                    available_deserializer.__module__,
                    available_deserializer.__class__.__name__
                )
                raise TypeError(msg)

            _default_incoming_mime_types.append(available_deserializer.content_type())

        # report on the acceptable mime types
        self._logger.info("generally accepts %s; speaks %s" % (
            str(_default_outgoing_mime_types).strip("[]'"),
            str(_default_incoming_mime_types).strip("[]'")
        ))

        # attempt to parse the HTTP request
        request = Request(
            environ=environ,
            charset=self._charset,
            logger=self._logger,
            deserializers=self._deserializers,
            default_deserializer=self._default_deserializer
        )

        # initialise the route map
        route_map = self.generate_route_map(self._routes)

        try:

            # check if the requested URL has a valid registered handler
            for regexp, handler_class in route_map:

                # if absent, can assume to be empty string
                # https://www.python.org/dev/peps/pep-3333/#environ-variables
                match = regexp.match(environ.get("PATH_INFO", ""))

                # if we've found a match; ensure its a handler subclass and return it's callable
                if match:

                    # assemble the args and kwargs
                    args = match.groups()
                    kwargs = {}
                    for key, value in iter(regexp.groupindex.items()):
                        kwargs[key] = args[value - 1]

                    if len(kwargs) > 0:
                        args = ()

                    if issubclass(handler_class, BlueprintHandler):

                        response = DictionaryResponse(
                            charset=self._charset, logger=self._logger,
                            serializers=self._serializers,
                            default_serializer=self._default_deserializer
                        )

                        request_handler = handler_class(
                            args=args,
                            kwargs=kwargs,
                            request=request,
                            response=response,
                            logger=self._logger,
                            debug=self._debug,
                            route_map=self._routes
                        )
                    else:
                        response = Response(
                            charset=self._charset,
                            logger=self._logger,
                            serializers=self._serializers,
                            default_serializer=self._default_deserializer
                        )
                        response.minify = request.is_minified

                        request_handler = handler_class(
                            args=args,
                            kwargs=kwargs,
                            request=request,
                            response=response,
                            logger=self._logger,
                            debug=self._debug
                        )

                    return request_handler(environ, start_response)

            # request does not have a matched handler
            no_endpoint = exception.NoEndpointError()
            no_endpoint.request = request
            raise no_endpoint

        except exception.Base as exp:
            self.logger.error(exp)
            error_response = ErrorResponse(exp, self._default_serializer)
            return error_response(environ, start_response)

    @classmethod
    def generate_route_map(cls, routes):

        parsed_handler_map = []

        for url, handler in routes:

            regexp = url

            # patch regular expression if it is incomplete
            if not regexp.startswith('^'):
                regexp = '^' + regexp
            if not regexp.endswith('$'):
                regexp += '$'

            compiled_regex = re.compile(regexp)

            arg_count = compiled_regex.groups
            kwarg_count = len(compiled_regex.groupindex.items())

            if arg_count != kwarg_count and kwarg_count > 0:
                raise ValueError("%s URL is invalid, cannot mix named and un-named groups" % url)
            else:
                parsed_handler_map.append((compiled_regex, handler))

        return parsed_handler_map
