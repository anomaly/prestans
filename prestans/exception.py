# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
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
#      * Neither the name of Eternity Technologies nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL ETERNITY TECHNOLOGIES BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

class Base(Exception):
    pass

class DirectUseNotAllowed(Base):
    pass

class ParseFailed(Base):
    pass

class InvalidValue(Base):
    pass

class LessThanMinimum(Base):
    pass

class MoreThanMaximum(Base):
    pass

class InvalidLength(Base):
    pass

class InvalidType(Base):
    pass

class InvalidCollection(Base):
    pass

class MissingParameter(Base):
    pass

class InvalidFormat(Base):
    pass

class InvalidMetaValue(Base):
    pass

class UnregisteredAdapter(Base):
    pass




class RESTOperation(Exception):
    """
    Extends from the Base exception to make available a HTTP status code, these
    are thrown if an unacceptable REST operation is performed. 

    E.g a client attempts to access data they are not allowed to.
    """
    pass

class ServiceUnavailable(RESTOperation):
    pass

class BadRequest(RESTOperation):
    pass

class Conflict(RESTOperation):
    pass

class NotFound(RESTOperation):
    pass

class Unauthorized(RESTOperation):
    pass

class Forbidden(RESTOperation):
    pass