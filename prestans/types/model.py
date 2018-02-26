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
import copy
import inspect
import string

from prestans import exception
# from prestans.parser import AttributeFilter
from prestans.types import DataCollection
from prestans.types import DataStructure
from prestans.types import DataType


class Model(DataCollection):

    def __init__(self, required=True, default=None, description=None, **kwargs):
        """
        If you are using the Model constructor to provide Meta data, you can provide it
        a default dictionary to initialise instance to initialise it from

        Can run _create_instance_attributes to copy attribute templates to the instance,
        Model instances do not have any configurable options.

        @param required whether or not this model is required when used as an attribute
        @param default provides a default value for your type, used if one is not provided
        @param kwargs Named parameters of which to instantiate the model with
        """

        self._required = required
        self._description = description

        self._create_instance_attributes(kwargs)

    def getmembers(self):
        """
        :return: list of members as name, type tuples
        :rtype: list
        """
        return filter(
            lambda m: not m[0].startswith("__") and not inspect.isfunction(m[1]) and not inspect.ismethod(m[1]),
            inspect.getmembers(self.__class__)
        )

    def attribute_count(self):

        attribute_count = 0

        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataType):
                attribute_count += 1

        return attribute_count

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'model'
        blueprint['description'] = inspect.getdoc(self.__class__)

        constraints = dict()
        constraints['required'] = self._required
        constraints['model_template'] = self.__class__.__name__
        constraints['description'] = self._description

        blueprint['constraints'] = constraints

        fields = dict()
        for attribute_name, type_instance in self.getmembers():

            if not isinstance(type_instance, DataType):
                raise TypeError("%s must be of a DataType subclass" % attribute_name)

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint

    def __setattr__(self, key, value):

        if key[0:1] == "_":
            self.__dict__[key] = value
            return

        validator = None
        for attribute_name, type_instance in self.getmembers():
            if attribute_name == key:
                validator = type_instance

        if validator is not None:

            try:
                if validator.__class__ == value.__class__:
                    self.__dict__[key] = value
                else:
                    self.__dict__[key] = validator.validate(value)

            except exception.DataValidationException as exp:
                raise exception.ValidationError(
                    message=str(exp),
                    attribute_name=key,
                    value=value,
                    blueprint=validator.blueprint()
                )
            return

        raise KeyError("No key named: %s in instance of type: %s" % (key, self.__class__.__name__))

    def _create_instance_attributes(self, arguments):
        """
        Copies class level attribute templates and makes instance placeholders

        This step is required for direct uses of Model classes. This creates a
        copy of attribute_names ignores methods and private variables.
        DataCollection types are deep copied to ignore memory reference conflicts.

        DataType instances are initialized to None or default value.
        """

        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataCollection):
                self.__dict__[attribute_name] = copy.deepcopy(type_instance)
                continue

            if type_instance is None:
                self.__dict__[attribute_name] = None
                continue

            if isinstance(type_instance, DataType):

                try:
                    value = None

                    if attribute_name in arguments:
                        value = arguments[attribute_name]

                    self.__dict__[attribute_name] = type_instance.validate(value)

                except exception.DataValidationException as exp:
                    self.__dict__[attribute_name] = None

    def get_attribute_keys(self):
        """
        Returns a list of managed attributes for the Model class

        Implemented for use with data adapters, can be used to quickly make a list of the
        attribute names in a prestans model
        """

        _attribute_keys = list()

        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataType):
                _attribute_keys.append(attribute_name)

        return _attribute_keys

    def get_attribute_filter(self, default_value=False):
        from prestans.parser import AttributeFilter

        attribute_filter = AttributeFilter()

        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataCollection):
                setattr(attribute_filter, attribute_name, type_instance.get_attribute_filter(default_value))
            else:
                setattr(attribute_filter, attribute_name, default_value)

        return attribute_filter

    def validate(self, value, attribute_filter=None, minified=False):
        """
        :param value: serializable input to validate
        :type value: dict | None
        :param attribute_filter:
        :type: prestans.parser.AttributeFilter | None
        :param minified: whether or not the input is minified
        :type minified: bool
        :return: the validated model
        :rtype: Model
        """

        if self._required and (value is None or not isinstance(value, dict)):
            """
            Model level validation requires a parsed dictionary
            this is done by the serializer
            """
            raise exception.RequiredAttributeError()

        if not self._required and not value:
            """
            Value was not provided by caller, but require a template
            """
            return None

        _model_instance = self.__class__()

        rewrite_map = self.attribute_rewrite_map()

        for attribute_name, type_instance in self.getmembers():

            if attribute_filter and not attribute_filter.is_attribute_visible(attribute_name):
                _model_instance.__dict__[attribute_name] = None

                continue

            if not isinstance(type_instance, DataType):
                raise TypeError("%s must be a DataType subclass" % attribute_name)

            validation_input = None

            input_value_key = attribute_name

            # minification support
            if minified is True:
                input_value_key = rewrite_map[attribute_name]

            if input_value_key in value:
                validation_input = value[input_value_key]

            try:

                if isinstance(type_instance, DataCollection):
                    sub_attribute_filter = None
                    if attribute_filter and attribute_name in attribute_filter:
                        sub_attribute_filter = getattr(attribute_filter, attribute_name)

                    validated_object = type_instance.validate(
                        validation_input,
                        sub_attribute_filter,
                        minified
                    )
                else:
                    validated_object = type_instance.validate(validation_input)

                _model_instance.__dict__[attribute_name] = validated_object

            except exception.DataValidationException as exp:
                raise exception.ValidationError(
                    message=str(exp),
                    attribute_name=attribute_name,
                    value=validation_input,
                    blueprint=type_instance.blueprint()
                )

        return _model_instance

    def attribute_rewrite_map(self):
        """
        Example: long_name -> a_b

        :return: the rewrite map
        :rtype: dict
        """

        rewrite_map = dict()
        token_rewrite_map = self.generate_attribute_token_rewrite_map()

        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataType):
                attribute_tokens = attribute_name.split('_')

                rewritten_attribute_name = ''
                for token in attribute_tokens:
                    rewritten_attribute_name += token_rewrite_map[token] + "_"
                # remove the trailing underscore
                rewritten_attribute_name = rewritten_attribute_name[:-1]

                rewrite_map[attribute_name] = rewritten_attribute_name

        return rewrite_map

    def attribute_rewrite_reverse_map(self):
        """
        Example: a_b -> long_name

        :return: the reverse rewrite map
        :rtype: dict
        """

        rewrite_map = dict()

        token_rewrite_map = self.generate_attribute_token_rewrite_map()

        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataType):

                attribute_tokens = attribute_name.split('_')
                rewritten_attribute_name = ''
                for token in attribute_tokens:
                    rewritten_attribute_name += token_rewrite_map[token] + "_"
                # remove the trailing underscore
                rewritten_attribute_name = rewritten_attribute_name[:-1]

                rewrite_map[rewritten_attribute_name] = attribute_name

        return rewrite_map

    def __contains__(self, attribute_name):

        has_key = attribute_name in self.__class__.__dict__

        if not has_key:

            base_classes = list()
            base_classes += list(self.__class__.__bases__)

            while not has_key and base_classes:

                # take a base class from the list
                base_class = base_classes.pop()

                # we found it clear the list
                if attribute_name in base_class.__dict__:
                    has_key = True
                    base_classes = list()
                # add any more base classes from this class
                else:
                    base_classes += list(base_class.__bases__)

        return has_key

    def generate_attribute_token_rewrite_map(self):

        rewrite_tokens = self.generate_attribute_tokens()
        minified_tokens = self.generate_minified_keys(len(rewrite_tokens))

        return dict(zip(rewrite_tokens, minified_tokens))

    def generate_attribute_tokens(self):

        rewrite_tokens = list()

        # create a list of tokens
        for attribute_name, type_instance in self.getmembers():

            if isinstance(type_instance, DataType):
                rewrite_tokens = rewrite_tokens + attribute_name.split('_')

        # remove duplicated; sort alphabetically for the algorithm to work
        rewrite_tokens = list(set(rewrite_tokens))
        rewrite_tokens.sort()

        return rewrite_tokens

    @classmethod
    def generate_minified_keys(cls, length=26, prefix=''):

        minified_keys = list()

        overflow = 0
        if length > 26:
            overflow = length - 26
            length = 26

        for index in range(0, length):

            generated_char = cls.generate_attribute_key(index)
            minified_keys.append(prefix + generated_char)

            if overflow > 0:

                sublist_length = overflow
                if sublist_length > 26:
                    sublist_length = 26

                sublist = cls.generate_minified_keys(sublist_length, generated_char)
                minified_keys = minified_keys + sublist
                overflow = overflow - len(sublist)

        if prefix == '':
            minified_keys.sort(key=len, reverse=False)

        return minified_keys

    @classmethod
    def generate_attribute_key(cls, val):
        """
        :param val:
        :type val: int
        :return:
        :rtype: str
        """
        return string.ascii_lowercase[val % 26] * (val // 26 + 1)

    def as_serializable(self, attribute_filter=None, minified=False):
        """
        Returns a dictionary with attributes and pure python representation of
        the data instances. If an attribute filter is provided as_serializable
        will respect the visibility.

        The response is used by serializers to return data to client

        :param attribute_filter:
        :type attribute_filter: prestans.parser.AttributeFilter
        :param minified:
        :type minified: bool
        """
        from prestans.parser import AttributeFilter

        model_dictionary = dict()

        rewrite_map = self.attribute_rewrite_map()

        for attribute_name, type_instance in self.getmembers():

            serialized_attribute_name = attribute_name

            if isinstance(attribute_filter, AttributeFilter) and \
               not attribute_filter.is_attribute_visible(attribute_name):
                continue

            # support minification
            if minified is True:
                serialized_attribute_name = rewrite_map[attribute_name]

            if attribute_name not in self.__dict__ or self.__dict__[attribute_name] is None:
                model_dictionary[serialized_attribute_name] = None
                continue

            if isinstance(type_instance, DataCollection):

                sub_attribute_filter = None
                if isinstance(attribute_filter, AttributeFilter) and attribute_name in attribute_filter:
                    sub_attribute_filter = getattr(attribute_filter, attribute_name)

                model_dictionary[serialized_attribute_name] = self.__dict__[attribute_name]. \
                    as_serializable(sub_attribute_filter, minified)

            elif isinstance(type_instance, DataStructure):
                python_value = self.__dict__[attribute_name]
                serializable_value = type_instance.as_serializable(python_value)
                model_dictionary[serialized_attribute_name] = serializable_value

            elif isinstance(type_instance, DataType):
                model_dictionary[serialized_attribute_name] = self.__dict__[attribute_name]

        return model_dictionary
