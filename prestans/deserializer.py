# -*- coding: utf-8 -*-
#
#  prestans, A WSGI compliant REST micro-framework
#  http://prestans.org
#
#  Copyright (c) 2015, Anomaly Software Pty Ltd.
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

__all__ = ['DeSerializer', 'JSON', 'XMLPlist']

import prestans.exception

class Base(object):

    def loads(self, input_string):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def content_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)


class JSON(Base):

    def loads(self, input_string):

        import json
        parsed_json = None

        try:
            parsed_json = json.loads(input_string)
        except Exception, exp:
            raise prestans.exception.DeSerializationFailedError('JSON')
            
        return parsed_json
        
    def content_type(self):
        return 'application/json'


class XMLPlist(Base):

    def loads(self, input_string):
        
        import plistlib
        unserialized_plist = None

        try:
            unserialized_plist = plistlib.readPlistFromString(input_string)
        except Exception, exp:
            raise prestans.exception.DeSerializationFailedError("XML/Plist")

        return unserialized_plist

    def content_type(self):
        return 'application/xml'
        