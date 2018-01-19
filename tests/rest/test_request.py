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
import logging
import unittest

from prestans.deserializer import JSON
from prestans.deserializer import XMLPlist
from prestans import exception
from prestans.http import VERB
from prestans.parser import AttributeFilter
from prestans.parser import ParameterSet
from prestans.rest import Request
from prestans import types


class RESTRequestTest(unittest.TestCase):
    def test_method(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.GET},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.GET)

        request = Request(
            environ={"REQUEST_METHOD": VERB.HEAD},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.HEAD)

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.POST)

        request = Request(
            environ={"REQUEST_METHOD": VERB.PUT},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.PUT)

        request = Request(
            environ={"REQUEST_METHOD": VERB.PATCH},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.PATCH)

        request = Request(
            environ={"REQUEST_METHOD": VERB.DELETE},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.DELETE)

        request = Request(
            environ={"REQUEST_METHOD": VERB.OPTIONS},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.OPTIONS)

    def test_logger(self):
        custom_logger = logging.getLogger("custom")
        request = Request(
            environ={"REQUEST_METHOD": VERB.GET},
            charset="utf-8",
            logger=custom_logger,
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.logger, custom_logger)

    def test_parsed_body(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertRaises(AttributeError, getattr, request, "parsed_body")

    def test_supported_mime_types(self):
        json_dsz = JSON()
        plist_dsz = XMLPlist()

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz],
            default_deserializer=json_dsz
        )
        self.assertEquals(request.supported_mime_types, [json_dsz.content_type()])

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz, plist_dsz],
            default_deserializer=json_dsz
        )
        self.assertEquals(request.supported_mime_types, [json_dsz.content_type(), plist_dsz.content_type()])

    def test_supported_mime_types_str(self):
        json_dsz = JSON()
        plist_dsz = XMLPlist()

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz],
            default_deserializer=json_dsz
        )
        self.assertEquals(request.supported_mime_types_str, json_dsz.content_type())

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz, plist_dsz],
            default_deserializer=json_dsz
        )
        self.assertEquals(request.supported_mime_types_str, json_dsz.content_type()+","+plist_dsz.content_type())

    def test_selected_deserializer(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertIsNone(request.selected_deserializer)

    def test_default_deserializer(self):
        json_dsz = JSON()

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz],
            default_deserializer=json_dsz
        )
        self.assertEquals(request.default_deserializer, json_dsz)

    def test_set_deserializer_by_mime_type(self):
        json_dsz = JSON()
        plist_dsz = XMLPlist()

        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz, plist_dsz],
            default_deserializer=json_dsz
        )
        self.assertIsNone(request.selected_deserializer)
        request.set_deserializer_by_mime_type("application/json")
        self.assertEquals(request.selected_deserializer, json_dsz)
        request.set_deserializer_by_mime_type("application/xml")
        self.assertEquals(request.selected_deserializer, plist_dsz)
        self.assertRaises(exception.UnsupportedContentTypeError, request.set_deserializer_by_mime_type, "text/plain")

    def test_attribute_filter(self):
        attribute_filter = AttributeFilter()
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        request.attribute_filter = attribute_filter
        self.assertEquals(request.attribute_filter, attribute_filter)

    def test_parameter_set(self):
        parameter_set = ParameterSet()
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        request.parameter_set = parameter_set
        self.assertEquals(request.parameter_set, parameter_set)

    def test_body_template(self):
        class Login(types.Model):
            email = types.String()
            password = types.String()

        # check that GET request raises exception if body template is attempted to be set
        get_request = Request(
            environ={
                "REQUEST_METHOD": VERB.GET
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertRaises(AssertionError, setattr, get_request, "body_template", Login())

        # check that None is ignored when setting body template
        post_request = Request(
            environ={
                "REQUEST_METHOD": VERB.POST
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        post_request.body_template = None
        self.assertIsNone(post_request.body_template)

        # check that exception raised for non DataCollection sub class
        self.assertRaises(AssertionError, setattr, post_request, "body_template", "string")

    def test_register_deserializers(self):
        json_dsz = JSON()
        plist_dsz = XMLPlist()

        request = Request(
            environ={
                "REQUEST_METHOD": VERB.POST
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[json_dsz],
            default_deserializer=json_dsz
        )
        self.assertEquals(request.supported_mime_types, ["application/json"])
        request.register_deserializers(plist_dsz)
        self.assertEquals(request.supported_mime_types, ["application/json", "application/xml"])

        self.assertRaises(TypeError, request.register_deserializers, "string")

    def test_get_response_attribute_filter(self):
        pass

    def test_is_minified(self):
        is_minified_missing = Request(
            environ={
                "REQUEST_METHOD": VERB.POST
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertFalse(is_minified_missing.is_minified)

        is_minified_on = Request(
            environ={
                "REQUEST_METHOD": VERB.POST,
                "HTTP_PRESTANS_MINIFICATION": "ON"
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertTrue(is_minified_on.is_minified)

        is_minified_off = Request(
            environ={
                "REQUEST_METHOD": VERB.POST,
                "HTTP_PRESTANS_MINIFICATION": "OFF"
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertFalse(is_minified_off.is_minified)
