# -*- coding: utf-8 -*-
#!/usr/bin/env python
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

import inspect
import copy
import re
import os
import base64
import uuid

from datetime import datetime
from datetime import date
from datetime import time

import prestans.parsers
import prestans.exceptions

#:
#: Base type classes
#: 

class DataType(object):
    
    def validate(self, value):
        raise exceptions.DirectUserNotAllowed("validate", self.__class__.__name__)

class DataStructure(DataType):
    """
    Wrappers on Python types generally represented as structures e.g DateTime

    as_serializable methods signature for %DataStructure is different to that of DataCollection
    it requires a value to be passed in, this is because the python type of structures is 
    difference to what gets serialized.

    E.g DateTime serializes itself as a ISO string
    """
    
    def as_serializable(self, value):
        raise prestans.exceptions.DirectUseNotAllowed("as_serializable", self.__class__.__name__)

class DataCollection(DataType):

    def validate(self, value, attribute_filter=None):
        raise prestans.exceptions.DirectUseNotAllowed("validate", self.__class__.__name__)

    def as_serializable(self, attribute_filter=None):
        raise prestans.exceptions.DirectUseNotAllowed("as_serializable", self.__class__.__name__)

    def get_attribute_filter(self):
        raise prestans.exceptions.DirectUseNotAllowed("get_attribute_fitler", self.__class__.__name__)

#:
#: Basic Types
#:

class String(DataType):
    
     def __init__(self, 
                 default=None, 
                 min_length=None, 
                 max_length=None, 
                 required=True, 
                 format=None, 
                 choices=None, 
                 utf_encoding='utf-8'):

        
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

    def validate(self, value):
        pass

class Integer(DataType):

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

    def validate(self, value):
        pass

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

    def validate(self, value):
        pass

class Boolean(DataType):

    def __init__(self, 
                 default=None, 
                 required=True):


        self._default = default
        self._required = required

    def validate(self, value):
        pass

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

    def __init__(self, 
                 required=True, 
                 allowed_mime_types=[]):

        self._required = required
        self._allowed_mime_types = allowed_mime_types

        #:
        #: If provided mime type is a string then wrap it into an array
        #:
        if isinstance(allowed_mime_types, str):
            self._allowed_mime_types = [allowed_mime_types]

        #:
        #: Set by validate
        #:
        self._mime_type = None
        self._file_contents = None

    def validate(self, value):
        pass

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

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def file_contents(self):
        return self._file_contents        

#:
#: DataStructures
#:

class DateTime(DataStructure):
    pass

class Date(DataStructure):
    pass

class Time(DataStructure):
    pass

#:
#: Collections
#:

class Array(DataCollection):
    pass

#:
#: Models
#:
        
class Model(DataCollection):

    def __init__(self, required=True, default=None, **kwargs):

        self._required = required
        self._default = default