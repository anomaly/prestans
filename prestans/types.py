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
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

class DataStructure(DataType):
    """
    Wrappers on Python types generally represented as structures e.g DateTime

    as_serializable methods signature for %DataStructure is different to that of DataCollection
    it requires a value to be passed in, this is because the python type of structures is 
    difference to what gets serialized.

    E.g DateTime serializes itself as a ISO string
    """
    
    def as_serializable(self, value):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

class DataCollection(DataType):

    def validate(self, value, attribute_filter=None):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def as_serializable(self, attribute_filter=None):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def get_attribute_filter(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

#:
#: Basic Types
#:

class String(DataType):
    
    def __init__(self, default=None, min_length=None, max_length=None, 
        required=True, format=None, choices=None, utf_encoding='utf-8'):

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
                _validated_value = str(value.decode(self._utf_encoding))
            else:
                _validated_value = str(value)
        except:
            raise prestans.exception.ParseFailedError(value, 'String')
        
        if not self._required and len(_validated_value) == 0:
            return _validated_value
        
        if _validated_value is not None and self._min_length and len(_validated_value) < self._min_length:
            raise prestans.exception.UnacceptableLengthError(value, self._min_length, self._max_length)
        if _validated_value is not None and self._max_length and len(_validated_value) > self._max_length:
            raise prestans.exception.UnacceptableLengthError(value, self._min_length, self._max_length)
            
        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exception.InvalidChoiceError(value, self._choices)
            
        if self._format is not None and re.search(self._format, _validated_value) is None:
            raise prestans.exception.InvalidFormatError(_validated_value)
        
        return _validated_value

class Integer(DataType):

    def __init__(self, default=None, minimum=None, maximum=None, 
        required=True, choices=None):

        if minimum and maximum and minimum > maximum:
            pass

        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'integer'

        constraints = dict()
        constraints['default'] = self._default
        constraints['minimum'] = self._minimum
        constraints['maximum'] = self._maximum
        constraints['required'] = self._required
        constraints['choices'] = self._choices

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
            _validated_value = int(value)
        except:
            raise prestans.exception.ParseFailedError(value, 'Integer')
        
        if _validated_value and self._minimum is not None and _validated_value < self._minimum:
            raise prestans.exception.LessThanMinimumError(value, self._minimum)
        if _validated_value and self._maximum is not None and _validated_value > self._maximum:
            raise prestans.exception.MoreThanMaximumError(value, self._maximum)
            
        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exception.InvalidChoiceError(value, self._choices)
        
        return _validated_value

class Float(DataType):

    def __init__(self, 
                 default=None, 
                 minimum=None, 
                 maximum=None, 
                 required=True, 
                 choices=None):
        
        if minimum and maximum and minimum > maximum:
            pass
        
        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'float'
        
        constraints = dict()
        constraints['default'] = self._default
        constraints['minimum'] = self._minimum
        constraints['maximum'] = self._maximum
        constraints['required'] = self._required
        constraints['choices'] = self._choices

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
        except:
            raise prestans.exception.ParseFailedError(value, 'Float')
        
        if _validated_value and self._minimum is not None and _validated_value < self._minimum:
            raise prestans.exception.LessThanMinimumError(value, self._minimum)
        if _validated_value and self._maximum is not None and _validated_value > self._maximum:
            raise prestans.exception.MoreThanMaximumError(value, self._maximum)
            
        if self._choices is not None and not _validated_value in self._choices:
            raise prestans.exception.InvalidChoiceError(value, self._choices)
        
        return _validated_value

        
class Boolean(DataType):

    def __init__(self, default=None, required=True):


        self._default = default
        self._required = required

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'boolean'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required

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
        except: 
            raise prestans.exception.ParseFailedError(value, 'Boolean')
        
        return _validated_value


class DataURLFile(DataType):
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

    def __init__(self, required=True, allowed_mime_types=[]):

        self._required = required
        self._allowed_mime_types = allowed_mime_types

        if isinstance(allowed_mime_types, str):
            self._allowed_mime_types = [allowed_mime_types]

        self._mime_type = None
        self._file_contents = None

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'data_url_file'

        constraints = dict()
        constraints['required'] = self._required
        constraints['allowed_mime_types'] = self._allowed_mime_types

        blueprint['constraints'] = constraints
        return blueprint

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def file_contents(self):
        return self._file_contents        

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
        except Exception, err:
            raise prestans.exception.ParseFailedError(value, 'DataURLFile')

        if self._allowed_mime_types and len(self._allowed_mime_types) > 0 \
        and not _validated_value._mime_type in self._allowed_mime_types:
            raise prestans.exception.InvalidChoiceError(_validated_value._mime_type, self._allowed_mime_types)

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

#:
#: DataStructures
#: Default format is the Date Time Format string, defaults to RFC822
#:

class DateTime(DataStructure):

    class CONSTANT:
        NOW = '_PRESTANS_CONSTANT_MODEL_DATETIME_NOW'

    def __init__(self, default=None, required=True, format="%Y-%m-%d %H:%M:%S"):

        self._default = default
        self._required = required
        self._format = format

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'datetime'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format

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
                raise prestans.exception.ParseFailedError(value, 'DateTime')
        else:
            raise prestans.exception.ParseFailedError(value, 'DateTime')
            
        return _validated_value

    def as_serializable(self, value):

        if not type(value) == datetime:
            raise prestans.exception.InvalidTypeError(value, 'datetime.datetime')
            
        return value.strftime(self._format)

class Date(DataStructure):

    class CONSTANT:
        TODAY = '_PRESTANS_CONSTANT_MODEL_DATE_TODAY'
    
    def __init__(self, default=None, required=True, format="%Y-%m-%d"):

        self._default = default
        self._required = required
        self._format = format

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'date'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format

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
                raise prestans.exception.ParseFailedError(value, 'Date')
        else:
            raise prestans.exception.ParseFailedError(value, 'Date')
            
        return _validated_value

    def as_serializable(self, value):

        if not type(value) == date:
            raise prestans.exception.InvalidTypeError(value, 'datetime.date')
            
        return value.strftime(self._format)

class Time(DataStructure):

    class CONSTANT:
        NOW = '_PRESTANS_CONSTANT_MODEL_TIME_NOW'
    
    def __init__(self, default=None, required=True, format="%H:%M:%S"):

        self._default = default
        self._required = required
        self._format = format

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'time'

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format

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
        
        if type(value) == time:
            _validated_value = value
        elif type(value) == str or type(value) == unicode:
            try:
                _validated_value = datetime.strptime(value, self._format).time()
            except ValueError, exp:
                raise prestans.exception.ParseFailedError(value, 'Time')
        else:
            raise prestans.exception.ParseFailedError(value, 'Time')

        return _validated_value

    def as_serializable(self, value):

        if not type(value) == time:
            raise prestans.exception.InvalidTypeError(value, 'datetime.time')
            
        return value.strftime(self._format)

#:
#: Collections
#:

class Array(DataCollection):
    
    def __init__(self, default=None, required=True, element_template=None, 
        min_length=None, max_length=None):
        
        self._default = default
        self._required = required
        self._element_template = element_template
        self._min_length = min_length
        self._max_length = max_length
        
        self._array_elements = list()

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'array'

        constraints = dict()
        # constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['min_length'] = self._min_length
        constraints['max_length'] = self._max_length
        constraints['element_template'] = self._element_template.blueprint()

        blueprint['constraints'] = constraints
        return blueprint

    @property
    def element_template(self):
        return self._element_template

    @element_template.setter
    def element_template(self, value):
        self._element_template = value

    def remove(self, value):
        self._array_elements.remove(value)
    
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

    def validate(self, value, attribute_filter=None):
        
        if not self._required and not value:
            return None

        _validated_value = self.__class__(element_template=self._element_template, 
                                     min_length=self._min_length, 
                                     max_length=self._max_length)
        
        if not isinstance(value, (list, tuple)):
            raise prestans.exception.InvalidCollectionError(value)
            
        for array_element in value:
    
            if issubclass(self._element_template.__class__, DataCollection):
                validated_array_element = self._element_template.validate(array_element, attribute_filter)
            else:
                validated_array_element = self._element_template.validate(array_element)
    
            _validated_value.append(validated_array_element)
    
        if self._min_length is not None and len(_validated_value) < self._min_length:
            raise prestans.exception.LessThanMinimumError(value, self._minimum)

        if self._max_length is not None and len(_validated_value) > self._max_length:
            raise prestans.exception.MoreThanMaximumError(value, self._maximum)

        return _validated_value
    
    def append(self, value):
        
        if isinstance(value, (list, tuple)):

            for element in value:
                self.append(element)
            return
        
        if isinstance(self._element_template, String) and \
        isinstance(value, str):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template, String) and \
        isinstance(value, unicode):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template, Integer) and \
        isinstance(value, int):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template, Float) and \
        isinstance(value, float):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template, Boolean) and \
        isinstance(value, bool):
            value = self._element_template.__class__().validate(value)
        elif not isinstance(value, self._element_template.__class__):
            raise TypeError("prestans array elements must be of type %s; given %s"
                            (self._element_template.__class__.__name__, value.__class__.__name__))
        
        self._array_elements.append(value)
            
    def as_serializable(self, attribute_filter=None, minified=False):
        
        _result_array = list()
            
        for array_element in self._array_elements:
        
            if isinstance(array_element, str) or \
            isinstance(array_element, unicode) or \
            isinstance(array_element, float) or \
            isinstance(array_element, int) or \
            isinstance(array_element, bool):

                _result_array.append(array_element)
            else:
                _result_array.append(array_element.as_serializable(attribute_filter, minified))
        
        return _result_array
        
    def get_attribute_filter(self, default_value=False):

        attribute_filter = None

        if issubclass(self._element_template.__class__, DataCollection):
            attribute_filter = self._element_template.get_attribute_filter(default_value)
        elif issubclass(self._element_template.__class__, DataType) or \
            issubclass(self._element_template.__class__, DataStructure):
            attribute_filter = default_value

        return attribute_filter

#:
#: Models
#:
        
class Model(DataCollection):

    def __init__(self, required=True, default=None, **kwargs):
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

    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = 'model'

        constraints = dict()
        constraints['required'] = self._required
        constraints['model_template'] = self.__class__.__name__
        blueprint['constraints'] = constraints

        # Fields
        fields = dict()
        model_class_members = inspect.getmembers(self.__class__)
    
        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if not isinstance(type_instance, DataType):
                raise DataTypeValidationException(
                    "%s must be of a DataType subclass" % attribute_name)

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint

    def __setattr__(self, key, value):
        
        if key[0:1] == "_":
            self.__dict__[key] = value
            return
        
        model_class_members = inspect.getmembers(self.__class__)
        
        validator = None
        for attribute_name,  type_instance in model_class_members:
            if attribute_name == key:
                validator = type_instance
            
        if validator is not None:
            if validator.__class__ == value.__class__:
                self.__dict__[key] = value
            else:
                self.__dict__[key] = validator.validate(value)
            
            return
            
        raise KeyError("No key named %s; in instance of type %s " % (key, self.__class__.__name__))
    
    def _create_instance_attributes(self, arguments):
        """
        Copies class level attribute templates and makes instance placeholders

        This step is required for direct uses of Model classes. This creates a copy of attribute_names
        ignores methods and private variables. DataCollection types are deep copied to ignore memory
        reference conflicts.

        DataType instances are initialized to None or default value.
        """

        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if issubclass(type_instance.__class__, DataCollection):
                self.__dict__[attribute_name] = copy.deepcopy(type_instance)
                continue
                
            if type_instance is None:
                self.__dict__[attribute_name] = None
                continue
                
            if issubclass(type_instance.__class__, DataType):
                
                try:
                    value = None
                    
                    if arguments.has_key(attribute_name):
                        value = arguments[attribute_name]
                        
                    self.__dict__[attribute_name] = type_instance.validate(value)

                except DataTypeValidationException:
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
            
            if issubclass(type_instance.__class__, DataType):
                _attribute_keys.append(attribute_name)
            
        return _attribute_keys

    def get_attribute_filter(self, default_value=False):

        attribute_filter = prestans.parser.AttributeFilter()

        _model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in _model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if issubclass(type_instance.__class__, DataCollection):
                setattr(attribute_filter, attribute_name, type_instance.get_attribute_filter(default_value))
            else:
                setattr(attribute_filter, attribute_name, default_value)

        return attribute_filter

    def validate(self, value, attribute_filter=None, minified=False):
        
        if self._required and (value is None or not isinstance(value, dict)):
            raise prestans.exception.RequiredAttributeError()
            
        if not value and self._default:
            return self._default
            
        if not self._required and not value:
            return None
            
        _model_instance = self.__class__()
        _model_class_members = inspect.getmembers(self.__class__)
    
        for attribute_name, type_instance in _model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                continue

            if attribute_filter and not attribute_filter.is_attribute_visible(attribute_name):
                _model_instance.__dict__[attribute_name] = None
                continue

            if not issubclass(type_instance.__class__, DataType):
                raise prestans.exception.InvalidDataTypeError(attribute_name, "DataType")

            validation_input = None
            
            if value.has_key(attribute_name):
                validation_input = value[attribute_name]
                
            try:
                
                if isinstance(type_instance, DataCollection):
                    sub_attribute_filter = None
                    if attribute_filter and attribute_filter.has_key(attribute_name):
                        sub_attribute_filter = getattr(attribute_filter, attribute_name)
                        
                    validated_object = type_instance.validate(validation_input, sub_attribute_filter)
                else:
                    validated_object = type_instance.validate(validation_input)
                
                _model_instance.__dict__[attribute_name] = validated_object
                    
            except prestans.exception.DataValidation, exp:
                #: @todo revise this
                raise prestans.exception.DataValidationError('%s, %s' % (attribute_name, str(exp)))

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
        