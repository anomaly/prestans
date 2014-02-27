# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2014, Eternity Technologies Pty Ltd.
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

__all__ = ['Serializer', 'JSON', 'XMLPlist']

import prestans.exception

class Base(object):

    def dumps(self, serializable_object):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def handler_body_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def content_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)


class TextSerializer(Base):

    def dumps(self, serializable_object):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def handler_body_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def content_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)


class BinarySerializer(Base):

    def dumps(self, serializable_object):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def handler_body_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def content_type(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)


class JSON(TextSerializer):

    def dumps(self, serializable_object):
        
        import json
        try:
            return json.dumps(serializable_object)
        except:
            raise prestans.exception.SerializationFailedError('JSON')

    def handler_body_type(self):
        return prestans.types.DataCollection

    def content_type(self):
        return 'application/json'


class XMLPlist(TextSerializer):
    """
    Uses Apple's Property List format to serialize collections 
    to XML. Refer to http://docs.python.org/2/library/plistlib.html
    """

    def dumps(self, serializable_object):

        import plistlib

        try:
            plist_str = plistlib.writePlistToString(serializable_object)
        except:
            raise prestans.exception.SerializationFailedError('XML')

        return plist_str

    def handler_body_type(self):
        return prestans.types.DataCollection

    def content_type(self):
        return 'application/xml'


class PDFSerializer(BinarySerializer):
    """
    Serializes HTML/CSS to PDF using WeasyPrint; http://weasyprint.org

    Handlers to use headers to set Content-Disposition header; to
    deliver files inline; or as an attacment with a filename

    headers = self.response.headers
    headers.add_header('Content-Disposition', 'attachment', filename="name")
    """

    def dumps(self, serializable_object):
        
        import StringIO
        from weasyprint import HTML, CSS

        output_stream = StringIO.StringIO()

        try:
            HTML(string=serializable_object).write_pdf(output_stream)

            output_string = output_stream.getvalue()
            output_stream.close()
        except:
            raise prestans.exception.SerializationFailedError('WeasyPrint/PDF')
            
        return output_string

    def handler_body_type(self):
        return str

    def content_type(self):
        return 'application/pdf'
