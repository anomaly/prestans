import inspect

from prestans.http import STATUS
from prestans.rest import RequestHandler


class BlueprintHandler(RequestHandler):
    """
    Generates a blueprint of the handler and serializes it using the requested Accept header.
    """

    def __init__(self, args, request, response, logger, debug, route_map):

        super(BlueprintHandler, self).__init__(args, request, response, logger, debug)
        self._route_map = route_map

    def _create_blueprint(self):

        blueprint_groups = dict()

        # interrogate each handler
        for regexp, handler_class in self.route_map:

            # Ignore discovery handler
            if issubclass(handler_class, BlueprintHandler):
                continue

            handler_blueprint = dict()
            handler_blueprint['url'] = regexp
            handler_blueprint['handler_class'] = handler_class.__name__
            handler_blueprint['description'] = inspect.getdoc(handler_class)
            handler_blueprint['supported_methods'] = handler_class(
                self._args,
                self.request,
                self.response,
                self.logger,
                self.debug
            ).blueprint()

            # Make a new group per module if one doesnt' exist
            if handler_class.__module__ not in blueprint_groups:
                blueprint_groups[handler_class.__module__] = []

            blueprint_groups[handler_class.__module__].append(handler_blueprint)

        return blueprint_groups

    @property
    def route_map(self):
        return self._route_map

    @route_map.setter
    def route_map(self, value):
        self._route_map = value

    def __call__(self, environ, start_response):

        # setup serializers
        self._setup_serializers()

        self.response.status = STATUS.OK

        self.response.body = self._create_blueprint()

        return self.response(environ, start_response)
