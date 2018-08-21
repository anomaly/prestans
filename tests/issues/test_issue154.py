from prestans.http import STATUS
from prestans.rest import RequestHandler

import pytest
import unittest


class NoContentHandler(RequestHandler):

    def get(self):
        self.response.status = STATUS.NO_CONTENT


@pytest.fixture
def test_app():
    from webtest import TestApp
    from prestans.rest import RequestRouter

    api = RequestRouter([
        ('/no-content', NoContentHandler)
    ], application_name="api", debug=True)

    return TestApp(app=api)


class Issue154(unittest.TestCase):

    def test_204_header_omitted(self):
            """
            Request should return no content with header omitted
            """
            app = test_app()
            resp = app.get('/no-content')
            self.assertEqual(resp.status_int, STATUS.NO_CONTENT)
            self.assertIsNone(resp.content_type)
