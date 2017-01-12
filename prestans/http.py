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

__all__ = ['VERB', 'STATUS']

#:
#: This file mostly contains constants for HTTP
#:

class VERB:
    """ 
    Encapsulates HTTP Verbs supported by the prestans framework in accordance
    with the REST definition. Each prestans REST handler must supporto at least
    one HTTP verb.

    HEAD is similar to a GET but it does not return a response.
    """

    GET    = "GET"
    HEAD   = "HEAD"
    POST   = "POST"
    PUT    = "PUT"
    PATCH  = "PATCH"
    DELETE = "DELETE"

    @classmethod
    def is_supported_verb(cls, method):
        return method in [VERB.GET, VERB.HEAD, VERB.POST, VERB.PUT, VERB.PATCH, VERB.DELETE]

class STATUS:
    """
    The following is a selection of HTTP status codes that are recommended for use 
    by REST services. You are welcome to use other available status codes.
    
    http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    """

    #: Informational

    CONTINUE                    = 100
    SWITCHING_PROTOCOLS         = 101

    #: Success

    OK                          = 200
    CREATED                     = 201
    ACCEPTED                    = 202
    NON_AUTH_INFORMATION        = 203
    NO_CONTENT                  = 204
    RESET_CONTENT               = 205
    PARTIAL_CONTENT             = 206

    #: Redirection

    MULTIPLE_CHOICES            = 300
    MOVED_PERMANENTLY           = 301
    FOUND                       = 302
    SEE_OTHER                   = 303
    NOT_MODIFIED                = 304
    USE_PROXY                   = 305
    SWITCH_PROXY                = 306
    TEMPORARY_REDIRECT          = 307
    PERMANENT_REDIRECT          = 308

    #: Client Error

    BAD_REQUEST                 = 400
    UNAUTHORIZED                = 401
    PAYMENT_REQUIRED            = 402
    FORBIDDEN                   = 403
    NOT_FOUND                   = 404
    METHOD_NOT_ALLOWED          = 405
    NOT_ACCEPTABLE              = 406
    PROXY_AUTH_REQUIRED         = 407
    REQUEST_TIMEOUT             = 408
    CONFLICT                    = 409
    GONE                        = 410
    LENGTH_REQUIRED             = 411
    PRECONDITION_FAILED         = 412
    REQUEST_ENTITY_TOO_LARGE    = 413
    REQUEST_URI_TOO_LARGE       = 414
    UNSUPPORTED_MEDIA_TYPE      = 415
    RANGE_NOT_SERIALIZABLE      = 416
    EXCEPTION_FAILED            = 417
    TEAPOT                      = 418
    AUTHENTICATION_TIMEOUT      = 419

    #: Server Error
    
    INTERNAL_SERVER_ERROR       = 500
    NOT_IMPLEMENTED             = 501
    BAD_GATEWAY                 = 502
    SERVICE_UNAVAILABLE         = 503
    GATEWAY_TIMEOUT             = 504
    UNSUPPORTED_HTTP_VERSION    = 505
    
