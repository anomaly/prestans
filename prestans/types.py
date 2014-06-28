#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2013, Anomaly Software Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
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
#  DISCLAIMED. IN NO EVENT SHALL Anomaly Software BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__all__ = ['DataTypeValidationException', 'DataType', 'DataCollection', 'String', 'Float', 'Integer', 'Boolean', 'DateTime', 'Array', 'Model']

## @package prestans.types provides wrappers on acceptable data types for REST requests
#
#  The wrappers are in line with what can be serialized down to the client by the REST
#  handlers, it was modelled based on the JSON standard but is equally valid for XML.
# 
#  Dictionaries are represented by Models and Array are collections.
#

import inspect
import exceptions
import copy
import re
import os
import base64
import uuid

from datetime import datetime
from datetime import date
from datetime import time

from prestans import ERROR_MESSAGE

import prestans.parsers

## @brief Provides a list of constants that types can use
#
class CONSTANT:
    TIME_NOW = 'CONSTANT_TIME_NOW'
    DATETIME_NOW = '129a8b5d-376b-4c70-b535-5c89b1b726fb'
    DATE_TODAY = '879864fa-6bfe-11e2-a3a9-3c07546f5fb6'
    ARRAY_DYNAMIC_ELEMENT_TEMPLATE = 'CONSTANT_ARRAY_DYNAMIC_ELEMENT_TEMPLATE'

## @brief Raised if one of the Metadata fields has invalid input
#
#  @ingroup exceptions
#
class InvalidMetadata(Exception):
    pass

## @brief raised if the DataType can't validate the provided input
#
# @ingroup exception
#
class DataTypeValidationException(Exception):
    pass

## @brief DataType is the base type definied in the prestans model chain
#
class DataType(object):
    
    ## @brief Base validate method, must be overridden by all implementing types
    #
    # @throws DataTypeValidationException string representation includes validation failure reason
    #
    # @param self The object pointer
    # @param value The value to validate
    #
    def validate(self, value):
        raise DataTypeValidationException(ERROR_MESSAGE.NO_DIRECT_USE % "prestans.types.DataType")

## @brief Wrappers on Python types generally represented as structures e.g DateTime
#
#  as_serializable methods signature for %DataStructure is different to that of DataCollection
#  it requires a value to be passed in, this is because the python type of structures is 
#  difference to what gets serialized.
#
#  E.g DateTime serializes itself as a ISO string
#
class DataStructure(DataType):
    
    ## @brief serializes values based on the rules
    #
    def as_serializable(self, value):
        raise DataTypeValidationException(ERROR_MESSAGE.NO_DIRECT_USE % "prestans.types.DataStructure")

## @brief represents a Type that has attributes in it like Arrays and Models
#    
class DataCollection(DataType):

    ## @brief Base validate method, must be overridden by all implementing types
    #
    # @throws DataTypeValidationException string representation includes validation failure reason
    #
    # @param self The object pointer
    # @param value The value to validate
    # @param attribute_filter attribute filter to use while 
    #
    def validate(self, value, attribute_filter=None):
        raise DataTypeValidationException(ERROR_MESSAGE.NO_DIRECT_USE % "prestans.types.DataType")

    ## @brief serializes values based on the rules
    #
    # DataCollection serializers should accept 
    #
    def as_serializable(self, attribute_filter=None):
        raise DataTypeValidationException(ERROR_MESSAGE.NO_DIRECT_USE % "prestans.types.DataCollection")

    ## @brief returns an AttributeFilter representation of an instance
    #
    def get_attribute_filter(self):
        raise DataTypeValidationException(ERROR_MESSAGE.NO_DIRECT_USE % "prestans.types.DataCollection")


     
## @brief wrapper for Python String types
#   
class String(DataType):
    
    ## @brief instantiates a String type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param min_length the lowest value this Integer can have
    #  @param max_length the highest value a Integer can have
    #  @param required marks that this field must have a value, also see default
    #  @param format is a regular expression that can be used to validate strings
    #  @param choices restrict the acceptable values to this list
    #  @param utf_encoding set to utf-8 for unicode input
    #
    def __init__(self, 
                 default=None, 
                 min_length=None, 
                 max_length=None, 
                 required=True, 
                 format=None, 
                 choices=None, 
                 utf_encoding='utf-8'):

        if min_length and max_length and min_length > max_length:
            raise InvalidMetadata(ERROR_MESSAGE.INVALID_META_VALUE % ('min_length', self.__class__.__name__))
        if required and min_length and min_length < 1:
            """ If String is required, min_length has to be one, this is a configuration time problem not runtime """
            raise InvalidMetadata(ERROR_MESSAGE.INVALID_META_VALUE % ('min_length', self.__class__.__name__))
            
        self._default = default
        self._min_length = min_length
        self._max_length = max_length
        self._required = required
        self._format = format
        self._choices = choices
        self._utf_encoding = utf_encoding
        
    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "string"

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

    ## @brief String specific validation rules
    #
    def validate(self, value):
        
        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            """ Encode the String is presented with Unicode """
            if isinstance(value, unicode):
                final_value = str(value.encode(self._utf_encoding))
            else:
                final_value = str(value)
        except:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, 'String'))  
        
        if not self._required and len(final_value) == 0:
            """ Check for a zero length string which is valid for not required """
            return final_value
        
        if final_value is not None and self._min_length and len(final_value) < self._min_length:
            """ Verify that the parsed value is acceptable """ 
            raise DataTypeValidationException(ERROR_MESSAGE.LESS_THAN_MIN_LENGTH % self._min_length)
        if final_value is not None and self._max_length and len(final_value) > self._max_length:
            raise DataTypeValidationException(ERROR_MESSAGE.MORE_THAN_MAX_LENGTH % self._max_length)
            
        if self._choices is not None and not final_value in self._choices:
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_IN_CHOICES)
            
        if self._format is not None and re.search(self._format, final_value) is None:
            raise DataTypeValidationException(ERROR_MESSAGE.DOESNOT_MATCH_STRING_FORMAT % final_value)
        
        return final_value
    
    
## @brief wrapper for Python Float type
#
class Float(DataType):

    ## @brief instantiates a Integer type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param minimum the lowest value this Float can have
    #  @param maximum the highest value a Float can have
    #  @param required marks that this field must have a value, also see default
    #  @param choices restrict the acceptable values to this list
    # 
    def __init__(self, 
                 default=None, 
                 minimum=None, 
                 maximum=None, 
                 required=True, 
                 choices=None):
        
        if minimum and maximum and minimum > maximum:
            raise InvalidMetadata(ERROR_MESSAGE.INVALID_META_VALUE % ('minimum', self.__class__.__name__))
        
        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices

    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "float"

        return blueprint
        
        constraints = dict()
        constraints['default'] = self._default
        constraints['minimum'] = self._minimum
        constraints['maximum'] = self._maximum
        constraints['required'] = self._required
        constraints['choices'] = self._choices

        blueprint['constraints'] = constraints
        return blueprint
        
    ## @brief Float specific validation rules
    #
    def validate(self, value):
        
        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            """ Attempt to parse the value as a Float """
            final_value = float(value)
        except:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, 'Float'))   
        
        if final_value and self._minimum is not None and final_value < self._minimum:
            """ Verify that the parsed value is acceptable """
            raise DataTypeValidationException(ERROR_MESSAGE.LESS_THAN_MINIMUM % self._minimum)
        if final_value and self._maximum is not None and final_value > self._maximum:
            raise DataTypeValidationException(ERROR_MESSAGE.MORE_THAN_MAXIMUM % self._maxmium)
            
        if self._choices is not None and not final_value in self._choices:
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_IN_CHOICES)
        
        return final_value    
        

## @brief wrapper for Python Integer
#    
class Integer(DataType):

    ## @brief instantiates a Integer type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param minimum the lowest value this Integer can have
    #  @param maximum the highest value a Integer can have
    #  @param required marks that this field must have a value, also see default
    #  @param choices restrict the acceptable values to this list
    # 
    def __init__(self, 
                 default=None, 
                 minimum=None, 
                 maximum=None, 
                 required=True, 
                 choices=None):

        if minimum and maximum and minimum > maximum:
            raise InvalidMetadata(ERROR_MESSAGE.INVALID_META_VALUE % ('minimum', self.__class__.__name__))

        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._required = required
        self._choices = choices

    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "int"

        constraints = dict()
        constraints['default'] = self._default
        constraints['minimum'] = self._minimum
        constraints['maximum'] = self._maximum
        constraints['required'] = self._required
        constraints['choices'] = self._choices

        blueprint['constraints'] = constraints
        return blueprint

    ## @brief Integer specific validation rules
    #
    def validate(self, value):

        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            """ Attempt to parse the value as an Integer """
            final_value = int(value)
        except:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, 'Integer')) 
        
        if final_value and self._minimum is not None and final_value < self._minimum:
            """ Verify that the parsed value is acceptable """
            raise DataTypeValidationException(ERROR_MESSAGE.LESS_THAN_MINIMUM % self._minimum)
        if final_value and self._maximum is not None and final_value > self._maximum:
            raise DataTypeValidationException(ERROR_MESSAGE.MORE_THAN_MAXIMUM % self._maximum)
            
        if self._choices is not None and not final_value in self._choices:
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_IN_CHOICES)
        
        return final_value
 
## @brief wrapper for Python Booleans
#   
class Boolean(DataType):


    ## @brief instantiates a Integer type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param required marks that this field must have a value, also see default
    # 
    def __init__(self, 
                 default=None, 
                 required=True):

        self._default = default
        self._required = required

    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "bool"

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required

        blueprint['constraints'] = constraints
        return blueprint
    
    ## @brief Boolean specific validation
    #
    def validate(self, value):

        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            value = self._default
        
        try:
            """ Attempt to parse the value as a Boolean """
            final_value = bool(value)
        except: 
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, 'Boolean'))
        
        return final_value

## @brief Accepts a Fileupload as part of the JSON body using FileReader's readAsDataURL
#
#  @param required
#  @param validate
#
#  readAsDataURL, encodes the contents of the file as a DataURLScheme, 
#  http://en.wikipedia.org/wiki/Data_URI_scheme
# 
#  Example
#  http://www.html5rocks.com/en/tutorials/file/dndfiles/
#
#  Meta information about the file upload is upto the implementing application
#
class DataURLFile(DataType):

    @classmethod
    def generate_filename(cls):
        return uuid.uuid4().hex

    ## @brief instantiates a field to support FileReader uploaded base64 encoded contents
    #
    def __init__(self, 
                 required=True, 
                 allowed_mime_types=[]):

        self._required = required
        self._allowed_mime_types = allowed_mime_types

        # If provided mime type is a string then wrap it into an array
        if isinstance(allowed_mime_types, str):
            self._allowed_mime_types = [allowed_mime_types]

        # Set by validate
        self._mime_type = None
        self._file_contents = None


    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "data_url_file"

        constraints = dict()
        constraints['required'] = self._required
        constraints['allowed_mime_types'] = self._allowed_mime_types

        blueprint['constraints'] = constraints
        return blueprint

    ## @brief validates a file upload
    #
    #  There are no default values for file upload, files can be not required
    #
    def validate(self, value):

        final_value = self.__class__()

        #Check conditions for a required parameter
        if self._required and value is None:
            import logging
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)

        #Check for not required starting condition and return before unpack takes place
        if self._required is False and value is None:
            return value

        #Try to unpack the data value
        try:
            
            data_url, delimiter, base64_content = value.partition(',')
            final_value._mime_type = data_url.replace(';base64', '').replace('data:', '')
            final_value._file_contents = base64.b64decode(base64_content)
        
        except Exception, err:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % ("Sized " + str(len(value)), "DataURLFile"))

        #Abort if the provided mime type is not acceptable
        if self._allowed_mime_types and len(self._allowed_mime_types) > 0 and not final_value._mime_type in self._allowed_mime_types:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % ("%s not an acceptable mime type" % final_value._mime_type, "DataURLFile"))

        return final_value

    ## @brief writes file to a particular location
    #
    #  This won't work for cloud environments like Google's Appengine, use with caution
    #  ensure to catch exceptions so you can provide informed feedback.
    #
    #  prestans does not mask File IO exceptions so your handler can respond better.
    #
    def save(self, path):
        
        file_handle = open(path, 'wb')
        file_handle.write(self._file_contents)
        file_handle.close()

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def file_contents(self):
        return self._file_contents


## @brief wrapper for Python datetime with format based parsing
#   
class DateTime(DataStructure):

    ## @brief instantiates a Integer type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param required marks that this field must have a value, also see default
    #  @param format is the Date Time Format string, defaults to RFC822
    # 
    def __init__(self, 
                 default=None, 
                 required=True, 
                 format="%Y-%m-%d %H:%M:%S"):

        self._default = default
        self._required = required
        self._format = format


    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "datetime"

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format

        blueprint['constraints'] = constraints
        return blueprint

    ## @brief DateTime Validator
    #
    def validate(self, value):
        
        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            """ Check to see if NOW """
            if self._default == CONSTANT.DATETIME_NOW:
                value = datetime.now()
            else:
                value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            if self._default == CONSTANT.DATETIME_NOW:
                value = datetime.now()
            else:
                value = self._default
        
        if type(value) == datetime:
            """ If it's a datetime then pass it through """
            final_value = value
        elif type(value) == str or type(value) == unicode:
            """ If its a string we need to parse it """
            try:
                final_value = datetime.strptime(value, self._format)
            except ValueError, e:
                raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, "DateTime"))
        else:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, "DateTime"))
            
        return final_value

    ## @brief serializes a datetime.datetime object into a String
    #
    def as_serializable(self, value):

        if not type(value) == datetime:
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_TYPE % (value, 'datetime.datetime'))
            
        return value.strftime(self._format)


## @brief wrapper for Python date with format based parsing
#   
class Date(DataStructure):

    ## @brief instantiates a Date type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param required marks that this field must have a value, also see default
    #  @param format is the Date Format string, defaults to RFC822
    # 
    def __init__(self, 
                 default=None, 
                 required=True, 
                 format="%Y-%m-%d"):

        self._default = default
        self._required = required
        self._format = format


    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "date"

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format

        blueprint['constraints'] = constraints
        return blueprint

    ## @brief DateTime Validator
    #
    def validate(self, value):
        
        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            """ Check to see if NOW """
            if self._default == CONSTANT.DATE_TODAY:
                value = date.today()
            else:
                value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            if self._default == CONSTANT.DATE_TODAY:
                value = date.today()
            else:
                value = self._default
        
        if type(value) == date:
            """ If it's a date then pass it through """
            final_value = value
        elif type(value) == str or type(value) == unicode:
            """ If its a string we need to parse it """
            try:
                final_value = datetime.strptime(value, self._format).date()
            except ValueError, e:
                raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, "Date"))
        else:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, "Date"))
            
        return final_value

    ## @brief serializes a datetime.date object into a String
    #
    def as_serializable(self, value):

        if not type(value) == date:
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_TYPE % (value, 'datetime.date'))
            
        return value.strftime(self._format)

# @brief wrapper for Python date with format based parsing
#   
class Time(DataStructure):

    ## @brief instantiates a Time type or a Meta definition 
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param required marks that this field must have a value, also see default
    #  @param format is the Time Format string, defaults to RFC822
    # 
    def __init__(self, 
                 default=None, 
                 required=True, 
                 format="%H:%M:%S"):

        self._default = default
        self._required = required
        self._format = format


    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "time"

        constraints = dict()
        constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['format'] = self._format

        blueprint['constraints'] = constraints
        return blueprint

    ## @brief Time Validator
    #
    def validate(self, value):

        final_value = None
        
        if self._required and self._default is None and value is None:
            """ Check conditions for a required parameter """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
        elif self._required and value is None:
            """ Check to see if NOW """
            if self._default == CONSTANT.TIME_NOW:
                value = time.today()
            else:
                value = self._default
        elif not self._required and self._default is None and value is None:
            """ Check conditions for a non-required parameter """
            return final_value
        elif not self._required and value is None:
            if self._default == CONSTANT.TIME_NOW:
                value = time.today()
            else:
                value = self._default
        
        if type(value) == time:
            """ If it's a time then pass it through """
            final_value = value
        elif type(value) == str or type(value) == unicode:
            """ If its a string we need to parse it """
            try:
                final_value = datetime.strptime(value, self._format).time()
            except ValueError, e:
                raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, "Time"))
        else:
            raise DataTypeValidationException(ERROR_MESSAGE.CANT_PARSE_VALUE % (value, "Time"))

        return final_value

    ## @brief serializes a datetime.time object into a String
    #
    def as_serializable(self, value):

        if not type(value) == time:
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_TYPE % (value, 'datetime.time'))
            
        return value.strftime(self._format)
    
## @brief collection of prestans types
#
class Array(DataCollection):

    ## @brief Constructor
    #
    #  @param default provides a default value for your type, used if one is not provided
    #  @param required marks that this field must have a value, also see default
    #  @param element_template specifies the model class of elements inside this array
    #  @param min_length the least amount of elements that this array can have
    #  @param max_length the most amount of elements that this array can have
    #
    def __init__(self, 
                 default=None, 
                 required=True, 
                 element_template=None, 
                 min_length=None, 
                 max_length=None):
        
        self._default = default
        self._required = required
        self._element_template = element_template
        self._min_length = min_length
        self._max_length = max_length
        
        self._array_elements = []

    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "array"

        constraints = dict()
        # constraints['default'] = self._default
        constraints['required'] = self._required
        constraints['min_length'] = self._min_length
        constraints['max_length'] = self._max_length
        constraints['element_template'] = self._element_template.blueprint()

        blueprint['constraints'] = constraints
        return blueprint


    ## @brief Setter for element template
    #
    def set_element_template(self, element_template):
        self._element_template = element_template
        
    ## @brief Validate method for %Array, validated elements against template
    #
    #  @param self The object pointer
    #  @param value The value to validate
    #  @param attribute_filter attribute filter to use while 
    # 
    def validate(self, value, attribute_filter=None):
        
        if not self._required and not value:
            return None

        final_value = self.__class__(element_template=self._element_template, 
                                     min_length=self._min_length, 
                                     max_length=self._max_length)
        
        if not isinstance(value, (list, tuple)):
            """ See if parsed data is infact an array otherwise raise the expcetion """
            raise DataTypeValidationException(ERROR_MESSAGE.NOT_ITERABLE)
            
        for array_element in value:
    
            """ Use validated element to parse attribute and store it in the array """
            if issubclass(self._element_template.__class__, DataCollection):
                """ If Model or Array, pass the attribute_filter along """
                validated_array_element = self._element_template.validate(array_element, attribute_filter)
            else:
                validated_array_element = self._element_template.validate(array_element)
    
            final_value.append(validated_array_element)
    
        if self._min_length is not None and len(final_value) < self._min_length:
            raise DataTypeValidationException(ERROR_MESSAGE.LESS_THAN_MIN_LENGTH % 
                                              self._min_length)

        if self._max_length is not None and len(final_value) > self._max_length:
            raise DataTypeValidationException(ERROR_MESSAGE.MORE_THAN_MAX_LENGTH % 
                                              self._max_length)

        return final_value
    

    ## @brief Mimics array like functionality to append element, runs validate before it appends
    #
    def append(self, value):
        
        if isinstance(value, (list, tuple)):

            """ Support adding arrays, return once we have looped through """
            for element in value:
                self.append(element)
            return
        
        if isinstance(self._element_template.__class__, String.__class__) and \
        isinstance(value, str):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, String.__class__) and \
        isinstance(value, unicode):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, Integer.__class__) and \
        isinstance(value, int):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, Float.__class__) and \
        isinstance(value, float):
            value = self._element_template.__class__().validate(value)
        elif isinstance(self._element_template.__class__, Boolean.__class__) and \
        isinstance(value, bool):
            value = self._element_template.__class__().validate(value)
        elif not isinstance(value, self._element_template.__class__):
            raise TypeError(ERROR_MESSAGE.ARRAY_TYPE_ERROR % 
                            (self._element_template.__class__.__name__, value.__class__.__name__))
        
        self._array_elements.append(value)
        
    ## @brief Wrapper for array remove function
    #
    def remove(self, value):
        self._array_elements.remove(value)
    
    ## @brief Wrapper for array length function
    #   
    def __len__(self):
        return len(self._array_elements)
        
    ## @brief Iterator for array
    #
    #  @param self The object pointer
    #
    #  With a little help from 
    #  http://johnmc.co/llum/the-easiest-way-to-implement-__iter__-for-a-python-object/
    #
    def __iter__(self):
        for element in self._array_elements:
            yield element
    
    ## @brief Generate a python representation of object
    #
    #  @param self The object pointer
    #  @param attribute_filter filter to use while serializing output
    #
    def as_serializable(self, attribute_filter=None):
        
        result_array = list()
            
        for array_element in self._array_elements:
        
            if isinstance(array_element, str) or \
            isinstance(array_element, unicode) or \
            isinstance(array_element, float) or \
            isinstance(array_element, int) or \
            isinstance(array_element, bool):

                result_array.append(array_element)
            else:
                result_array.append(array_element.as_serializable(attribute_filter))
        
        return result_array
        
    ## @brief override fetch for by index, wrapper for internal array
    #
    def __getitem__(self, index):
        return self._array_elements[index]

    ## @brief returns a dictionary representation for the element_template
    #
    def get_attribute_filter(self, default_value=False):

        attribute_filter = None

        if issubclass(self._element_template.__class__, DataCollection):
            attribute_filter = self._element_template.get_attribute_filter(default_value)
        elif issubclass(self._element_template.__class__, DataType) or \
            issubclass(self._element_template.__class__, DataStructure):
            attribute_filter = default_value

        return attribute_filter


## @brief Models are complex structures made up of existing base data types
#
#  Models details the relationships between properties in the parsed data.
#
#  If the parse fails, the handler request handler must respond with an appropriate 
#  error code. On success the parsed data is then provided to the REST request handler.
#
#  Unlike basic types Models do not use the _data_type_value instance variable keep
#  track of the parsed value, values are copied into the instance. The class __dict__
#  is used as a template.
#   
class Model(DataCollection):

    ## @brief Constructor
    #
    #  If you are using the Model constructor to provide Meta data, you can provide it
    #  a default dictionary to initialise instance to initalise it from
    #
    #  Can run _create_instance_attributes to copy attribute tempaltes to the instance,
    #  Model instances do not have any configurable options.
    #
    #  @param required whether or not this model is required when used as an attribute
    #  @param default provides a default value for your type, used if one is not provided
    #  @param kwargs Named parameters of which to instantiate the model with
    #
    def __init__(self, 
                 required=True, 
                 default=None, 
                 **kwargs):
        
        self._required = required
        self._default = default
        
        self._create_instance_attributes(kwargs)

    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "%s.%s" % (self.__module__, self.__class__.__name__)

        constraints = dict()
        constraints['required'] = self._required
        blueprint['constraints'] = constraints

        # Fields
        fields = dict()
        model_class_members = inspect.getmembers(self.__class__)
    
        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                """ Ignore parameters with __ and if they are methods """
                continue

            if not issubclass(type_instance.__class__, DataType):
                """ All attributes in the Model class must be of type DataType """
                raise DataTypeValidationException(ERROR_MESSAGE.NOT_SUBCLASS % (attribute_name, "prestans.types.DataType"))

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint    
        
    ## @brief returns a list of managed attributes for the Model class
    #
    #  Implemented for use with data adapters, can be used to quickly make a list of the 
    #  attribute names in a prestans model
    #
    def get_attribute_keys(self):

        attribute_keys = []
        
        model_class_members = inspect.getmembers(self.__class__)
        
        for attribute_name, type_instance in model_class_members:
            
            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                """ Ignore parameters with __ and if they are methods """
                continue
            
            if issubclass(type_instance.__class__, DataType):
                """ All acceptable types are a subclass of DataType """
                attribute_keys.append(attribute_name)
            
        return attribute_keys

    ## @brief validates a method for %Model
    #
    #  @return Instance of the %Model subclass with instance variables
    # 
    #  @param self The object pointer
    #  @param value The value to validate
    #
    def validate(self, value, attribute_filter=None):
        
        if self._required and (value is None or not isinstance(value, dict)):
            """ Model level validation requires a parsed dictionary, this is done by the serializer """
            raise DataTypeValidationException(ERROR_MESSAGE.REQUIRED_PARAMETER_MISSING)
            
        if not value and self._default:
            """ If no value provided but a default model instance was provided """
            return self._default
            
        if not self._required and not value:
            """ Value was not provided by caller, but require a template """
            return None
            
        model_instance = self.__class__()
    
        model_class_members = inspect.getmembers(self.__class__)
    
        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                """ Ignore parameters with __ and if they are methods """
                continue

            if attribute_filter and not attribute_filter.is_attribute_visible(attribute_name):
                """ Attribute not visible, ensure you do this before the check non existant attributes """
                model_instance.__dict__[attribute_name] = None
                continue

            if not issubclass(type_instance.__class__, DataType):
                """ All attributes in the Model class must be of type DataType """
                raise DataTypeValidationException(ERROR_MESSAGE.NOT_SUBCLASS % (attribute_name, "prestans.types.DataType"))

            validation_input = None
            
            if value.has_key(attribute_name):
                validation_input = value[attribute_name]
                
            try:
                
                """ Try and validate the attribute in quesiton, this may be recursive """
                if issubclass(type_instance.__class__, DataCollection):
                    """ Pass on the attribute filter if this is a collection """
                    sub_attribute_filter = None
                    if attribute_filter and attribute_filter.has_key(attribute_name):
                        sub_attribute_filter = getattr(attribute_filter, attribute_name)
                        
                    validated_object = type_instance.validate(validation_input, sub_attribute_filter)
                else:
                    validated_object = type_instance.validate(validation_input)
                """ If successful then set the attribute instance with the parsed value """
                
                model_instance.__dict__[attribute_name] = validated_object
                    
            except DataTypeValidationException, exp:
                """ Raises this exception if data validation fails, with a meaningful message """
                raise DataTypeValidationException('Attribute %s, %s' % (attribute_name, str(exp)))

        return model_instance

    ## @brief genrates an %AttributeFilter version of itself
    #
    #  @param default_value is set to False, this means by default attributed are invisible
    #         set this to True if you want to show them by default
    #
    #  By default this includes sub models, arrays are serialized down to 
    #  %AttributeFilter instances of elements in a each element template
    #
    def get_attribute_filter(self, default_value=False):

        attribute_filter = prestans.parsers.AttributeFilter()

        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                """ Ignore parameters with __ and if they are methods """
                continue

            if issubclass(type_instance.__class__, DataCollection):
                """ Returns the fields for an instance only """
                setattr(attribute_filter, attribute_name, type_instance.get_attribute_filter(default_value))
            else:
                setattr(attribute_filter, attribute_name, default_value)

        return attribute_filter

        
    ## @brief Generate a pure python representation of object which is serializable
    #
    #  @param self The object pointer
    #  @param attribute_filter filter to use while serializing output
    #
    def as_serializable(self, attribute_filter=None):
        
        model_dictionary = dict()
        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:
            
            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                """ Ignore parameters with __ and if they are methods """
                continue

            if isinstance(attribute_filter, prestans.parsers.AttributeFilter) and not attribute_filter.is_attribute_visible(attribute_name):
                """ Attribute not visible, ensure you do this before the check non existant attributes """
                continue

            if not self.__dict__.has_key(attribute_name) or self.__dict__[attribute_name] is None:
                """ attribute_name should exist in the class level dictionary """
                model_dictionary[attribute_name] = None
                continue

            """ Check to see if the property is visible in this context """
            if issubclass(type_instance.__class__, DataCollection):

                sub_attribute_filter = None
                if isinstance(attribute_filter, prestans.parsers.AttributeFilter) and attribute_filter.has_key(attribute_name):
                    """ Check to see if there's a sub attribute """
                    sub_attribute_filter = getattr(attribute_filter, attribute_name)

                """ Added exception for DateTime to be treated as a complex type when serializing """
                model_dictionary[attribute_name] = self.__dict__[attribute_name].as_serializable(sub_attribute_filter)

            elif issubclass(type_instance.__class__, DataStructure):
                """ Get a Python value form the model """
                python_value = self.__dict__[attribute_name]
                """ Get a handle to the DataType definition """
                """ Use the as_serialize method """
                serializable_value = type_instance.as_serializable(python_value)
                """ Add that to the dictionary """
                model_dictionary[attribute_name] = serializable_value

            else:
                """ Do this in else, because everything is a sub class of DataType """
                model_dictionary[attribute_name] = self.__dict__[attribute_name]
        
        return model_dictionary
        
    ## @brief Overridden __setattr__ to ensure that users only set attributes defined in the model
    #
    #  @param key Attribute name
    #  @param value New Attribute value
    #
    def __setattr__(self, key, value):
        
        #Set internal fields
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
                #If the incoming object is a prestans data type, set it directly
                self.__dict__[key] = value
            else:
                #otherwise run the validate method to turn it into a prestans type
                self.__dict__[key] = validator.validate(value)
            
            return
            
        raise KeyError(ERROR_MESSAGE.NO_KEY % (key, self.__class__.__name__))
        
    
    ## @brief copies class level attribute templates and makes instance placeholders
    #
    #  This step is required for direct uses of Model classes. This creates a copy of attribute_names
    #  ignores methods and private variables. DataCollection types are deep copied to ignore memory
    #  reference conflicts.
    #
    #  DataType instances are initialized to None or default value.
    #
    def _create_instance_attributes(self, arguments):

        model_class_members = inspect.getmembers(self.__class__)

        for attribute_name, type_instance in model_class_members:

            #Ignore parameters with __ or if they are methods
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
                        """ If the argument_name exists in kwargs use that value instead of None to validate """
                        value = arguments[attribute_name]
                        
                    self.__dict__[attribute_name] = type_instance.validate(value)

                except DataTypeValidationException:
                    self.__dict__[attribute_name] = None
