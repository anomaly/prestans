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

import unittest
import logging

import prestans.http
import prestans.rest

"""
class Handler(prestans.rest.RequestHandler):
    pass

get_request = {
    "REQUEST_METHOD": "GET",
    "SERVER_NAME": "localhost",
    "PATH_INFO": "/test",
    "wsgi.version": (1, 0),
    "wsgi.url_scheme" : "http"
}

def start_response(self, status, headers):
    pass

rest_application = prestans.rest.RequestRouter([
    ('/test', Handler)
], application_name="test-request-api", debug=True)
"""

class RequestUnitTest(unittest.TestCase):

    def setUp(self):
        
        logging.basicConfig()
        self.logger = logging.getLogger("prestans")

        deserializers=[prestans.deserializer.JSON()]
        self.default_deserializer=prestans.deserializer.JSON()

        self.get_request = prestans.rest.Request(
            environ={
                "REQUEST_METHOD": prestans.http.VERB.GET
            },
            charset="utf-8",
            logger=self.logger,
            deserializers=deserializers,
            default_deserializer=self.default_deserializer
        )

        self.post_request = prestans.rest.Request(
            environ={
                "REQUEST_METHOD": prestans.http.VERB.POST
            },
            charset="utf-8",
            logger=self.logger,
            deserializers=deserializers,
            default_deserializer=self.default_deserializer
        )

    def test_method(self):
        self.assertEqual(self.get_request.method, prestans.http.VERB.GET)
        self.assertEqual(self.post_request.method, prestans.http.VERB.POST)

    def test_logger(self):
        self.assertEqual(self.get_request.logger, self.logger)

    def test_default_deserializer(self):
        self.assertEqual(self.get_request.default_deserializer, self.default_deserializer)
        self.assertEqual(self.get_request.default_deserializer, self.default_deserializer)

    def tearDown(self):
        pass
