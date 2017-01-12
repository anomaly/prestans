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

from functools import wraps

import prestans.exception


class Base(object):
    """Base class for an auth provider, this should be overridden to suit
    each application."""

    def __init__(self):
        self._debug = False
        self._request = None

    @property
    def debug(self):
        """Getter for debug property"""
        return self._debug

    @debug.setter
    def debug(self, value):
        """Setter for debug property"""
        self._debug = value

    @property
    def request(self):
        """Getter for request property"""
        return self._request

    @request.setter
    def request(self, value):
        """Setter for request property"""
        self._request = value

    def current_user_has_role(self, role_name):
        """Override this method to check if the given role is allowed access"""
        raise NotImplementedError

    def is_authenticated_user(self):
        """Override this method to check if a user is logged in"""
        raise NotImplementedError

    def is_authorized_user(self, config):
        """Override this method to check if a user has access"""
        raise NotImplementedError

    def get_current_user(self):
        """Override this method to provide reference to logged in user"""
        raise NotImplementedError


def login_required(http_method_handler):
    """
    provides a decorator for RESTRequestHandler methods to check for authenticated users

    RESTRequestHandler subclass must have a auth_context instance, refer to prestans.auth
    for the parent class definition.

    If decorator is used and no auth_context is provided the client will be denied access.

    Handler will return a 401 Unauthorized if the user is not logged in, the service does
    not redirect to login handler page, this is the client's responsibility.

    auth_context_handler instance provides a message called get_current_user, use this
    to obtain a reference to an authenticated user profile.

    If all goes well, the original handler definition is executed.
    """

    @wraps(http_method_handler)
    def secure_http_method_handler(self, *args):

        if not self.__provider_config__.authentication:
            _message = ("Service available to authenticated users only, "
                        "no auth context provider set in handler")
            authentication_error = prestans.exception.AuthenticationError(_message)
            authentication_error.request = self.request
            raise authentication_error

        if not self.__provider_config__.authentication.is_authenticated_user():
            authentication_error = prestans.exception.AuthenticationError()
            authentication_error.request = self.request
            raise authentication_error

        http_method_handler(self, *args)

    return secure_http_method_handler


def role_required(role_name=None):
    """
    Authenticates a HTTP method handler based on a provided role

    With a little help from Peter Cole's Blog
    http://mrcoles.com/blog/3-decorator-examples-and-awesome-python/

    """

    def _role_required(http_method_handler):

        @wraps(http_method_handler)
        def secure_http_method_handler(self, *args):

            # Role name must be provided
            if role_name is None:
                _message = "Role name must be provided"
                authorization_error = prestans.exception.AuthorizationError(_message)
                authorization_error.request = self.request
                raise authorization_error

            # Authentication context must be set
            if not self.__provider_config__.authentication:
                _message = ("Service available to authenticated users only, "
                            "no auth context provider set in handler")
                authentication_error = prestans.exception.AuthenticationError(_message)
                authentication_error.request = self.request
                raise authentication_error

            # Check for the role by calling current_user_has_role
            if not self.__provider_config__.authentication.current_user_has_role(role_name):
                authorization_error = prestans.exception.AuthorizationError(role_name)
                authorization_error.request = self.request
                raise authorization_error

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
                _message = ("Service available to authenticated users only, "
                            "no auth context provider set in handler")
                authentication_error = prestans.exception.AuthenticationError(_message)
                authentication_error.request = self.request
                raise authentication_error

            # Check for access by calling is_authorized_user
            if not self.__provider_config__.authentication.is_authorized_user(config):
                _message = "Service available to authorized users only"
                authorization_error = prestans.exception.AuthorizationError(_message)
                authorization_error.request = self.request
                raise authorization_error

            http_method_handler(self, *args)

        return wraps(http_method_handler)(secure_http_method_handler)

    return _access_required
