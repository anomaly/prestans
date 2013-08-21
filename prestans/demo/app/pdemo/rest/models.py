#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
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
#      * Neither the name of Eternity Technologies nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ETERNITY TECHNOLOGIES BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from prestans import types

class StringSample(types.Model):
	string_required = types.String(required=True)
	string_not_required = types.String(required=False)
	string_default = types.String(default="Hello World")
	string_min_length = types.String(min_length=1)
	string_max_length = types.String(max_length=5)
	string_choices = types.String(choices=["A", "B", "C"])
	string_format = types.String(format="^[0-9]+[a-z]{3}$")

class IntegerSample(types.Model):
	integer_required = types.Integer(required=True)
	integer_not_required = types.Integer(required=False)
	integer_default = types.Integer(default=6)
	integer_minimum = types.Integer(minimum=1)
	integer_maximum = types.Integer(maximum=5)
	integer_choices = types.Integer(choices=[1, 2, 3])

class FloatSample(types.Model):
	float_required = types.Float(required=True)
	float_not_required = types.Float(required=False)
	float_default = types.Float(default=6.0)
	float_minimum = types.Float(minimum=1.0)
	float_maximum = types.Float(maximum=5.0)
	float_choices = types.Float(choices=[1.1, 2.2, 3.3])

class BooleanSample(types.Model):
	boolean_required = types.Boolean(required=True)
	boolean_not_required = types.Boolean(required=False)
	boolean_default = types.Boolean(default=True)

class DateTime(types.Model):
	datetime_required = types.DateTime(required=True)
	datetime_not_required = types.DateTime(required=False)
	datetime_default_now = types.DateTime(default=types.DateTime.CONSTANT.NOW)
	datetime_default_string = types.DateTime(default="2013-01-01 12:01:34")

class Date(types.Model):
	date_required = types.Date(required=True)
	date_not_required = types.Date(required=False)
	date_default_today = types.Date(default=types.Date.CONSTANT.TODAY)
	date_default_string = types.Date(default="2013-01-02")

class Time(types.Model):
	time_required = types.Date(required=True)
	time_not_required = types.Date(required=False)
	time_default_now = types.Date(default=types.Time.CONSTANT.NOW)

class ModelSample(types.Model):
	integer_sample = IntegerSample()
	string_sample = StringSample()
	string_title = types.String(required=True)

class ArraySample(types.Model):
	model_array = types.Array(element_template=IntegerSample())
	integer_array = types.Array(element_template=types.Integer())
	string_array = types.Array(element_template=types.String())
	string_title = types.String(required=True)
