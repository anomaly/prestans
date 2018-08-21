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
import base64

from prestans import exception
from prestans.types import DataStructure


class DataURLFile(DataStructure):
    """
    Accepts a Fileupload as part of the JSON body using FileReader's readAsDataURL

    readAsDataURL, encodes the contents of the file as a DataURLScheme,
    http://en.wikipedia.org/wiki/Data_URI_scheme

    Example
    http://www.html5rocks.com/en/tutorials/file/dndfiles/

    Meta information about the file upload is up to the implementing application
    """

    @classmethod
    def generate_filename(cls):
        import uuid
        return uuid.uuid4().hex

    def __init__(self, required=True, allowed_mime_types=None, description=None):

        if allowed_mime_types is None:
            allowed_mime_types = []
        elif isinstance(allowed_mime_types, str):
            allowed_mime_types = [allowed_mime_types]

        self._required = required
        self._allowed_mime_types = allowed_mime_types
        self._description = description

        self._mime_type = None
        self._file_contents = None

    @property
    def required(self):
        return self._required

    @property
    def allowed_mime_types(self):
        return self._allowed_mime_types

    @property
    def description(self):
        return self._description

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
            raise exception.RequiredAttributeError()

        if self._required is False and value is None:
            return value

        try:
            data_url, delimiter, base64_content = value.partition(',')
            _validated_value._mime_type = data_url.replace(';base64', '').replace('data:', '')
            _validated_value._file_contents = base64.b64decode(base64_content)
        except Exception as exp:
            raise exception.ParseFailedError("data url file encoding failed %s" % exp)

        if self._allowed_mime_types and len(self._allowed_mime_types) > 0 \
           and _validated_value._mime_type not in self._allowed_mime_types:
            raise exception.InvalidChoiceError(_validated_value._mime_type, self._allowed_mime_types)

        return _validated_value

    def save(self, path):
        """
        Writes file to a particular location

        This won't work for cloud environments like Google's App Engine, use with caution
        ensure to catch exceptions so you can provide informed feedback.

        prestans does not mask File IO exceptions so your handler can respond better.
        """

        file_handle = open(path, 'wb')
        file_handle.write(self._file_contents)
        file_handle.close()

    def as_serializable(self, value):
        #: This is passed in a DataURLFile and we construct a String back from it
        return "data:%s;base64,%s" % (value.mime_type, value.base64_contents.decode("utf-8"))
