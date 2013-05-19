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


class DataType(object):
    """

    """
    
    def validate(self, value):
        """
            
        """
        raise exceptions.DirectUserNotAllowed("prestans.types.DataStructure")

class DataStructure(DataType):
    """
    Wrappers on Python types generally represented as structures e.g DateTime

    as_serializable methods signature for %DataStructure is different to that of DataCollection
    it requires a value to be passed in, this is because the python type of structures is 
    difference to what gets serialized.

    E.g DateTime serializes itself as a ISO string
    """
    
    def as_serializable(self, value):
        raise prestans.exceptions.DirectUserNotAllowed("prestans.types.DataStructure")

class DataCollection(DataType):

    def validate(self, value, attribute_filter=None):
        raise prestans.exceptions.DirectUserNotAllowed("prestans.types.DataCollection")

    def as_serializable(self, attribute_filter=None):
        raise prestans.exceptions.DirectUserNotAllowed("prestans.types.DataCollection")

    def get_attribute_filter(self):
        raise prestans.exceptions.DirectUserNotAllowed("prestans.types.DataCollection")
        