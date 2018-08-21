from prestans.types import BinaryResponse
from prestans.types import DataCollection


class VerbConfig(object):
    """
    VerbConfig sets out rules for each HTTP Verb that your API will make available.
    These rules are used by prestans to validate requests and responses before
    handing over execution control to your handler.

    All verbs in use must provide at least a response_template which should be a
    subclass of prestans.types.DataCollection.
    """

    def __init__(self, response_template=None, response_attribute_filter_default_value=False,
                 parameter_sets=None, body_template=None, request_attribute_filter=None):

        """
        Each handler has a meta attribute called __verb_config__ this must be an instance
        of prestans.parser.Config which accepts six named parameters one for each supported
        HTTP verb (HEAD, GET, POST, PUT, DELETE, PATCH) each one of which must be an
        instance of prestans.parser.VerbConfig. A VerbConfig accepts the following named
        parameters (not all of them are supported across all HTTP verbs):

        * response_template an instance of a prestans.types.DataCollection subclass
          i.e a Model or an Array of Prestans DataType. This is what Prestans will use
          to validate the response your handler sends back to the client.
        * response_attribute_filter_default_value Prestans automatically creates an
          attribute filter based on the response_template by default Prestans exposes
          all it's attributes in the response, setting this to False will hide all
          attributes be default. Your handler code is responsible for toggling
          visibility in either instance.
        * parameter_sets an array of prestans.parser.ParameterSet instances
        * body_template an instance of a prestans.types.DataCollection subclass i.e
          a Model or an Array of Prestans DataType, this is what Prestans will use
          to validate the request sent to your handler. If validation of the incoming
          data fails, Prestans will not execute the associated verb in your handler.
        * request_attribute_filter is an attribute filter used to relax or tighten
          rules for the incoming data. This is particularly useful if you want
          to use portions of a model. Particularly useful for UPDATE requests.
        """
        from prestans.parser import AttributeFilter
        from prestans.parser import ParameterSet

        self._response_attribute_filter_template = None

        # response_template; required parameter
        if response_template is not None and \
                (not isinstance(response_template, DataCollection) and not isinstance(response_template, BinaryResponse)):
            raise TypeError("response_template of type %s must be an instance of \
                a prestans.types.DataCollection subclass" % response_template.__class__.__name__)

        if response_template is not None and isinstance(response_template, DataCollection):
            self.response_attribute_filter_template = AttributeFilter.from_model(
                model_instance=response_template,
                default_value=response_attribute_filter_default_value
            )
        else:
            self.response_attribute_filter_template = None

        self._response_template = response_template

        # turn parameter_sets single object into a list
        if parameter_sets is not None and not isinstance(parameter_sets, list):
            parameter_sets = [parameter_sets]

        # check that all parameter sets are of valid type
        if isinstance(parameter_sets, list):
            for parameter_set in parameter_sets:
                if not isinstance(parameter_set, ParameterSet):
                    raise TypeError("parameter_set of type %s must be an instance of \
                    prestans.parser.ParameterSet" % parameter_set.__class__.__name__)

            self._parameter_sets = parameter_sets
        else:
            self._parameter_sets = list()

        # body_template
        if body_template is not None and not \
                isinstance(body_template, DataCollection):
            raise TypeError(
                "body_template of type %s must be an instance of \
                a prestans.types.DataCollection subclass" % body_template.__class__.__name__)

        self._body_template = body_template

        # request_attribute_filter
        if request_attribute_filter is not None and \
           not isinstance(request_attribute_filter, AttributeFilter):
            raise TypeError("request_attribute_filter of type %s must an instance \
            of prestans.parser.AttributeFilter" % request_attribute_filter.__class__.__name__)

        self._request_attribute_filter = request_attribute_filter

    def blueprint(self):

        verb_config_blueprint = dict()

        if self._response_template is not None:
            verb_config_blueprint['response_template'] = self._response_template.blueprint()
        else:
            verb_config_blueprint['response_template'] = self._response_template

        verb_config_blueprint['parameter_sets'] = []
        for parameter_set in self._parameter_sets:
            if parameter_set is not None:
                verb_config_blueprint['parameter_sets'].append(parameter_set.blueprint())

        if self._body_template is not None:
            verb_config_blueprint['body_template'] = self._body_template.blueprint()
        else:
            verb_config_blueprint['body_template'] = self._body_template

        if self._request_attribute_filter is not None:
            verb_config_blueprint['request_attribute_filter'] = self._request_attribute_filter.blueprint()
        else:
            verb_config_blueprint['request_attribute_filter'] = self._request_attribute_filter

        return verb_config_blueprint

    @property
    def response_template(self):
        return self._response_template

    @property
    def response_attribute_filter_template(self):
        return self._response_attribute_filter_template

    @response_attribute_filter_template.setter
    def response_attribute_filter_template(self, value):
        self._response_attribute_filter_template = value

    @property
    def parameter_sets(self):
        return self._parameter_sets

    @property
    def body_template(self):
        return self._body_template

    @property
    def request_attribute_filter(self):
        return self._request_attribute_filter
