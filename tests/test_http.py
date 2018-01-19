import unittest

from prestans.http import STATUS
from prestans.http import VERB


class VerbTest(unittest.TestCase):
    def test_codes(self):
        self.assertEquals(VERB.GET, "GET")
        self.assertEquals(VERB.HEAD, "HEAD")
        self.assertEquals(VERB.POST, "POST")
        self.assertEquals(VERB.PUT, "PUT")
        self.assertEquals(VERB.PATCH, "PATCH")
        self.assertEquals(VERB.DELETE, "DELETE")
        self.assertEquals(VERB.OPTIONS, "OPTIONS")

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
        self.assertEquals(STATUS.CONTINUE, 100)
        self.assertEquals(STATUS.SWITCHING_PROTOCOLS, 101)
        self.assertEquals(STATUS.PROCESSING, 102)
        self.assertEquals(STATUS.EARLY_HINTS, 103)

        self.assertEquals(STATUS.OK, 200)
        self.assertEquals(STATUS.CREATED, 201)
        self.assertEquals(STATUS.ACCEPTED, 202)
        self.assertEquals(STATUS.NON_AUTHORITATIVE_INFORMATION, 203)
        self.assertEquals(STATUS.NO_CONTENT, 204)
        self.assertEquals(STATUS.RESET_CONTENT, 205)
        self.assertEquals(STATUS.PARTIAL_CONTENT, 206)
        self.assertEquals(STATUS.MULTI_STATUS, 207)
        self.assertEquals(STATUS.ALREADY_REPORTED, 208)
        self.assertEquals(STATUS.IM_USED, 226)

        self.assertEquals(STATUS.MULTIPLE_CHOICES, 300)
        self.assertEquals(STATUS.MOVED_PERMANENTLY, 301)
        self.assertEquals(STATUS.FOUND, 302)
        self.assertEquals(STATUS.SEE_OTHER, 303)
        self.assertEquals(STATUS.NOT_MODIFIED, 304)
        self.assertEquals(STATUS.USE_PROXY, 305)
        self.assertEquals(STATUS.SWITCH_PROXY, 306)
        self.assertEquals(STATUS.TEMPORARY_REDIRECT, 307)
        self.assertEquals(STATUS.PERMANENT_REDIRECT, 308)

        self.assertEquals(STATUS.BAD_REQUEST, 400)
        self.assertEquals(STATUS.UNAUTHORIZED, 401)
        self.assertEquals(STATUS.PAYMENT_REQUIRED, 402)
        self.assertEquals(STATUS.FORBIDDEN, 403)
        self.assertEquals(STATUS.NOT_FOUND, 404)
        self.assertEquals(STATUS.METHOD_NOT_ALLOWED, 405)
        self.assertEquals(STATUS.NOT_ACCEPTABLE, 406)
        self.assertEquals(STATUS.PROXY_AUTH_REQUIRED, 407)
        self.assertEquals(STATUS.REQUEST_TIMEOUT, 408)
        self.assertEquals(STATUS.CONFLICT, 409)
        self.assertEquals(STATUS.GONE, 410)
        self.assertEquals(STATUS.LENGTH_REQUIRED, 411)
        self.assertEquals(STATUS.PRECONDITION_FAILED, 412)
        self.assertEquals(STATUS.PAYLOAD_TOO_LARGE, 413)
        self.assertEquals(STATUS.URI_TOO_LONG, 414)
        self.assertEquals(STATUS.UNSUPPORTED_MEDIA_TYPE, 415)
        self.assertEquals(STATUS.RANGE_NOT_SATISFIABLE, 416)
        self.assertEquals(STATUS.EXCEPTION_FAILED, 417)
        self.assertEquals(STATUS.MISDIRECTED_REQUEST, 421)
        self.assertEquals(STATUS.UNPROCESSABLE_ENTITY, 422)
        self.assertEquals(STATUS.LOCKED, 423)

        self.assertEquals(STATUS.INTERNAL_SERVER_ERROR, 500)
        self.assertEquals(STATUS.NOT_IMPLEMENTED, 501)
        self.assertEquals(STATUS.BAD_GATEWAY, 502)
        self.assertEquals(STATUS.SERVICE_UNAVAILABLE, 503)
        self.assertEquals(STATUS.GATEWAY_TIMEOUT, 504)
        self.assertEquals(STATUS.HTTP_VERSION_NOT_SUPPORTED, 505)
        self.assertEquals(STATUS.VARIANT_ALSO_NEGOTIATES, 506)
        self.assertEquals(STATUS.INSUFFICIENT_STORAGE, 507)
        self.assertEquals(STATUS.LOOP_DETECTED, 508)
        self.assertEquals(STATUS.NOT_EXTENDED, 510)
        self.assertEquals(STATUS.NETWORK_AUTHENTICATION_REQUIRED, 511)