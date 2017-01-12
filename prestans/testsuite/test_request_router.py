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

import prestans.rest

LOGGER_MCLOGFACE = logging.Logger("temp", level='ERROR')
LOGGER_MCLOGFACE.disabled = 50  # silence the logger


class MyModel(prestans.types.Model):
    id = prestans.types.Integer()


class _UserHandler(prestans.rest.RequestHandler):
    __parser_config__ = prestans.parser.Config(
        GET=prestans.parser.VerbConfig(
            response_template=MyModel(),
            response_attribute_filter_default_value=True
        )
    )

    def get(self, id):
        model = MyModel()
        model.id = id
        self.response.body = model


class MockStartResponse:
    @classmethod
    def __call__(cls, status, response_headers, exc_info=None):
        pass


class RequestRouterTest(unittest.TestCase):
    def test_script_alias_match_with_global_match_group_should_not_pass_call(self):
        """
        WSGIScriptAliasMatch /mountpoint(.*) script.wsgi

        with router r"/mountpoint/some/path/([0-9]+"
        """

        expected_value = 123

        self._test_routing_behavour(environ={
            "REQUEST_METHOD": prestans.http.VERB.GET,
            "SCRIPT_NAME": "/mountpoint/some/path/{}".format(expected_value),
            "PATH_INFO": "",
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": None,  # shouldn't be called
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "1234"
        }, should_pass=False)

    def test_script_alias_match_with_match_group_should_pass_call(self):
        """
        WSGIScriptAliasMatch /mountpoint(.*) script.wsgi$1

        with router ``TestRequestRouter``
        :return:
        """
        self._test_routing_behavour(environ={
            "REQUEST_METHOD": prestans.http.VERB.GET,
            "SCRIPT_NAME": "/mountpoint",
            "PATH_INFO": "/some/path/{}".format(123),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "1234"
        })

    def test_script_alias_match_with_solidus_should_pass_call(self):
        """
        WSGIScriptAliasMatch /mountpoint/(.*) script.wsgi/$1
        :return:
        """
        self._test_routing_behavour(environ={
            "REQUEST_METHOD": prestans.http.VERB.GET,
            "SCRIPT_NAME": "/mountpoint/",
            "PATH_INFO": "/some/path/{}".format(123),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "1234"
        })

    def test_router_should_not_crash_with_no_path_info_field(self):
        """
        Test the ability to accept blank PATH_INFO as per specification PEP 3333

        :return:
        """
        expected_value = 123

        self._test_routing_behavour(environ={
            "REQUEST_METHOD": prestans.http.VERB.GET,
            "SCRIPT_NAME": "/mountpoint/some/path/{}".format(123),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "1234"
        }, match=r"/mountpoint/some/path/([0-9]+)", should_pass=False)

    def test_router_should_not_crash_with_no_script_name_field(self):
        """
        Test the ability to accept a blank SCRIPT_NAME as per spec PEP 3333

        `<https://www.python.org/dev/peps/pep-3333/#environ-variables>`
        :return:
        """

        expected_value = 123

        self._test_routing_behavour(environ={
            "REQUEST_METHOD": prestans.http.VERB.GET,
            "PATH_INFO": "/some/path/{}".format(123),
            "wsgi.url_scheme": "http",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "1234"})

    def _test_routing_behavour(self, environ, should_pass=True, expected_value=123, match=r"/some/path/([0-9]+)"):

        test_router = prestans.rest.RequestRouter([
            (match, _UserHandler)
        ], application_name="test-router", logger=LOGGER_MCLOGFACE)

        response = test_router(environ=environ, start_response=MockStartResponse.__call__)
        response_parsed = prestans.deserializer.JSON().loads(response[0])
        if should_pass:
            self.assert_should_find_route(environ, expected_value, match, response_parsed)
        else:
            self.assert_should_not_find_route(environ, match, response_parsed)

    def assert_should_not_find_route(self, environ, match, response_parsed):
        if 'id' in response_parsed.keys():
            self.fail(self.gen_route_match_failure_message(environ, match, assertion="SHOULD NOT MATCH"))

    def assert_should_find_route(self, environ, expected_value, match, response_parsed):
        if 'code' in response_parsed.keys() and response_parsed['code'] == 404:
            self.fail(self.gen_route_match_failure_message(environ, match, assertion="SHOULD MATCH"))
        else:
            self.assertEqual(response_parsed['id'], expected_value,
                             "expected id field with value of {}".format(expected_value))

    def gen_route_match_failure_message(self, environ, match, assertion="SHOULD"):
        return "SCRIPT_NAME[{script}] and PATH_INFO[{path}] {assertion} route[{route}]".format(
            script=environ.get("SCRIPT_NAME", ""),
            path=environ.get("PATH_INFO", ""),
            route=match,
            assertion=assertion
        )


if __name__ == '__main__':
    unittest.main()
