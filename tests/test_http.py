import unittest

from prestans.http import STATUS
from prestans.http import VERB


class VerbTest(unittest.TestCase):
    def test_codes(self):
        self.assertEqual(VERB.GET, "GET")
        self.assertEqual(VERB.HEAD, "HEAD")
        self.assertEqual(VERB.POST, "POST")
        self.assertEqual(VERB.PUT, "PUT")
        self.assertEqual(VERB.PATCH, "PATCH")
        self.assertEqual(VERB.DELETE, "DELETE")
        self.assertEqual(VERB.OPTIONS, "OPTIONS")

    def test_is_supported_verb(self):
        self.assertTrue(VERB.is_supported_verb("GET"))
        self.assertTrue(VERB.is_supported_verb("HEAD"))
        self.assertTrue(VERB.is_supported_verb("POST"))
        self.assertTrue(VERB.is_supported_verb("PUT"))
        self.assertTrue(VERB.is_supported_verb("PATCH"))
        self.assertTrue(VERB.is_supported_verb("DELETE"))
        self.assertTrue(VERB.is_supported_verb("OPTIONS"))
        self.assertFalse(VERB.is_supported_verb("CAT"))
        self.assertFalse(VERB.is_supported_verb("DOG"))


class StatusTest(unittest.TestCase):
    def test_codes(self):
        self.assertEqual(STATUS.CONTINUE, 100)
        self.assertEqual(STATUS.SWITCHING_PROTOCOLS, 101)
        self.assertEqual(STATUS.PROCESSING, 102)
        self.assertEqual(STATUS.EARLY_HINTS, 103)

        self.assertEqual(STATUS.OK, 200)
        self.assertEqual(STATUS.CREATED, 201)
        self.assertEqual(STATUS.ACCEPTED, 202)
        self.assertEqual(STATUS.NON_AUTHORITATIVE_INFORMATION, 203)
        self.assertEqual(STATUS.NO_CONTENT, 204)
        self.assertEqual(STATUS.RESET_CONTENT, 205)
        self.assertEqual(STATUS.PARTIAL_CONTENT, 206)
        self.assertEqual(STATUS.MULTI_STATUS, 207)
        self.assertEqual(STATUS.ALREADY_REPORTED, 208)
        self.assertEqual(STATUS.IM_USED, 226)

        self.assertEqual(STATUS.MULTIPLE_CHOICES, 300)
        self.assertEqual(STATUS.MOVED_PERMANENTLY, 301)
        self.assertEqual(STATUS.FOUND, 302)
        self.assertEqual(STATUS.SEE_OTHER, 303)
        self.assertEqual(STATUS.NOT_MODIFIED, 304)
        self.assertEqual(STATUS.USE_PROXY, 305)
        self.assertEqual(STATUS.SWITCH_PROXY, 306)
        self.assertEqual(STATUS.TEMPORARY_REDIRECT, 307)
        self.assertEqual(STATUS.PERMANENT_REDIRECT, 308)

        self.assertEqual(STATUS.BAD_REQUEST, 400)
        self.assertEqual(STATUS.UNAUTHORIZED, 401)
        self.assertEqual(STATUS.PAYMENT_REQUIRED, 402)
        self.assertEqual(STATUS.FORBIDDEN, 403)
        self.assertEqual(STATUS.NOT_FOUND, 404)
        self.assertEqual(STATUS.METHOD_NOT_ALLOWED, 405)
        self.assertEqual(STATUS.NOT_ACCEPTABLE, 406)
        self.assertEqual(STATUS.PROXY_AUTH_REQUIRED, 407)
        self.assertEqual(STATUS.REQUEST_TIMEOUT, 408)
        self.assertEqual(STATUS.CONFLICT, 409)
        self.assertEqual(STATUS.GONE, 410)
        self.assertEqual(STATUS.LENGTH_REQUIRED, 411)
        self.assertEqual(STATUS.PRECONDITION_FAILED, 412)
        self.assertEqual(STATUS.PAYLOAD_TOO_LARGE, 413)
        self.assertEqual(STATUS.URI_TOO_LONG, 414)
        self.assertEqual(STATUS.UNSUPPORTED_MEDIA_TYPE, 415)
        self.assertEqual(STATUS.RANGE_NOT_SATISFIABLE, 416)
        self.assertEqual(STATUS.EXCEPTION_FAILED, 417)
        self.assertEqual(STATUS.MISDIRECTED_REQUEST, 421)
        self.assertEqual(STATUS.UNPROCESSABLE_ENTITY, 422)
        self.assertEqual(STATUS.LOCKED, 423)

        self.assertEqual(STATUS.INTERNAL_SERVER_ERROR, 500)
        self.assertEqual(STATUS.NOT_IMPLEMENTED, 501)
        self.assertEqual(STATUS.BAD_GATEWAY, 502)
        self.assertEqual(STATUS.SERVICE_UNAVAILABLE, 503)
        self.assertEqual(STATUS.GATEWAY_TIMEOUT, 504)
        self.assertEqual(STATUS.HTTP_VERSION_NOT_SUPPORTED, 505)
        self.assertEqual(STATUS.VARIANT_ALSO_NEGOTIATES, 506)
        self.assertEqual(STATUS.INSUFFICIENT_STORAGE, 507)
        self.assertEqual(STATUS.LOOP_DETECTED, 508)
        self.assertEqual(STATUS.NOT_EXTENDED, 510)
        self.assertEqual(STATUS.NETWORK_AUTHENTICATION_REQUIRED, 511)