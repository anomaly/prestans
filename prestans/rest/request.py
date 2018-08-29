import webob

from prestans import deserializer
from prestans import exception
from prestans.http import VERB
from prestans.parser import AttributeFilter
from prestans.types import DataCollection


class Request(webob.Request):
    """
    Request is parsed REST Request; it's inherits and relies on Webob.Request to
    do the heavy lifting of parsing HTTP requests. It adds on top parsing of
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
            msg = "access to request.parsed_body is not allowed when body_template is set to None"
            raise AttributeError(msg)

        self.parse_body()

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

    def set_deserializer_by_mime_type(self, mime_type):
        """
        :param mime_type:
        :return:

        Used by content_type_set to set get a reference to the serializer object
        """

        for deserializer in self._deserializers:
            if deserializer.content_type() == mime_type:
                self._selected_deserializer = deserializer
                return

        raise exception.UnsupportedContentTypeError(mime_type, self.supported_mime_types_str)

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
        Mutator for parameter_set
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

        if self.method == VERB.GET:
            raise AssertionError("body_template cannot be set for GET requests")

        if value is None:
            self.logger.warn("body_template is None, parsing will be ignored")
            return

        if not isinstance(value, DataCollection):
            msg = "body_template must be an instance of %s.%s" % (
                DataCollection.__module__,
                DataCollection.__name__
            )
            raise AssertionError(msg)

        self._body_template = value

        # get a deserializer based on the Content-Type header
        # do this here so the handler gets a chance to setup extra serializers
        self.set_deserializer_by_mime_type(self.content_type)

    def parse_body(self):

        if self._parsed_body is None and self._body_template is not None:
            # parse the body using the deserializer
            unserialized_body = self.selected_deserializer.loads(self.body)

            # valiate the body using the template and attribute_filter
            self._parsed_body = self._body_template.validate(unserialized_body, self.attribute_filter, self.is_minified)

    def register_deserializers(self, deserializers):

        if not isinstance(deserializers, list):
            deserializers = [deserializers]

        # todo: should this prevent duplicates for same mime-type?

        for new_deserializer in deserializers:

            if not isinstance(new_deserializer, deserializer.Base):
                msg = "registered deserializer %s does not inherit from prestans.serializer.DeSerializer" % (
                      new_deserializer.__class__.__name__
                )
                raise TypeError(msg)

        self._deserializers = self._deserializers + deserializers

    def get_response_attribute_filter(self, template_filter, template_model=None):
        """
        Prestans-Response-Attribute-List can contain a client's requested
        definition for attributes required in the response. This should match
        the response_attribute_filter_template?

        :param template_filter:
        :param template_model: the expected model that this filter corresponds to
        :return:
        :rtype: None | AttributeFilter
        """

        if template_filter is None:
            return None

        if 'Prestans-Response-Attribute-List' not in self.headers:
            return None

        # header not set results in a None
        attribute_list_str = self.headers['Prestans-Response-Attribute-List']

        # deserialize the header contents
        json_deserializer = deserializer.JSON()
        attribute_list_dictionary = json_deserializer.loads(attribute_list_str)

        # construct an AttributeFilter
        attribute_filter = AttributeFilter(
            from_dictionary=attribute_list_dictionary,
            template_model=template_model
        )

        #: Check template? Do this even through we might have template_model
        #: in case users have made a custom filter
        evaluated_filter = attribute_filter.conforms_to_template_filter(template_filter)

        return evaluated_filter

    @property
    def is_minified(self):
        """
        :return:
        :rtype: bool
        """

        if 'Prestans-Minification' not in self.headers:
            return False

        return self.headers['Prestans-Minification'].upper() == "ON"
