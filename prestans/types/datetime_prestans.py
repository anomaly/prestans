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
from datetime import datetime as datetime_type
from datetime import datetime

from prestans import exception
from prestans.types import DataStructure


class DateTime(DataStructure):

    DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"
    NOW = '_PRESTANS_CONSTANT_MODEL_DATETIME_NOW'
    UTC_NOW = '_PRESTANS_CONSTANT_MODEL_DATETIME_UTC_NOW'

    def __init__(self, default=None, required=True, format=DEFAULT_FORMAT,
                 timezone=False, utc=False, description=None):

        if isinstance(default, datetime_type) or \
                default == self.NOW or \
                default == self.UTC_NOW or \
                default is None:
            self._default = default
        else:
            raise TypeError("default must be one of datetime, DateTime.NOW or DateTime.UTC_NOW")

        self._required = required
        self._timezone = timezone
        self._utc = utc
        self._format = format
        self._description = description

    @property
    def default(self):
        return self._default

    @property
    def required(self):
        return self._required

    @property
    def format(self):
        return self._format

    @property
    def timezone(self):
        return self._timezone

    @property
    def utc(self):
        return self._utc

    @property
    def description(self):
        return self._description

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'datetime'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format
        constraints['timezone'] = self._timezone
        constraints['utc'] = self._utc
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def validate(self, value):

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise exception.RequiredAttributeError()
        elif self._required and value is None:
            if self._default == DateTime.NOW:
                value = datetime.now()
            elif self._default == DateTime.UTC_NOW:
                value = datetime.utcnow()
            else:
                value = self._default

        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            if self._default == DateTime.NOW:
                value = datetime.now()
            elif self._default == DateTime.UTC_NOW:
                value = datetime.utcnow()
            else:
                value = self._default

        from prestans.util import string_types

        if isinstance(value, datetime_type):
            _validated_value = value
        elif isinstance(value, string_types):
            try:
                _validated_value = datetime.strptime(value, self._format)
            except ValueError as exp:
                raise exception.ParseFailedError("date time parsing failed %s" % exp)
        else:
            raise exception.ParseFailedError("cannot parse value of type %s" % value.__class__.__name__)

        return _validated_value

    def as_serializable(self, value):

        if not type(value) == datetime:
            raise exception.InvalidTypeError(value, 'datetime.datetime')

        return value.strftime(self._format)
