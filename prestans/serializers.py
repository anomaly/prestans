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

import prestans.exceptions

class Serializer(object):
    """
    Base Serializer class, all implementation must inherit from this class and 
    override the methods defined in this class.

    The request parser will ensure that all serializer inherit from this class.

    If you serializer depends on a Python library to perform the Serialization,
    ensure you import those libraries in the loads and dumps methods
    """

    def loads(self, input_string):
        raise prestans.exceptions.DirectUserNotAllowed("loads", self.__class__.__name__)

    def dumps(self, serialzable_object):
        raise prestans.xceptions.DirectUserNotAllowed("dumps", self.__class__.__name__)

    def content_type(self):
        raise prestans.exceptions.DirectUserNotAllowed("content_type", self.__class__.__name__)


class JSON(Serializer):
    """
    Support for JSON, http://json.org

    JSON (JavaScript Object Notation) is a lightweight data-interchange format. 
    It is easy for humans to read and write. It is easy for machines to parse 
    and generate. It is based on a subset of the JavaScript Programming Language, 
    Standard ECMA-262 3rd Edition - December 1999. JSON is a text format that is 
    completely language independent but uses conventions that are familiar to 
    programmers of the C-family of languages, including C, C++, C#, Java, JavaScript, 
    Perl, Python, and many others. These properties make JSON an ideal 
    data-interchange language.
    """

    def loads(self, input_string):

        import json
        parsed_json = None

        try:
            parsed_json = json.loads(input_string)
        except Exception, exp:
            raise prestans.exceptions.SerializationFailed('JSON')
            
        return parsed_json
        
    def dumps(self, serialzable_object):
        
        import json
        return json.dumps(serializable_object)

    def content_type(self):
        return 'application/json'

