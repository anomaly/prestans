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
from prestans import exception

from prestans.types import ElementTemplate

from prestans.types import DataCollection
from prestans.types import DataStructure
from prestans.types import DataType

from prestans.types import Boolean
from prestans.types import Float
from prestans.types import Integer
from prestans.types import String

from prestans.types import Date
from prestans.types import DateTime
from prestans.types import Time

import inspect


class Array(DataCollection):

    def __init__(self, required=True, element_template=None,
                 min_length=None, max_length=None, description=None):
        """
        :param required:
        :type required: bool
        :param element_template:
        :param min_length:
        :type min_length: int
        :param max_length:
        :type max_length: int
        :param description:
        :type description: str
        """
        if not isinstance(element_template, ElementTemplate):
            raise TypeError("element_template must be an instance of %s" % ElementTemplate.__name__)

        self._required = required
        self._min_length = min_length
        self._max_length = max_length
        self._description = description
        self._element_template = element_template  # type: ElementTemplate

        self._array_elements = list()

    def __len__(self):
        return len(self._array_elements)

    def __iter__(self):
        """"
        With a little help from:
        http://johnmc.co/llum/the-easiest-way-to-implement-__iter__-for-a-python-object
        """
        for element in self._array_elements:
            yield element

    def __getitem__(self, index):
        return self._array_elements[index]

    def __contains__(self, item):
        return item in self._array_elements

    @property
    def max_length(self):
        """
        :return:
        :rtype: int or None
        """
        return self._max_length

    @property
    def min_length(self):
        """
        :return:
        :rtype: int or None
        """
        return self._min_length

    @property
    def description(self):
        return self._description

    @property
    def is_scalar(self):
        """
        :return:
        :rtype: bool
        """
        return self.element_template.is_scalar

    @property
    def element_template(self):
        return self._element_template

    @element_template.setter
    def element_template(self, value):
        self._element_template = value

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'array'

        constraints = dict()
        constraints['required'] = self._required
        constraints['min_length'] = self._min_length
        constraints['max_length'] = self._max_length
        constraints['element_template'] = self.element_template.blueprint
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def remove(self, value):
        self._array_elements.remove(value)

    def validate(self, value, attribute_filter=None, minified=False):
        """
        :param value:
        :type value: list | None
        :param attribute_filter:
        :type attribute_filter: prestans.parser.AttributeFilter
        :param minified:
        :type minified: bool
        :return:
        """

        if not self._required and not value:
            return None

        _validated_array = self.__class__(
            element_template=self.element_template,
            min_length=self._min_length,
            max_length=self._max_length
        )

        if not isinstance(value, (list, tuple)):
            raise TypeError(value)

        for array_element in value:
            validated_array_element = self.element_template.validate(array_element, attribute_filter, minified)
            _validated_array.append(validated_array_element)

        if self._min_length is not None and len(_validated_array) < self._min_length:
            raise exception.LessThanMinimumError(value, self._min_length)

        if self._max_length is not None and len(_validated_array) > self._max_length:
            raise exception.MoreThanMaximumError(value, self._max_length)

        return _validated_array

    def append(self, value):

        if isinstance(value, (list, tuple)):

            for element in value:
                self.append(element)
            return

        # scalar or data structure types should be validated before appending
        # for example a data represented by a string needs to be turned into a datetime.date
        if self.element_template.is_scalar or self.element_template.is_data_structure:
            value = self.element_template.validate(value)
        elif not isinstance(value, self.element_template.class_ref):
            msg = "prestans array elements must be of type %s; given %s" % (
                self.element_template.class_ref.__name__,
                value.__class__.__name__
            )
            raise TypeError(msg)

        self._array_elements.append(value)

    def as_serializable(self, attribute_filter=None, minified=False):
        """
        :param attribute_filter:
        :param minified:
        :type minified: bool
        :return:
        :rtype: list
        """

        _result_array = list()

        for array_element in self._array_elements:
            serialized_value = self.element_template.as_serializable(array_element, attribute_filter, minified)
            _result_array.append(serialized_value)

        return _result_array

    def attribute_rewrite_map(self):
        return self.element_template.attribute_rewrite_map()

    def attribute_rewrite_reverse_map(self):
        return self.element_template.attribute_rewrite_reverse_map()

    def get_attribute_filter(self, default_value=False):
        return self.element_template.get_attribute_filter(default_value)
