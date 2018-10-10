from prestans.http import STATUS
from prestans import rest

import pytest
import unittest


class EmptyOk(rest.RequestHandler):

    def get(self):
        self.response.status = STATUS.OK


class EmptyNoContent(rest.RequestHandler):

    def get(self):
        self.response.status = STATUS.NO_CONTENT


@pytest.fixture
def test_app():
    from webtest import TestApp
    from prestans.rest import RequestRouter

    api = RequestRouter([
        ('/empty-ok', EmptyOk),
        ('/empty-no-content', EmptyNoContent)
    ], application_name="api", debug=True)

    return TestApp(app=api)


class Issue175(unittest.TestCase):

    def test_ok_with_empty_body(self):

        app = test_app()
        resp = app.get(url="/empty-ok", status="*")
        self.assertEquals(resp.status_int, STATUS.OK)

    def test_no_content_with_empty_body(self):

        app = test_app()
        resp = app.get(url="/empty-no-content", status="*")
        self.assertEquals(resp.status_int, STATUS.NO_CONTENT)
