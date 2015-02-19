# -*- coding: utf-8 -*-
#
#  prestans, A WSGI compliant REST micro-framework
#  http://prestans.org
#
#  Copyright (c) 2015, Anomaly Software Pty Ltd.
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

from functools import wraps

import prestans.exception

class Base(object):

    def __init__(self):
        self._debug = False

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    def current_user_has_role(self, role_name):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)
    
    def is_authenticated_user(self, handler_reference):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)
        
    def is_authorized_user(self, handler_reference):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)

    def get_current_user(self):
        raise TypeError("%s should not be used directly" % self.__class__.__name__)


def login_required(http_method_handler):
    """
    provides a decorator for RESTRequestHandler methods to check for authenticated users

    RESTRequestHandler subclass must have a auth_context instance, refer to prestans.auth
    for the parent class definition.

    If decorator is used and no auth_context is provided the client will be denied access

    Handler will return a 401 Unauthorized if the user is not logged in, the service does not redirect
    to login handler page, this is the client's responsibility

    auth_context_handler instance provides a message called get_current_user, use this to obtain a
    reference to an authenticated user profile.

    If all goes well, the original handler definition is executed.

    """
    
    @wraps(http_method_handler)
    def secure_http_method_handler(self, *args):
            
        if not self.__provider_config__.authentication:
            _message = "Service available to authenticated users only, no auth context provider set in handler"
            raise prestans.exception.AuthenticationError(_message)
            
        if not self.__provider_config__.authentication.is_authenticated_user():
            raise prestans.exception.AuthenticationError()

        http_method_handler(self, *args)
        
    return secure_http_method_handler
    
def role_required(role_name=None):
    """
    Authenticates a HTTP method handler based on a provided role

    With a little help from Peter Cole's Blog
    http://mrcoles.com/blog/3-decorator-examples-and-awesome-python/

    """
    
    def _role_required(http_method_handler):

        def secure_http_method_handler(self, *args):
    
            # Role name must be provided
            if role_name is None:
                raise prestans.exception.AuthorizationError("None")
        
            # Authentication context must be set
            if not self.__provider_config__.authentication:
                _message = "Service available to authenticated users only, no auth context provider set in handler"
                raise prestans.exception.AuthenticationError(_message)
            
            # Check for the role by calling current_user_has_role
            if not self.__provider_config__.authentication.current_user_has_role(role_name):
                raise prestans.exception.AuthorizationError(role_name)

            http_method_handler(self, *args)
        
        return wraps(http_method_handler)(secure_http_method_handler)
        
    return _role_required

def access_required(config=None):
    """
    Authenticates a HTTP method handler based on a custom set of arguments
    """
    
    def _access_required(http_method_handler):

        def secure_http_method_handler(self, *args):

            # Authentication context must be set
            if not self.__provider_config__.authentication:
                _message = "Service available to authenticated users only, no auth context provider set in handler"
                raise prestans.exception.AuthenticationError(_message)

            # Check for access by calling is_authorized_user
            if not self.__provider_config__.authentication.is_authorized_user(config):
                _message = "Service available to authorized users only"
                raise prestans.exception.AuthorizationError(_message)

            http_method_handler(self, *args)
        
        return wraps(http_method_handler)(secure_http_method_handler)
        
    return _access_required