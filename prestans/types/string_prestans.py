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

from prestans import exception
from prestans.types import DataType


class String(DataType):

    def __init__(self, default=None, min_length=None, max_length=None,
                 required=True, format=None, choices=None, utf_encoding='utf-8',
                 description=None, trim=True):

        if min_length and max_length and min_length > max_length:
            raise ValueError("max length cannot be less than min length")

        if min_length and min_length < 1:
            raise ValueError("min length must be positive")

        if max_length and max_length < 1:
            raise ValueError("max length must be positive")

        self._default = default
        self._min_length = min_length
        self._max_length = max_length
        self._required = required
        self._format = format
        self._choices = choices
        self._utf_encoding = utf_encoding
        self._description = description
        self._trim = trim

    @property
    def required(self):
        return self._required

    @property
    def max_length(self):
        return self._max_length

    @property
    def min_length(self):
        return self._min_length

    @property
    def default(self):
        return self._default

    @property
    def choices(self):
        return self._choices

    @property
    def format(self):
        return self._format

    @property
    def description(self):
        return self._description

    @property
    def trim(self):
        return self._trim

    @property
    def utf_encoding(self):
        return self._utf_encoding

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'string'

        constraints = dict()
        constraints['default'] = self._default
        constraints['min_length'] = self._min_length
        constraints['max_length'] = self._max_length
        constraints['required'] = self._required
        constraints['format'] = self._format
        constraints['choices'] = self._choices
        constraints['utf_encoding'] = self._utf_encoding
        constraints['description'] = self._description
        constraints['trim'] = self._trim

        blueprint['constraints'] = constraints

        return blueprint

    def validate(self, value):

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise exception.RequiredAttributeError()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default

        try:
            from prestans.util import string_types

            if isinstance(value, string_types):
                _validated_value = value
            else:
                _validated_value = str(value)
        except Exception as exp:
            raise exception.ParseFailedError("unicode or string encoding failed, %s" % exp)

        if self._trim:
            _validated_value = _validated_value.strip()

        # check for required and empty string
        if self._required and len(_validated_value) == 0:
            raise exception.RequiredAttributeError()

        if not self._required and len(_validated_value) == 0:
            return _validated_value

        if _validated_value is not None and self._min_length is not None and \
                len(_validated_value) < self._min_length:
            raise exception.MinimumLengthError(value, self._min_length)
        if _validated_value is not None and self._max_length is not None and \
                len(_validated_value) > self._max_length:
            raise exception.MaximumLengthError(value, self._max_length)

        if self._choices is not None and not _validated_value in self._choices:
            raise exception.InvalidChoiceError(value, self._choices)

        if self._format is not None and re.search(self._format, _validated_value) is None:
            raise exception.InvalidFormatError(_validated_value)

        return _validated_value
