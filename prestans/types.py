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
import exceptions
import copy
import re
import os
import base64
import uuid

from datetime import datetime
from datetime import date
from datetime import time

import .parsers


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


     