from prestans import exception
from prestans.http import STATUS
from prestans import rest

import pytest
import unittest


class PermanentRedirectHandler(rest.RequestHandler):

    def get(self):
        raise exception.PermanentRedirect("/permanent-new")


class TemporaryRedirectHandler(rest.RequestHandler):

    def get(self):
        raise exception.TemporaryRedirect("/temporary-new")


@pytest.fixture
def test_app():
    from webtest import TestApp
    from prestans.rest import RequestRouter

    api = RequestRouter([
        ('/permanent', PermanentRedirectHandler),
        ('/temporary', TemporaryRedirectHandler)
    ], application_name="api", debug=True)

    return TestApp(app=api)


class Issue155(unittest.TestCase):

    def test_permanent_redirect(self):
        app = test_app()

        resp = app.get("/permanent")
        self.assertEquals(resp.status_int, STATUS.PERMANENT_REDIRECT)

    def test_temporary_redirect(self):
        app = test_app()

        resp = app.get("/temporary")
        self.assertEquals(resp.status_int, STATUS.TEMPORARY_REDIRECT)
