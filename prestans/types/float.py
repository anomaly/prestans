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
from prestans.types import DataType


class Float(DataType):

    def __init__(self, default=None, minimum=None, maximum=None, required=True,
                 choices=None, description=None):

        if minimum and maximum and minimum > maximum:
            raise ValueError("maximum cannot be less than minimum")

        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices
        self._description = description

    @property
    def default(self):
        return self._default

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def required(self):
        return self._required

    @property
    def choices(self):
        return self._choices

    @property
    def description(self):
        return self._description

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'float'

        constraints = dict()
        constraints['default'] = self._default
        constraints['minimum'] = self._minimum
        constraints['maximum'] = self._maximum
        constraints['required'] = self._required
        constraints['choices'] = self._choices
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def validate(self, value):

        if not self._required and self._default is None and value is None:
            return None
        if self._required and self._default is None and value is None:
            raise exception.RequiredAttributeError()
        elif self._required and value is None:
            value = self._default
        elif not self._required and value is None:
            value = self._default

        try:
            _validated_value = float(value)
        except Exception as exp:
            raise exception.ParseFailedError("float encoding failed %s" % exp)

        if _validated_value is not None and self._minimum is not None and _validated_value < self._minimum:
            raise exception.LessThanMinimumError(value, self._minimum)

        if _validated_value is not None and self._maximum is not None and _validated_value > self._maximum:
            raise exception.MoreThanMaximumError(value, self._maximum)

        if self._choices is not None and _validated_value not in self._choices:
            raise exception.InvalidChoiceError(value, self._choices)

        return _validated_value
