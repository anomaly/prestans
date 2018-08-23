from prestans.http import STATUS
from prestans import parser
from prestans.provider import auth
from prestans import rest
from prestans import types

import json
from mock import patch, PropertyMock
import pytest
import unittest


class PersonREST(types.Model):
    first_name = types.String()
    last_name = types.String()


BODY = {
    "first_name": "Jane",
    "last_name": "Doe"
}


class AuthContextProvider(auth.Base):

    def current_user_has_role(self, role_name):
        return False

    def get_current_user(self):
        return None

    def is_authorized_user(self, config):
        return False

    def is_authenticated_user(self):
        return False


class AuthHandler(rest.RequestHandler):

    def handler_will_run(self):
        self.__provider_config__.authentication = AuthContextProvider()

    __parser_config__ = parser.Config(
        POST=parser.VerbConfig(
            body_template=PersonREST(),
            response_attribute_filter_default_value=True,
            response_template=PersonREST()
        )
    )

    @auth.login_required
    def post(self):
        self.response.status = STATUS.NO_CONTENT


class NoAuthHandler(rest.RequestHandler):

    __parser_config__ = parser.Config(
        POST=parser.VerbConfig(
            body_template=PersonREST(),
            response_attribute_filter_default_value=True,
            response_template=PersonREST()
        )
    )

    def post(self):
        person = self.request.parsed_body

        self.response.status = STATUS.OK
        self.response.body = person


@pytest.fixture
def test_app():
    from webtest import TestApp
    from prestans.rest import RequestRouter

    api = RequestRouter([
        ('/auth', AuthHandler),
        ('/no-auth', NoAuthHandler)
    ], application_name="api", debug=True)

    return TestApp(app=api)


class Issue155(unittest.TestCase):

    def test_no_auth_parses_body(self):
        """
        """
        app = test_app()
        resp = app.post_json(url="/no-auth", params=BODY, status="*")
        resp_body = json.loads(resp.body if isinstance(resp.body, str) else resp.body.decode())

        self.assertEquals(resp.status_int, STATUS.OK)
        self.assertEquals(resp_body["first_name"], BODY["first_name"])
        self.assertEquals(resp_body["last_name"], BODY["last_name"])

    @patch("prestans.rest.request.Request.parsed_body", new_callable=PropertyMock)
    @patch("prestans.rest.request.Request.parse_body")
    def test_unauthenticated_ignores_body(self, parsed_body, parse_body):
        """
        """
        app = test_app()
        resp = app.post_json(url="/auth", params=BODY, status="*")
        self.assertEqual(resp.status_int, STATUS.UNAUTHORIZED)
        parsed_body.assert_not_called()
        parse_body.assert_not_called()
