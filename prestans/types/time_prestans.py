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
from datetime import datetime
from datetime import time

from prestans import exception
from prestans.types import DataStructure


class Time(DataStructure):

    DEFAULT_FORMAT = "%H:%M:%S"
    NOW = '_PRESTANS_CONSTANT_MODEL_TIME_NOW'
    UTC_NOW = '_PRESTANS_CONSTANT_MODEL_TIME_UTC_NOW'

    def __init__(self, default=None, required=True, format=DEFAULT_FORMAT, description=None):

        if isinstance(default, time) or \
           default == self.NOW or \
           default == self.UTC_NOW or \
           default is None:
            self._default = default
        else:
            raise TypeError("default must be one of time, Time.NOW or Time.UTC_NOW")

        self._required = required
        self._format = format
        self._description = description

    @property
    def default(self):
        return self._default

    @property
    def required(self):
        """
        :return:
        :rtype: bool
        """
        return self._required

    @property
    def format(self):
        return self._format

    @property
    def description(self):
        return self._description

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'time'

        constraints = dict()
        constraints['default'] = self.default
        constraints['required'] = self.required
        constraints['format'] = self.format
        constraints['description'] = self.description

        blueprint['constraints'] = constraints
        return blueprint

    def validate(self, value):
        from prestans.util import string_types

        _validated_value = None

        # no need to do any validation if None, not required and default provided
        if not self._required and self._default is None and value is None:
            return value
        elif self._required and self._default is None and value is None:
            raise exception.RequiredAttributeError()
        elif value is None and self._default is not None:
            if self._default == Time.NOW:
                value = datetime.now()
            elif self._default == Time.UTC_NOW:
                value = datetime.utcnow()
            else:
                value = self._default

        if isinstance(value, time):
            _validated_value = value
        elif isinstance(value, string_types):
            try:
                _validated_value = datetime.strptime(value, self._format).time()
            except ValueError as exp:
                raise exception.ParseFailedError("time parsing failed %s" % exp)
        else:
            raise exception.ParseFailedError("cannot parse value of type %s" % value.__class__.__name__)

        return _validated_value

    def as_serializable(self, value):

        if not type(value) == time:
            raise exception.InvalidTypeError(value, 'datetime.time')

        return value.strftime(self._format)
