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

"""
Parser
"""

__all__ = ['Config', 'VerbConfig', 'AttributeFilter', 'ParameterSet']

import inspect

import prestans.types
import prestans.http
import prestans.exception

class ParameterSet(object):
    """
    ParameterSet is a group of Dataprestans.types that are expected as GET parameters

    ParameterSet defines rules and patterns in which they are acceptable.
    while ParserRuleSet is responsible for running the parse mechanism.
    """

    def blueprint(self):
        """
        blueprint support, returns a partial dictionary
        """

        blueprint = dict()
        blueprint['type'] = "%s.%s" % (self.__module__, self.__class__.__name__)

        # Fields
        fields = dict()

        # Inspects the attributes of a parameter set and tries to validate the input
        for attribute_name, type_instance in self.__class__.__dict__.iteritems():

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            # Must be one of the following types
            if not isinstance(type_instance, prestans.types.String) and \
            not isinstance(type_instance, prestans.types.Float) and \
            not isinstance(type_instance, prestans.types.Integer) and \
            not isinstance(type_instance, prestans.types.Date) and \
            not isinstance(type_instance, prestans.types.DateTime) and \
            not isinstance(type_instance, prestans.types.Array):
                raise TypeError("%s should be subclass of\
                 prestans.types.String/Integer/Float/Date/DateTime/Array" % attribute_name)

            if isinstance(type_instance, prestans.types.Array):
                if not isinstance(type_instance.element_template, prestans.types.String) and \
                not isinstance(type_instance.element_template, prestans.types.Float) and \
                not isinstance(type_instance.element_template, prestans.types.Integer):
                    raise TypeError("%s should be subclass of \
                        prestans.types.String/Integer/Float/Array" % attribute_name)

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint

    def validate(self, request):
        """
        validate method for %ParameterSet

        Since the introduction of ResponseFieldListParser, the parameter _response_field_list
        will be ignore, this is a prestans reserved parameter, and cannot be used by apps.

        @param self The object pointer
        @param request The request object to be validated
        """

        validated_parameter_set = self.__class__()

        # Inspects the attributes of a parameter set and tries to validate the input
        for attribute_name, type_instance in self.__class__.__dict__.iteritems():

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            #: Must be one of the following types
            if not isinstance(type_instance, prestans.types.String) and \
            not isinstance(type_instance, prestans.types.Float) and \
            not isinstance(type_instance, prestans.types.Integer) and \
            not isinstance(type_instance, prestans.types.Date) and \
            not isinstance(type_instance, prestans.types.DateTime) and \
            not isinstance(type_instance, prestans.types.Array):
                raise TypeError("%s should be of type \
                    prestans.types.String/Integer/Float/Date/DateTime/Array" % attribute_name)

            if issubclass(type_instance.__class__, prestans.types.Array):

                if not isinstance(type_instance.element_template, prestans.types.String) and \
                not isinstance(type_instance.element_template, prestans.types.Float) and \
                not isinstance(type_instance.element_template, prestans.types.Integer):
                    raise TypeError("%s elements should be of \
                        type prestans.types.String/Integer/Float" % attribute_name)

            try:

                #: Get input from parameters
                #: Empty list returned if key is missing for getall
                if issubclass(type_instance.__class__, prestans.types.Array):
                    validation_input = request.params.getall(attribute_name)
                #: Key error thrown if key is missing for getone
                else:
                    try:
                        validation_input = request.params.getone(attribute_name)
                    except KeyError:
                        validation_input = None

                #: Validate input based on data type rules,
                #: raises DataTypeValidationException if validation fails
                validation_result = type_instance.validate(validation_input)

                setattr(validated_parameter_set, attribute_name, validation_result)

            except prestans.exception.DataValidationException, exp:
                raise prestans.exception.ValidationError(
                    message=str(exp),
                    attribute_name=attribute_name,
                    value=validation_input,
                    blueprint=type_instance.blueprint())

        return validated_parameter_set


class AttributeFilter(object):
    """
      {
        field_name0: true,
        field_name1: false,
        collection_name0: true,
        collection_name1: false,
        collection_name2: {
            sub_field_name0: true,
            sub_field_name1: false
        }
      }
    """

    @classmethod
    def from_model(cls, model_instance, default_value=False, **kwargs):
        """
        wrapper for Model's get_attribute_filter
        """

        if not isinstance(model_instance, prestans.types.DataCollection):
            raise TypeError("model_instance must be a sublcass of \
                prestans.types.DataCollection, %s given" % (model_instance.__class__.__name__))
        elif isinstance(model_instance, prestans.types.Array) and model_instance.is_scalar:
            return AttributeFilter(is_array_scalar=True)
        attribute_filter_instance = model_instance.get_attribute_filter(default_value)

        #: kwargs support
        for name, value in kwargs.iteritems():
            if attribute_filter_instance.__dict__.has_key(name):
                setattr(attribute_filter_instance, name, value)
            else:
                raise KeyError(name)

        return attribute_filter_instance

    def __init__(self, from_dictionary=None, template_model=None, is_array_scalar=False, **kwargs):
        """
        Creates an attribute filter object, optionally populates from a
        dictionary of booleans
        """

        if from_dictionary:
            self._init_from_dictionary(from_dictionary, template_model)

        #: kwargs support
        for name, value in kwargs.iteritems():
            if self.__dict__.has_key(name):
                setattr(self, name, value)
            else:
                raise KeyError(name)


    def conforms_to_template_filter(self, template_filter):
        """
        Check AttributeFilter conforms to the rules set by the template

         - If self, has attributes that template_fitler does not contain, throw Exception
         - If sub list found, perform the first check
         - If self has a value for an attribute, assign to final AttributeFilter
         - If not found, assign value from template
        """

        if not isinstance(template_filter, self.__class__):
            raise TypeError("AttributeFilter can only check conformance against \
                another template filter, %s provided" % (template_filter.__class__.__name__))

        #:
        #: Keys from the template
        #:
        template_filter_keys = template_filter.keys()
        # Keys from the object itself
        this_filter_keys = self.keys()

        #:
        #: 1. Check to see if the client has provided unwanted keys
        #:
        unwanted_keys = set(this_filter_keys) - set(template_filter_keys)
        if len(unwanted_keys) > 0:
            raise prestans.exception.AttributeFilterDiffers(list(unwanted_keys))

        #:
        #: 2. Make a attribute_filter that we send back
        #:
        evaluated_attribute_filter = AttributeFilter()

        #:
        #: 3. Evaluate the differences between the two, with template_filter as the standard
        #:
        for template_key in template_filter_keys:

            if template_key in this_filter_keys:

                value = getattr(self, template_key)

                #:
                #: If sub filter and boolean provided with of true, create default filter
                #: with value of true
                #:
                if isinstance(value, bool) and \
                value is True and \
                isinstance(getattr(template_filter, template_key), AttributeFilter):
                    setattr(evaluated_attribute_filter, template_key, \
                        getattr(template_filter, template_key))
                elif isinstance(value, bool):
                    setattr(evaluated_attribute_filter, template_key, value)
                elif isinstance(value, self.__class__):
                    # Attribute lists sort themselves out, to produce sub Attribute Filters
                    template_sub_list = getattr(template_filter, template_key)
                    this_sub_list = getattr(self, template_key)
                    setattr(evaluated_attribute_filter, template_key, \
                        this_sub_list.conforms_to_template_filter(template_sub_list))
            else:
                setattr(evaluated_attribute_filter, template_key, \
                    getattr(template_filter, template_key))

        return evaluated_attribute_filter

    def keys(self):
        """
        returns a list of usable keys
        """

        keys = list()

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            keys.append(attribute_name)

        return keys

    def has_key(self, key):
        """
        contains a particular key, wrapper on self.__dict__.key
        """
        return self.__dict__.has_key(key)

    def is_filter_at_key(self, key):
        """
        return True if attribute is a subfilter
        """

        if self.has_key(key):
            attribute_status = getattr(self, key)
            if isinstance(attribute_status, self.__class__):
                return True

        return False

    def is_attribute_visible(self, key):
        """
        returns True if an attribute is visible
        If attribute is an instance of AttributeFilter, it returns True if all attributes
        of the sub filter are visible.
        """
        if self.has_key(key):
            attribute_status = getattr(self, key)
            if isinstance(attribute_status, bool) and attribute_status == True:
                return True
            elif isinstance(attribute_status, self.__class__) and \
            attribute_status.are_any_attributes_visible():
                return True

        return False

    def are_any_attributes_visible(self):
        """
        checks to see if any attributes are set to true
        """

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, bool) and type_instance == True:
                return True
            elif isinstance(type_instance, self.__class__) and \
            type_instance.are_all_attributes_visible() == True:
                return True

        return False

    def are_all_attributes_visible(self):
        """
        checks to see if all attributes are set to true
        """

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            if isinstance(type_instance, bool) and type_instance == False:
                return False
            elif isinstance(type_instance, self.__class__) and \
            type_instance.are_all_attributes_visible() == False:
                return False

        return True

    def set_all_attribute_values(self, value):
        """
        sets all the attribute values to the value and propagate to any children
        """

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            if isinstance(type_instance, bool):
                self.__dict__[attribute_name] = value
            elif isinstance(type_instance, self.__class__):
                type_instance.set_all_attribute_values(value)


    def as_dict(self):
        """
        turns attribute filter object into python dictionary
        """

        output_dictionary = dict()

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, bool):
                output_dictionary[attribute_name] = type_instance
            elif isinstance(type_instance, self.__class__):
                output_dictionary[attribute_name] = type_instance.as_dict()

        return output_dictionary


    def _init_from_dictionary(self, from_dictionary, template_model=None):
        """
        Private helper to init values from a dictionary, wraps chidlren into
        AttributeFilter objects
        """

        if not isinstance(from_dictionary, dict):
            raise TypeError("from_dictionary must be of type dict, %s \
                provided" % from_dictionary.__class__.__name__)
        rewrite_map = None
        if template_model is not None:

            rewrite_map = template_model.attribute_rewrite_reverse_map()

            if not isinstance(template_model, prestans.types.DataCollection):
                raise TypeError("template_model should be a prestans model in AttributeFilter \
                    init (from dictionary), %s provided" % template_model.__class__.__name__)

        for key, value in from_dictionary.iteritems():

            target_key = key

            #:
            #: Minification support
            #:
            if rewrite_map is not None:
                target_key = rewrite_map[key]

            #:
            #: Check to see we can work with the value
            #:
            if not isinstance(value, (bool, dict)):
                raise TypeError("AttributeFilter input for key %s must be \
                    boolean or dict, %s provided" % (key, value.__class__.__name__))

            #:
            #: Ensure that the key exists in the template model
            #:
            if template_model is not None and not template_model.has_key(target_key):

                unwanted_keys = list()
                unwanted_keys.append(target_key)
                raise prestans.exception.AttributeFilterDiffers(unwanted_keys)

            #:
            #: Either keep the value of wrap it up with AttributeFilter
            #:
            if isinstance(value, bool):
                setattr(self, target_key, value)
            elif isinstance(value, dict):

                sub_map = None
                if template_model is not None:

                    sub_map = getattr(template_model, target_key)

                    #: prestans Array support
                    if isinstance(sub_map, prestans.types.Array):
                        sub_map = sub_map.element_template

                setattr(self, target_key, \
                    AttributeFilter(from_dictionary=value, template_model=sub_map))

    def __setattr__(self, key, value):
        """
        Overrides setattr to allow only booleans or an AttributeFilter
        """

        # Set internal fields
        if key[0:1] == "_":
            self.__dict__[key] = value
            return

        # Values should either be boolean or type of self
        if isinstance(value, bool) and key in self.__dict__ and \
        isinstance(self.__dict__[key], self.__class__):
            self.__dict__[key].set_all_attribute_values(value)
            return
        elif isinstance(value, (bool, self.__class__)):
            self.__dict__[key] = value
            return

        raise TypeError("%s name in %s must be of type Boolean or AttributeFilter, given %s" %
                        (key, self.__class__.__name__, value.__class__.__name__))


class VerbConfig(object):
    """
    VerbConfig sets out rules for each HTTP Verb that your API will make available.
    These rules are used by prestans to validate requests and responses before
    handing over execution control to your handler.

    All verbs in use must provide atleast a response_template which should be a
    subclass of prestans.types.DataCollection.
    """

    def __init__(self, response_template=None, response_attribute_filter_default_value=False,\
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

        self._response_attribute_filter_template = None

        #: response_template; required parameter
        if response_template is not None and \
        (not isinstance(response_template, prestans.types.DataCollection) and\
         not isinstance(response_template, prestans.types.BinaryResponse)):
            raise TypeError("response_template of type %s must be an instance of \
                a prestans.types.DataCollection subclass" % response_template.__class__.__name__)

        if response_template is not None and \
        isinstance(response_template, prestans.types.DataCollection):
            self.response_attribute_filter_template = AttributeFilter.\
            from_model(model_instance=response_template,\
                default_value=response_attribute_filter_default_value)
        else:
            self.response_attribute_filter_template = None

        self._response_template = response_template

        #: parameter_sets turn a single object into a list
        if isinstance(parameter_sets, ParameterSet):
            parameter_sets = [parameter_sets]

        if isinstance(parameter_sets, list):
            for parameter_set in parameter_sets:
                if not isinstance(parameter_set, ParameterSet):
                    raise TypeError("parameter_set of type %s must be an instance of \
                    prestans.parser.ParameterSet" % parameter_set.__class__.__name__)

            self._parameter_sets = parameter_sets
        else:
            self._parameter_sets = list()

        #: body_template
        if body_template is not None and not \
        isinstance(body_template, prestans.types.DataCollection):
            raise TypeError(
                "body_template of type %s must be an instance of \
                a prestans.types.DataCollection subclass" % body_template.__class__.__name__)

        self._body_template = body_template

        #: request_attribute_filter
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
            verb_config_blueprint['request_attribute_filter'] = \
            self._request_attribute_filter.blueprint()
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

class Config(object):
    """
    Configuration that's attached to each handler to define rules for each
    HTTP Verb. All HTTP verbs in use must have a configuration defined.

    __init__ takes in a VerbConfig instance for each parameter with names
    adjacent to the HTTP verb.
    """

    def __init__(self, GET=None, HEAD=None, POST=None, PUT=None, PATCH=None, DELETE=None):

        for verb in [GET, HEAD, POST, PUT, PATCH, DELETE]:
            if verb is not None and not isinstance(verb, VerbConfig):
                raise TypeError("All Parser configs should be of type prestans.parser.VerbConfig")

        self._configs = dict()

        self._configs[prestans.http.VERB.GET] = GET
        self._configs[prestans.http.VERB.HEAD] = HEAD
        self._configs[prestans.http.VERB.POST] = POST
        self._configs[prestans.http.VERB.PUT] = PUT
        self._configs[prestans.http.VERB.PATCH] = PATCH
        self._configs[prestans.http.VERB.DELETE] = DELETE

    def get_config_for_verb(self, verb):
        return self._configs[verb]

    @property
    def get(self):
        return self._configs[prestans.http.VERB.GET]

    @property
    def head(self):
        return self._configs[prestans.http.VERB.HEAD]

    @property
    def post(self):
        return self._configs[prestans.http.VERB.POST]

    @property
    def put(self):
        return self._configs[prestans.http.VERB.PUT]

    @property
    def patch(self):
        return self._configs[prestans.http.VERB.PATCH]

    @property
    def delete(self):
        return self._configs[prestans.http.VERB.DELETE]
