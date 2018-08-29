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

from prestans import exception
from prestans.http import STATUS
from prestans.http import VERB
from prestans.provider.auth import Base
from prestans.provider.auth import access_required
from prestans.provider.auth import login_required
from prestans.provider.auth import role_required
from prestans.provider import Config
from prestans.rest import Request
from prestans.rest import RequestHandler
from prestans.rest import Response


class BaseUnitTest(unittest.TestCase):

    def test_debug(self):
        base = Base()
        self.assertEqual(base.debug, False)

        base.debug = True
        self.assertEqual(base.debug, True)

    def test_request(self):
        base = Base()
        self.assertIsNone(base.request)

        base.request = True
        self.assertEqual(base.request, True)

    def test_current_user_has_role(self):
        base = Base()
        self.assertRaises(NotImplementedError, base.current_user_has_role, "Admin")

    def test_is_authenticated_user(self):
        base = Base()
        self.assertRaises(NotImplementedError, base.is_authenticated_user)

    def test_is_authorized_user(self):
        base = Base()
        self.assertRaises(NotImplementedError, base.is_authorized_user, None)

    def test_get_current_user(self):
        base = Base()
        self.assertRaises(NotImplementedError, base.get_current_user)


class AdminRoleProvider(Base):
    
    def current_user_has_role(self, role_name):
        return role_name == "Admin"


class AuthenticatedProvider(Base):

    def is_authenticated_user(self):
        return True


class UnauthenticatedProvider(Base):

    def is_authenticated_user(self):
        return False


class AuthorizedProvider(Base):

    def is_authorized_user(self, config):
        return True


class UnauthorizedProvider(Base):

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


def start_response(status, headers):
    pass


class LoginRequiredUnitTest(unittest.TestCase):

    def setUp(self):

        import logging
        logging.basicConfig()
        self.logger = logging.getLogger("prestans")

        from prestans.deserializer import JSON
        self.charset = "utf-8"
        self.serializers = [JSON()]
        self.default_serializer = JSON()

        self.get_environ = {"REQUEST_METHOD": VERB.GET}

        self.get_request = Request(
            environ=self.get_environ,
            charset=self.charset,
            logger=self.logger,
            deserializers=self.serializers,
            default_deserializer=self.default_serializer
        )

        self.response = Response(
            charset=self.charset,
            logger=self.logger,
            serializers=self.serializers,
            default_serializer=self.default_serializer
        )

        class HandlerWithoutProvider(RequestHandler):

            @login_required
            def get(self):
                pass

        self.handler_without_provider = HandlerWithoutProvider

        class AuthenticatedProvider(Base):

            def is_authenticated_user(self):
                return True

        class AuthenticatedHandler(RequestHandler):

            __provider_config__ = Config(
                authentication=AuthenticatedProvider()
            )

            @login_required
            def get(self):
                self.response.status = STATUS.NO_CONTENT

        self.authenticated_handler = AuthenticatedHandler

        class UnauthenticatedProvider(Base):

            def is_authenticated_user(self):
                return False

        class UnauthenticatedHandler(RequestHandler):

            __provider_config__ = Config(
                authentication=UnauthenticatedProvider()
            )

            @login_required
            def get(self):
                self.response.status = STATUS.NO_CONTENT

        self.unauthenticated_handler = UnauthenticatedHandler

    def test_login_required_no_provider_raises_exception(self):
        handler = self.handler_without_provider(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthenticationError, handler, self.get_environ, start_response)

    def test_login_required_unauthenticated_raises_exception(self):
        handler = self.unauthenticated_handler(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthenticationError, handler, self.get_environ, start_response)

    def test_login_required_authenticated(self):
        handler = self.authenticated_handler(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertIsInstance(handler(self.get_environ, start_response), list)


class RoleRequiredUnitTest(unittest.TestCase):

    def setUp(self):
        import logging
        logging.basicConfig()
        self.logger = logging.getLogger("prestans")

        from prestans.deserializer import JSON
        charset = "utf-8"
        serializers = [JSON()]
        default_serializer = JSON()

        self.get_environ = {"REQUEST_METHOD": VERB.GET}
        self.post_environ = {"REQUEST_METHOD": VERB.POST}
        self.put_environ = {"REQUEST_METHOD": VERB.PUT}

        self.get_request = Request(
            environ=self.get_environ,
            charset=charset,
            logger=self.logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        self.post_request = Request(
            environ=self.post_environ,
            charset=charset,
            logger=self.logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        self.put_request = Request(
            environ=self.put_environ,
            charset=charset,
            logger=self.logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        self.response = Response(
            charset=charset,
            logger=self.logger,
            serializers=serializers,
            default_serializer=default_serializer
        )

        class AuthProvider(Base):

            def current_user_has_role(self, role_name):
                return role_name == "Admin"

        class HandlerWithoutProvider(RequestHandler):

            @role_required("Admin")
            def get(self):
                pass

        self.handler_without_provider = HandlerWithoutProvider

        class HandlerWithProvider(RequestHandler):

            __provider_config__ = Config(
                authentication=AuthProvider()
            )

            @role_required(None)
            def get(self):
                self.response.status = STATUS.NO_CONTENT

            @role_required("Manager")
            def post(self):
                self.response.status = STATUS.NO_CONTENT

            @role_required("Admin")
            def put(self):
                self.response.status = STATUS.NO_CONTENT

        self.handler_with_provider = HandlerWithProvider

    def test_role_required_no_provider_raises_exception(self):
        handler = self.handler_without_provider(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthenticationError, handler, self.get_environ, start_response)

    def test_role_required_none_raises_authorization_error(self):
        handler = self.handler_with_provider(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthorizationError, handler, self.get_environ, start_response)

    def test_role_required_incorrect_role_raises_exception(self):
        handler = self.handler_with_provider(
            args=[],
            kwargs={},
            request=self.post_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthorizationError, handler, self.post_environ, start_response)

    def test_role_required_success(self):
        handler = self.handler_with_provider(
            args=[],
            kwargs={},
            request=self.put_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertIsInstance(handler(self.put_environ, start_response), list)


class AccessRequiredUnitTest(unittest.TestCase):

    def setUp(self):
        import logging
        logging.basicConfig()
        self.logger = logging.getLogger("prestans")

        from prestans.deserializer import JSON
        charset = "utf-8"
        serializers = [JSON()]
        default_serializer = JSON()

        class AuthProvider(Base):

            def is_authorized_user(self, config):
                return config["name"] == "Jack"

        class HandlerWithoutProvider(RequestHandler):

            @access_required({"name": "Jack"})
            def get(self):
                self.response.status = STATUS.NO_CONTENT
        self.handler_without_provider = HandlerWithoutProvider

        class HandlerWithProvider(RequestHandler):

            __provider_config__ = Config(
                authentication=AuthProvider()
            )

            @access_required({"name": "Jack"})
            def get(self):
                self.response.status = STATUS.NO_CONTENT

            @access_required({"name": "Jill"})
            def post(self):
                self.response.status = STATUS.NO_CONTENT

        self.handler_with_provider = HandlerWithProvider

        self.get_environ = {"REQUEST_METHOD": VERB.GET}
        self.post_environ = {"REQUEST_METHOD": VERB.POST}

        self.get_request = Request(
            environ=self.get_environ,
            charset=charset,
            logger=self.logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        self.post_request = Request(
            environ=self.post_environ,
            charset=charset,
            logger=self.logger,
            deserializers=serializers,
            default_deserializer=default_serializer
        )

        self.response = Response(
            charset=charset,
            logger=self.logger,
            serializers=serializers,
            default_serializer=default_serializer
        )

    def test_access_required_no_provider_raises_exception(self):
        handler = self.handler_without_provider(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthenticationError, handler, self.get_environ, start_response)

    def test_access_required_unauthorized_raises_exception(self):
        handler = self.handler_with_provider(
            args=[],
            kwargs={},
            request=self.post_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertRaises(exception.AuthorizationError, handler, self.post_environ, start_response)

    def test_access_required_success(self):
        handler = self.handler_with_provider(
            args=[],
            kwargs={},
            request=self.get_request,
            response=self.response,
            logger=self.logger,
            debug=True
        )

        self.assertIsInstance(handler(self.get_environ, start_response), list)
