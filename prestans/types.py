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
import os
import copy
import string
import inspect
import base64

from datetime import datetime
from datetime import date
from datetime import time

import prestans.parser
import prestans.exception

#:
#: Base type classes
#:

class DataType(object):

    def validate(self, value):
        raise NotImplementedError

class DataStructure(DataType):
    """
    Wrappers on Python types generally represented as structures e.g DateTime

    as_serializable methods signature for %DataStructure is different to that of DataCollection
    it requires a value to be passed in, this is because the python type of structures is
    difference to what gets serialized.

    E.g DateTime serializes itself as a ISO string
    """

    def as_serializable(self, value):
        raise NotImplementedError

class DataCollection(DataType):

    def validate(self, value, attribute_filter=None):
        raise NotImplementedError

    def as_serializable(self, attribute_filter=None):
        raise NotImplementedError

    def get_attribute_filter(self):
        raise NotImplementedError

#:
#: Basic Types
#:

class String(DataType):

    def __init__(self, default=None, min_length=None, max_length=None,\
        required=True, format=None, choices=None, utf_encoding='utf-8',\
        description=None, trim=True):

        if min_length and max_length and min_length > max_length:
            pass

        if required and min_length and min_length < 1:
            pass

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
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default

        try:
            if isinstance(value, unicode):
                _validated_value = u''.join(value).encode(self._utf_encoding).strip()
            else:
                _validated_value = str(value)
        except Exception, exp:
            raise prestans.exception.ParseFailedError("unicode or string encoding failed, %s" % exp)

        if self._trim:
            _validated_value = _validated_value.strip()

        #check for required and empty string
        if self._required and len(_validated_value) == 0:
            raise prestans.exception.RequiredAttributeError()

        if not self._required and len(_validated_value) == 0:
            return _validated_value

        if _validated_value is not None and self._min_length is not None and \
           len(_validated_value) < self._min_length:
            raise prestans.exception.MinimumLengthError(value, self._min_length)
        if _validated_value is not None and self._max_length is not None and \
           len(_validated_value) > self._max_length:
            raise prestans.exception.MaximumLengthError(value, self._max_length)

        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exception.InvalidChoiceError(value, self._choices)

        if self._format is not None and re.search(self._format, _validated_value) is None:
            raise prestans.exception.InvalidFormatError(_validated_value)

        return _validated_value

class Integer(DataType):

    def __init__(self, default=None, minimum=None, maximum=None,\
        required=True, choices=None, description=None):

        if minimum and maximum and minimum > maximum:
            pass

        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices
        self._description = description

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def default(self):
        return self._default

    @property
    def choices(self):
        return self._choices

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'integer'

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

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default

        try:
            if isinstance(value, long):
                _validated_value = long(value)
            else:
                _validated_value = int(value)
        except Exception as exp:
            raise prestans.exception.ParseFailedError("encoding failed: value is not an integer or a long")

        if _validated_value is not None and self._minimum is not None and _validated_value < self._minimum:
            raise prestans.exception.LessThanMinimumError(value, self._minimum)
        if _validated_value is not None and self._maximum is not None and _validated_value > self._maximum:
            raise prestans.exception.MoreThanMaximumError(value, self._maximum)

        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exception.InvalidChoiceError(value, self._choices)

        return _validated_value

class Float(DataType):

    def __init__(self, default=None, minimum=None, maximum=None, required=True,\
        choices=None, description=None):

        if minimum and maximum and minimum > maximum:
            pass

        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices
        self._description = description

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def default(self):
        return self._default

    @property
    def choices(self):
        return self._choices

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

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default

        try:
            _validated_value = float(value)
        except Exception, exp:
            raise prestans.exception.ParseFailedError("float encoding failed %s" % exp)

        if _validated_value is not None and self._minimum is not None and _validated_value < self._minimum:
            raise prestans.exception.LessThanMinimumError(value, self._minimum)

        if _validated_value is not None and self._maximum is not None and _validated_value > self._maximum:
            raise prestans.exception.MoreThanMaximumError(value, self._maximum)

        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exception.InvalidChoiceError(value, self._choices)

        return _validated_value

class Boolean(DataType):

    def __init__(self, default=None, required=True, description=None):

        self._default = default
        self._required = required
        self._description = description

    @property
    def default(self):
        return self._default

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'boolean'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def validate(self, value):

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            value = self._default

        try:
            _validated_value = bool(value)
        except Exception, exp:
            raise prestans.exception.ParseFailedError()

        return _validated_value


class DataURLFile(DataStructure):
    """
    Accepts a Fileupload as part of the JSON body using FileReader's readAsDataURL

    readAsDataURL, encodes the contents of the file as a DataURLScheme,
    http://en.wikipedia.org/wiki/Data_URI_scheme

    Example
    http://www.html5rocks.com/en/tutorials/file/dndfiles/

    Meta information about the file upload is upto the implementing application
    """

    @classmethod
    def generate_filename(cls):
        import uuid
        return uuid.uuid4().hex

    def __init__(self, required=True, allowed_mime_types=[], description=None):

        self._required = required
        self._allowed_mime_types = allowed_mime_types
        self._description = description

        if isinstance(allowed_mime_types, str):
            self._allowed_mime_types = [allowed_mime_types]

        self._mime_type = None
        self._file_contents = None

    @property
    def allowed_mime_types(self):
        return self._allowed_mime_types

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'data_url_file'

        constraints = dict()
        constraints['required'] = self._required
        constraints['allowed_mime_types'] = self._allowed_mime_types
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def file_contents(self):
        return self._file_contents

    @property
    def base64_contents(self):
        return base64.b64encode(self._file_contents)

    def validate(self, value):

        _validated_value = self.__class__()

        if self._required and value is None:
            raise prestans.exception.RequiredAttributeError()

        if self._required is False and value is None:
            return value

        try:
            data_url, delimiter, base64_content = value.partition(',')
            _validated_value._mime_type = data_url.replace(';base64', '').replace('data:', '')
            _validated_value._file_contents = base64.b64decode(base64_content)
        except Exception, exp:
            raise prestans.exception.ParseFailedError("data url file encoding failed %s" % exp)

        if self._allowed_mime_types and len(self._allowed_mime_types) > 0 \
        and not _validated_value._mime_type in self._allowed_mime_types:
            raise prestans.exception.InvalidChoiceError(_validated_value._mime_type,\
                self._allowed_mime_types)

        return _validated_value

    def save(self, path):
        """
        Writes file to a particular location

        This won't work for cloud environments like Google's Appengine, use with caution
        ensure to catch exceptions so you can provide informed feedback.

        prestans does not mask File IO exceptions so your handler can respond better.
        """

        file_handle = open(path, 'wb')
        file_handle.write(self._file_contents)
        file_handle.close()

    def as_serializable(self, value):
        #: This is passed in a DataURLFile and we construct a String back from it
        return "data:%s;base64,%s" % (value.mime_type, value.base64_contents)

#:
#: DataStructures
#: Default format is the Date Time Format string, defaults to RFC822
#:

class DateTime(DataStructure):

    class CONSTANT:
        NOW = '_PRESTANS_CONSTANT_MODEL_DATETIME_NOW'

    def __init__(self, default=None, required=True, format="%Y-%m-%d %H:%M:%S",\
        timezone=False, utc=False, description=None):

        self._default = default
        self._required = required
        self._timezone = timezone
        self._utc = utc
        self._format = format
        self._description = description

    @property
    def default(self):
        return self._default

    @property
    def format(self):
        return self._format

    @property
    def timezone(self):
        return self._timezone

    @property
    def utc(self):
        return self._utc

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
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            if self._default == DateTime.CONSTANT.NOW:
                value = datetime.now()
            else:
                value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            if self._default == DateTime.CONSTANT.NOW:
                value = datetime.now()
            else:
                value = self._default

        if type(value) == datetime:
            _validated_value = value
        elif type(value) == str or type(value) == unicode:
            try:
                _validated_value = datetime.strptime(value, self._format)
            except ValueError, exp:
                raise prestans.exception.ParseFailedError("date time parsing failed %s" % exp)
        else:
            raise prestans.exception.ParseFailedError("cannot parse value of type %s"\
                % value.__class__.__name__)

        return _validated_value

    def as_serializable(self, value):

        if not type(value) == datetime:
            raise prestans.exception.InvalidTypeError(value, 'datetime.datetime')

        return value.strftime(self._format)

class Date(DataStructure):

    class CONSTANT:
        TODAY = '_PRESTANS_CONSTANT_MODEL_DATE_TODAY'

    def __init__(self, default=None, required=True, format="%Y-%m-%d", description=None):

        self._default = default
        self._required = required
        self._format = format
        self._description = description

    @property
    def default(self):
        return self._default

    @property
    def format(self):
        return self._format

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'date'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def validate(self, value):

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            if self._default == Date.CONSTANT.TODAY:
                value = date.today()
            else:
                value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            if self._default == Date.CONSTANT.TODAY:
                value = date.today()
            else:
                value = self._default

        if type(value) == date:
            _validated_value = value
        elif type(value) == str or type(value) == unicode:
            try:
                _validated_value = datetime.strptime(value, self._format).date()
            except ValueError, exp:
                raise prestans.exception.ParseFailedError("date parsing failed %s" % exp)
        else:
            raise prestans.exception.ParseFailedError("cannot parse value of type %s" %\
                value.__class__.__name__)

        return _validated_value

    def as_serializable(self, value):

        if not type(value) == date:
            raise prestans.exception.InvalidTypeError(value, 'datetime.date')

        return value.strftime(self._format)

class Time(DataStructure):

    class CONSTANT:
        NOW = '_PRESTANS_CONSTANT_MODEL_TIME_NOW'

    def __init__(self, default=None, required=True, format="%H:%M:%S", description=None):

        self._default = default
        self._required = required
        self._format = format
        self._description = description

    @property
    def default(self):
        return self._default

    @property
    def format(self):
        return self._format

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'time'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def validate(self, value):

        _validated_value = None

        if self._required and self._default is None and value is None:
            raise prestans.exception.RequiredAttributeError()
        elif self._required and value is None:
            if self._default == Time.CONSTANT.NOW:
                value = time.today()
            else:
                value = self._default
        elif not self._required and self._default is None and value is None:
            return _validated_value
        elif not self._required and value is None:
            if self._default == Time.CONSTANT.NOW:
                value = time.today()
            else:
                value = self._default

        if isinstance(value, time):
            _validated_value = value
        elif isinstance(value, str) or isinstance(value, unicode):
            try:
                _validated_value = datetime.strptime(value, self._format).time()
            except ValueError, exp:
                raise prestans.exception.ParseFailedError("time parsing failed %s" % exp)
        else:
            raise prestans.exception.ParseFailedError("cannot parse value of type %s"\
                % value.__class__.__name__)

        return _validated_value

    def as_serializable(self, value):

        if not type(value) == time:
            raise prestans.exception.InvalidTypeError(value, 'datetime.time')

        return value.strftime(self._format)

#:
#: Collections
#:

class Array(DataCollection):

    def __init__(self, default=None, required=True, element_template=None,\
        min_length=None, max_length=None, description=None):

        if not isinstance(element_template, DataType):
            raise TypeError("Array element_template must a DataType subclass; %s given" %\
                element_template.__class__.__name__)

        #:
        #: Force required to be True if basic type in  use
        #:
        if isinstance(element_template, DataType)\
         and not isinstance(element_template, DataCollection)\
          and not isinstance(element_template, DataStructure):
            element_template._required = True

        self._default = default
        self._required = required
        self._element_template = element_template
        self._min_length = min_length
        self._max_length = max_length
        self._description = description

        self._array_elements = list()

    def __len__(self):
        return len(self._array_elements)

    def __iter__(self):
        #:
        #: With a little help from
        #: http://johnmc.co/llum/the-easiest-way-to-implement-__iter__-for-a-python-object/
        #:
        for element in self._array_elements:
            yield element

    def __getitem__(self, index):
        return self._array_elements[index]

    def __constains__(self, item):
        return item in self._array_elements

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
    def element_template(self):
        return self._element_template

    @property
    def is_scalar(self):
        return isinstance(self._element_template, Float) or isinstance(self._element_template, Boolean) or \
                isinstance(self._element_template, Integer) or isinstance(self._element_template, String)

    @element_template.setter
    def element_template(self, value):
        self._element_template = value

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'array'

        constraints = dict()
        # constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['min_length'] = self._min_length
        constraints['max_length'] = self._max_length
        constraints['element_template'] = self._element_template.blueprint()
        constraints['description'] = self._description

        blueprint['constraints'] = constraints
        return blueprint

    def remove(self, value):
        self._array_elements.remove(value)

    def validate(self, value, attribute_filter=None, minified=False):

        if not self._required and not value:
            return None

        _validated_value = self.__class__(element_template=self._element_template,\
                                     min_length=self._min_length,\
                                     max_length=self._max_length)

        if not isinstance(value, (list, tuple)):
            raise TypeError(value)

        for array_element in value:

            if isinstance(self._element_template, DataCollection):
                validated_array_element = self._element_template.\
                validate(array_element, attribute_filter)
            else:
                validated_array_element = self._element_template.\
                validate(array_element)

            _validated_value.append(validated_array_element)

        if self._min_length is not None and len(_validated_value) < self._min_length:
            raise prestans.exception.LessThanMinimumError(value, self._min_length)

        if self._max_length is not None and len(_validated_value) > self._max_length:
            raise prestans.exception.MoreThanMaximumError(value, self._max_length)

        return _validated_value

    def append(self, value):

        if isinstance(value, (list, tuple)):

            for element in value:
                self.append(element)
            return

        #check for basic types supported by array
        if isinstance(self._element_template, String) or \
           isinstance(self._element_template, Integer) or \
           isinstance(self._element_template, Float) or \
           isinstance(self._element_template, Boolean):
            value = self._element_template.__class__().validate(value)
        elif not isinstance(value, self._element_template.__class__):
            raise TypeError("prestans array elements must be of type %s; given %s"\
                % (self._element_template.__class__.__name__, value.__class__.__name__))

        self._array_elements.append(value)

    def as_serializable(self, attribute_filter=None, minified=False):

        _result_array = list()

        for array_element in self._array_elements:

            if isinstance(array_element, DataCollection):
                serialized_value = array_element.as_serializable(attribute_filter, minified)
                _result_array.append(serialized_value)
            elif isinstance(array_element, DataStructure):
                serialized_value = self._element_template.as_serializable(array_element)
                _result_array.append(serialized_value)
            elif isinstance(self._element_template, DataType):
                _result_array.append(array_element)




        return _result_array

    def attribute_rewrite_map(self):
        return self._element_template.attribute_rewrite_map()

    def attribute_rewrite_reverse_map(self):
        return self._element_template.attribute_rewrite_reverse_map()

    def get_attribute_filter(self, default_value=False):

        attribute_filter = None

        if isinstance(self._element_template, DataCollection):
            attribute_filter = self._element_template.get_attribute_filter(default_value)
        elif isinstance(self._element_template, DataType) or \
            isinstance(self._element_template, DataStructure):
            attribute_filter = default_value

        return attribute_filter

#:
#: Models
#:

class Model(DataCollection):

    def __init__(self, required=True, default=None, description=None, **kwargs):
        """
        If you are using the Model constructor to provide Meta data, you can provide it
        a default dictionary to initialise instance to initalise it from

        Can run _create_instance_attributes to copy attribute tempaltes to the instance,
        Model instances do not have any configurable options.

        @param required whether or not this model is required when used as an attribute
        @param default provides a default value for your type, used if one is not provided
        @param kwargs Named parameters of which to instantiate the model with
        """

        self._required = required
        self._default = default
        self._description = description

        self._create_instance_attributes(kwargs)

    def default(self):
        return self._default

    def attribute_count(self):

        count = 0
        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataType):
                _attribute_keys.append(attribute_name)

        return count

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
        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if not isinstance(type_instance, DataType):
                raise TypeError("%s must be of a DataType subclass" % attribute_name)

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint

    def __setattr__(self, key, value):

        if key[0:1] == "_":
            self.__dict__[key] = value
            return

        model_class_members = inspect.getmembers(self.__class__)

        validator = None
        for attribute_name, type_instance in model_class_members:
            if attribute_name == key:
                validator = type_instance

        if validator is not None:

            try:
                if validator.__class__ == value.__class__:
                    self.__dict__[key] = value
                else:
                    self.__dict__[key] = validator.validate(value)

            except prestans.exception.DataValidationException as exp:
                raise prestans.exception.ValidationError(\
                message=str(exp),\
                attribute_name=key,\
                value=value,\
                blueprint=validator.blueprint())

            return

        raise KeyError("No key named %s; in instance of type %s "\
            % (key, self.__class__.__name__))

    def _create_instance_attributes(self, arguments):
        """
        Copies class level attribute templates and makes instance placeholders

        This step is required for direct uses of Model classes. This creates a
        copy of attribute_names ignores methods and private variables.
        DataCollection types are deep copied to ignore memory reference conflicts.

        DataType instances are initialized to None or default value.
        """

        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataCollection):
                self.__dict__[attribute_name] = copy.deepcopy(type_instance)
                continue

            if type_instance is None:
                self.__dict__[attribute_name] = None
                continue

            if isinstance(type_instance, DataType):

                try:
                    value = None

                    if arguments.has_key(attribute_name):
                        value = arguments[attribute_name]

                    self.__dict__[attribute_name] = type_instance.validate(value)

                except prestans.exception.DataValidationException, exp:
                    self.__dict__[attribute_name] = None

    def get_attribute_keys(self):
        """
        Returns a list of managed attributes for the Model class

        Implemented for use with data adapters, can be used to quickly make a list of the
        attribute names in a prestans model
        """

        _attribute_keys = list()

        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataType):
                _attribute_keys.append(attribute_name)

        return _attribute_keys

    def get_attribute_filter(self, default_value=False):

        attribute_filter = prestans.parser.AttributeFilter()

        _model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in _model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataCollection):
                setattr(attribute_filter, attribute_name,\
                    type_instance.get_attribute_filter(default_value))
            else:
                setattr(attribute_filter, attribute_name, default_value)

        return attribute_filter

    def validate(self, value, attribute_filter=None, minified=False):

        if self._required and (value is None or not isinstance(value, dict)):
            """
            Model level validation requires a parsed dictionary
            this is done by the serializer
            """
            raise prestans.exception.RequiredAttributeError()

        if not value and self._default:
            return self._default

        if not self._required and not value:
            """
            Value was not provided by caller, but require a template
            """
            return None

        _model_instance = self.__class__()
        _model_class_members = inspect.getmembers(self.__class__)

        rewrite_map = self.attribute_rewrite_map()

        for attribute_name, type_instance in _model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if attribute_filter and not attribute_filter.is_attribute_visible(attribute_name):
                _model_instance.__dict__[attribute_name] = None
                continue

            if not isinstance(type_instance, DataType):
                raise TypeError("%s must be a DataType subclass" % attribute_name)

            validation_input = None

            input_value_key = attribute_name

            #: Minification support
            if minified is True:
                input_value_key = rewrite_map[attribute_name]

            if value.has_key(input_value_key):
                validation_input = value[input_value_key]

            try:

                if isinstance(type_instance, DataCollection):
                    sub_attribute_filter = None
                    if attribute_filter and attribute_filter.has_key(attribute_name):
                        sub_attribute_filter = getattr(attribute_filter, attribute_name)

                    validated_object = type_instance.validate(validation_input,\
                        sub_attribute_filter, minified)
                else:
                    validated_object = type_instance.validate(validation_input)

                _model_instance.__dict__[attribute_name] = validated_object

            except prestans.exception.DataValidationException as exp:
                raise prestans.exception.ValidationError(\
                message=str(exp),\
                attribute_name=attribute_name,\
                value=validation_input,\
                blueprint=type_instance.blueprint())

        return _model_instance

    #:
    #: Rewrite map generation
    #:

    def attribute_rewrite_map(self):

        rewrite_map = dict()
        model_class_members = inspect.getmembers(self.__class__)

        token_rewrite_map = self._generate_attribute_token_rewrite_map(model_class_members)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataType):
                attribute_tokens = attribute_name.split('_')

                rewritten_attribute_name = ''
                for token in attribute_tokens:
                    rewritten_attribute_name += token_rewrite_map[token] + "_"
                #: Remove the trailing underscore
                rewritten_attribute_name = rewritten_attribute_name[:-1]

                rewrite_map[attribute_name] = rewritten_attribute_name

        return rewrite_map

    def attribute_rewrite_reverse_map(self):

        rewrite_map = dict()
        model_class_members = inspect.getmembers(self.__class__)

        token_rewrite_map = self._generate_attribute_token_rewrite_map(model_class_members)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataType):
                attribute_tokens = attribute_name.split('_')

                rewritten_attribute_name = ''
                for token in attribute_tokens:
                    rewritten_attribute_name += token_rewrite_map[token] + "_"
                #: Remove the trailing underscore
                rewritten_attribute_name = rewritten_attribute_name[:-1]

                rewrite_map[rewritten_attribute_name] = attribute_name

        return rewrite_map

    def has_key(self, attribute_name):

        members = inspect.getmembers(self)

        has_key = self.__class__.__dict__.has_key(attribute_name)

        if not has_key:

            base_classes = list()
            base_classes += list(self.__class__.__bases__)

            while not has_key and base_classes:

                #take a base class from the list
                base_class = base_classes.pop()

                #we found it clear the list
                if base_class.__dict__.has_key(attribute_name):
                    has_key = True
                    base_classes = list()
                #add any more base classes from this class
                else:
                    base_classes += list(base_class.__bases__)

        return has_key

    def _generate_attribute_token_rewrite_map(self, model_class_members):

        rewrite_tokens = self._generate_attribute_tokens(model_class_members)
        minified_tokens = self._generate_minfied_keys(len(rewrite_tokens))

        return dict(zip(rewrite_tokens, minified_tokens))

    def _generate_attribute_tokens(self, model_class_members):

        rewrite_tokens = list()

        #: Create a list of tokens
        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(type_instance, DataType):
                rewrite_tokens = rewrite_tokens + attribute_name.split('_')

        #: Remove duplicated; sort alphabetically for the algorithm to work
        rewrite_tokens = list(set(rewrite_tokens))
        rewrite_tokens.sort()

        return rewrite_tokens

    def _generate_minfied_keys(self, length=26, prefix=''):

        minified_keys = list()

        overflow = 0
        if length > 26:
            overflow = length - 26
            length = 26

        for index in range(0, length):

            generated_char = self._generate_attribute_key(index)
            minified_keys.append(prefix + generated_char)

            if overflow > 0:

                sublist_length = overflow
                if sublist_length > 26:
                    sublist_length = 26

                sublist = self._generate_minfied_keys(sublist_length, generated_char)
                minified_keys = minified_keys + sublist
                overflow = overflow - len(sublist)

        if prefix == '':
            minified_keys.sort(key=len, reverse=False)

        return minified_keys


    def _generate_attribute_key(self, val):
        return string.lowercase[val%26]*(val/26+1)

    #:
    #: Serialization
    #:

    def as_serializable(self, attribute_filter=None, minified=False):
        """
        Returns a dictionary with attributes and pure python representation of
        the data instances. If an attribute filter is provided as_serializable
        will respect the visibility.

        The response is used by serializers to return data to client
        """

        model_dictionary = dict()
        model_class_members = inspect.getmembers(self.__class__)

        rewrite_map = self.attribute_rewrite_map()

        for attribute_name, type_instance in model_class_members:

            serialized_attribute_name = attribute_name

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if isinstance(attribute_filter, prestans.parser.AttributeFilter) and\
             not attribute_filter.is_attribute_visible(attribute_name):
                continue

            #: Support minification
            if minified is True:
                serialized_attribute_name = rewrite_map[attribute_name]

            if not self.__dict__.has_key(attribute_name) or self.__dict__[attribute_name] is None:
                model_dictionary[serialized_attribute_name] = None
                continue

            if isinstance(type_instance, DataCollection):

                sub_attribute_filter = None
                if isinstance(attribute_filter, prestans.parser.AttributeFilter) and\
                 attribute_filter.has_key(attribute_name):
                    sub_attribute_filter = getattr(attribute_filter, attribute_name)

                model_dictionary[serialized_attribute_name] = self.__dict__[attribute_name].\
                as_serializable(sub_attribute_filter, minified)

            elif isinstance(type_instance, DataStructure):
                python_value = self.__dict__[attribute_name]
                serializable_value = type_instance.as_serializable(python_value)
                model_dictionary[serialized_attribute_name] = serializable_value

            elif isinstance(type_instance, DataType):
                model_dictionary[serialized_attribute_name] = self.__dict__[attribute_name]

        return model_dictionary

#:
#: Body Response Template to transfer binary files
#:

class BinaryResponse(object):

    def __init__(self, mime_type=None, file_name=None, as_attachment=True, contents=None):

        if mime_type is not None:
            self._mime_type = mime_type.encode('ascii', 'ignore')
        else:
            self._mime_type = mime_type

        if file_name is not None:
            self._file_name = file_name.encode('ascii', 'ignore')
        else:
            self._file_name = file_name

        self._as_attachment = as_attachment
        self._contents = contents

    @property
    def mime_type(self):
        return self._mime_type

    @mime_type.setter
    def mime_type(self, value):
        self._mime_type = value.encode('ascii', 'ignore')

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value.encode('ascii', 'ignore')

    @property
    def as_attachment(self):
        return self._as_attachment

    @as_attachment.setter
    def as_attachment(self, value):
        self._as_attachment = value

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, value):
        self._contents = contents

    @property
    def content_length(self):
        if self._contents == None:
            return 0
        return len(self._contents)

    def validate(self):
        return self._mime_type != None\
         and self._file_name != None\
          and self.content_length > 0


