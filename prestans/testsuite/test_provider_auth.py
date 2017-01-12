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

import prestans.provider.auth
import prestans.rest


class BaseUnitTest(unittest.TestCase):

    def setUp(self):

        self.auth = prestans.provider.auth.Base()

    def test_debug(self):
        self.assertEqual(self.auth.debug, False)
        self.auth.debug = True
        self.assertEqual(self.auth.debug, True)

    def test_current_user_has_role(self):
        self.assertRaises(NotImplementedError, self.auth.current_user_has_role, "Admin")

    def test_is_authenticated_user(self):
        self.assertRaises(NotImplementedError, self.auth.is_authenticated_user)

    def test_is_authorized_user(self):
        self.assertRaises(NotImplementedError, self.auth.is_authorized_user, None)

    def test_get_current_user(self):
        self.assertRaises(NotImplementedError, self.auth.get_current_user)

    def tearDown(self):
        pass


class AdminRoleProvider(prestans.provider.auth.Base):
    
    def current_user_has_role(self, role_name):
        return role_name == "Admin"


class AuthenticatedProvider(prestans.provider.auth.Base):

    def is_authenticated_user(self):
        return True


class UnauthenticatedProvider(prestans.provider.auth.Base):

    def is_authenticated_user(self):
        return False


class AuthorizedProvider(prestans.provider.auth.Base):

    def is_authorized_user(self, config):
        return True


class UnauthorizedProvider(prestans.provider.auth.Base):

    def is_authorized_user(self, config):
        return False


class CustomUnitTest(unittest.TestCase):

    def setUp(self):

        self.admin_role = AdminRoleProvider()
        self.authenticated = AuthenticatedProvider()
        self.unauthenticated = UnauthenticatedProvider()
        self.authorized = AuthorizedProvider()
        self.unauthorized = UnauthorizedProvider()

    def test_debug(self):
        self.assertEqual(self.admin_role.debug, False)
        self.admin_role.debug = True
        self.assertEqual(self.admin_role.debug, True)

    def test_current_user_has_role(self):
        self.assertEqual(self.admin_role.current_user_has_role("Admin"), True)
        self.assertEqual(self.admin_role.current_user_has_role("Manager"), False)

    def test_is_authenticated_user(self):
        self.assertEqual(self.authenticated.is_authenticated_user(), True)
        self.assertEqual(self.unauthenticated.is_authenticated_user(), False)

    def test_is_authorized_user(self):
        self.assertEqual(self.authorized.is_authorized_user(None), True)
        self.assertEqual(self.unauthorized.is_authorized_user(None), False)

    def tearDown(self):
        pass


class AuthenticatedHandlerProvider(prestans.provider.auth.Base):
    
    def is_authenticated_user(self):
        return True

    def current_user_has_role(self, role_name):
        return role_name == "Admin"


class UnauthenticatedHandlerProvider(prestans.provider.auth.Base):
    
    def is_authenticated_user(self):
        return False


class HandlerWithoutProvider(prestans.rest.RequestHandler):

    @prestans.provider.auth.login_required
    def get(self):
        pass


class AuthenticatedHandler(prestans.rest.RequestHandler):
    
    __provider_config__ = prestans.provider.Config(
        authentication=AuthenticatedHandlerProvider()
    )

    @prestans.provider.auth.login_required
    def get(self):
        self.response.status = prestans.http.STATUS.NO_CONTENT

    @prestans.provider.auth.role_required("Admin")
    def post(self):
        self.response.status = prestans.http.STATUS.NO_CONTENT

    @prestans.provider.auth.role_required("Manager")
    def put(self):
        self.response.status = prestans.http.STATUS.NO_CONTENT


class UnauthenticatedHandler(prestans.rest.RequestHandler):
    
    __provider_config__ = prestans.provider.Config(
        authentication=UnauthenticatedHandlerProvider()
    )

    @prestans.provider.auth.login_required
    def get(self):
        self.response.status = prestans.http.STATUS.NO_CONTENT


def start_response(status, headers):
    pass


class HandlerUnitTest(unittest.TestCase):

    def setUp(self):

        logging.basicConfig()
        logger = logging.getLogger("prestans")

        charset="utf-8"
        serializers=[prestans.deserializer.JSON()]
        default_serializer=prestans.deserializer.JSON()

        self.get_environ = {"REQUEST_METHOD": prestans.http.VERB.GET}
        self.post_environ = {"REQUEST_METHOD": prestans.http.VERB.POST}
        self.put_environ = {"REQUEST_METHOD": prestans.http.VERB.PUT}

        get_request = prestans.rest.Request(
            environ=self.get_environ,
            charset=charset,
            logger=logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        post_request = prestans.rest.Request(
            environ=self.post_environ,
            charset=charset,
            logger=logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        put_request = prestans.rest.Request(
            environ=self.put_environ,
            charset=charset,
            logger=logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        response = prestans.rest.Response(
            charset=charset,
            logger=logger,
            serializers=serializers,
            default_serializer=default_serializer
        )

        self.authenticated_handler = AuthenticatedHandler(
            args=[],
            request=get_request,
            response=response,
            logger=logger,
            debug=True
        )

        self.unauthenticated_handler = UnauthenticatedHandler(
            args=[],
            request=get_request,
            response=response,
            logger=logger,
            debug=True
        )

        self.correct_role_handler = AuthenticatedHandler(
            args=[],
            request=post_request,
            response=response,
            logger=logger,
            debug=True
        )

        self.incorrect_role_handler = AuthenticatedHandler(
            args=[],
            request=put_request,
            response=response,
            logger=logger,
            debug=True
        )

        self.handler_without_provider = HandlerWithoutProvider(
            args=[],
            request=get_request,
            response=response,
            logger=logger,
            debug=True
        )

    def test_login_required(self):
        self.assertRaises(prestans.exception.AuthenticationError, self.handler_without_provider, self.get_environ, start_response)
        self.assertRaises(prestans.exception.AuthenticationError, self.unauthenticated_handler, self.get_environ, start_response)
        self.assertIsInstance(self.authenticated_handler(self.get_environ, start_response), list)

    def test_current_user_has_role(self):
        self.assertRaises(prestans.exception.AuthorizationError, self.incorrect_role_handler, self.post_environ, start_response)
        self.assertIsInstance(self.correct_role_handler(self.put_environ, start_response), list)

    def tearDown(self):
        pass