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


class RESTRequestMethod(unittest.TestCase):
    def test_get(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.GET},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.GET)

    def test_head(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.HEAD},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.HEAD)

    def test_post(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.POST)

    def test_put(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.PUT},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.PUT)

    def test_patch(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.PATCH},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.PATCH)

    def test_delete(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.DELETE},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertEquals(request.method, VERB.DELETE)

    def test_options(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.OPTIONS},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertEquals(request.method, VERB.OPTIONS)


class RESTRequestLogger(unittest.TestCase):
    def test_logger_passed_via_init(self):
        custom_logger = logging.getLogger("custom")
        request = Request(
            environ={"REQUEST_METHOD": VERB.GET},
            charset="utf-8",
            logger=custom_logger,
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertEquals(request.logger, custom_logger)


class RESTRequestParsedBody(unittest.TestCase):
    def test_none_raises_attribute_error(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON],
            default_deserializer=JSON
        )
        self.assertRaises(AttributeError, getattr, request, "parsed_body")

    def test_get_body(self):
        request = Request(
            environ={
                "REQUEST_METHOD": VERB.POST,
                "CONTENT_TYPE": "application/json"
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )

        class Person(types.Model):
            first_name = types.String()
            last_name = types.String()

        request.body = b'{"first_name": "John", "last_name": "Smith"}'
        request.body_template = Person()
        self.assertTrue(isinstance(request.parsed_body, Person))
        self.assertEquals(request.parsed_body.first_name, "John")
        self.assertEquals(request.parsed_body.last_name, "Smith")


class RESTRequestSupportedMimeTypes(unittest.TestCase):
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


class RESTRequestSelectedDeserializer(unittest.TestCase):
    def test_selected_deserializer(self):
        request = Request(
            environ={"REQUEST_METHOD": VERB.POST},
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertIsNone(request.selected_deserializer)


class RESTRequestDefaultDeserializer(unittest.TestCase):
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


class RESTRequestSetDeserializerByMimeType(unittest.TestCase):
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


class RESTRequestAttributeFilter(unittest.TestCase):
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


class RESTRequestParameterSet(unittest.TestCase):
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


class RESTRequestBodyTemplate(unittest.TestCase):
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


class RESTRequestRegisterDeserializers(unittest.TestCase):
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


class RESTRequestGetResponseAttributeFilter(unittest.TestCase):

    def test_template_filter_none_returns_none(self):
        request = Request(
            environ={
                "REQUEST_METHOD": VERB.GET
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertIsNone(request.get_response_attribute_filter(template_filter=None))

    def test_header_not_found_returns_none(self):
        request = Request(
            environ={
                "REQUEST_METHOD": VERB.GET
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )
        self.assertIsNone(request.get_response_attribute_filter(template_filter=AttributeFilter()))

    def test_header_correctly_parsed(self):
        request = Request(
            environ={
                "REQUEST_METHOD": VERB.GET,
                "HTTP_PRESTANS_RESPONSE_ATTRIBUTE_LIST": '{"first_name": true, "last_name": false}'
            },
            charset="utf-8",
            logger=logging.getLogger(),
            deserializers=[JSON()],
            default_deserializer=JSON()
        )

        class Person(types.Model):
            first_name = types.String()
            last_name = types.String()

        response_filter = request.get_response_attribute_filter(template_filter=AttributeFilter.from_model(Person()))
        self.assertIsInstance(response_filter, AttributeFilter)
        self.assertTrue(response_filter.first_name)
        self.assertFalse(response_filter.last_name)


class RESTRequestIsMinified(unittest.TestCase):
    def test_default_false(self):
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

    def test_on_is_true(self):
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

    def test_off_is_false(self):
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
