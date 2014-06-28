#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2013, Anomaly Software Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
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
#  DISCLAIMED. IN NO EVENT SHALL Anomaly Software BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__all__ = ['AuthContextProvider']

from functools import wraps

## @package prestans.auth providers skeleton for an Authentication Provider
#
#

class AuthContextProvider:
    
    def current_user_has_role(self, role_name):
        raise Exception("Direct use of AuthContextProvider not allowed")
    
    def is_authenticated_user(self, handler_reference):
        raise Exception("Direct use of AuthContextProvider not allowed")
        
    def get_current_user(self):
        raise Exception("Direct use of AuthContextProvider not allowed")

## @brief provides a decorator for RESTRequestHandler methods to check for authenticated users
#
# @ingroup decorators
#
# RESTRequestHandler subclass must have a auth_context instance, refer to prestans.auth
# for the parent class definition.
#
# If decorator is used and no auth_context is provided the client will be denied access
#
# Handler will return a 401 Unauthorized if the user is not logged in, the service does not redirect
# to login handler page, this is the client's responsibility
#
# auth_context_handler instance provides a message called get_current_user, use this to obtain a
# reference to an authenticated user profile.
#
# If all goes well, the original handler definition is executed.
#
def login_required(http_method_handler):
    
    ## @brief provides a security wrapper for HTTP handlers
    #
    @wraps(http_method_handler)
    def secure_http_method_handler(self, *args):
    
        # Reference to prestans HTTP Status codes, instance self.response is not available
        from prestans.rest import STATUS as PRESTANS_HTTP_STATUS
        
        if not self.auth_context:
            self.response.http_status = PRESTANS_HTTP_STATUS.UNAUTHORIZED
            self.response.set_body_attribute('message', "Service available to authenticated users only, no auth context provider set in handler")
            return
            
        if not self.auth_context.is_authenticated_user():
            self.response.http_status = PRESTANS_HTTP_STATUS.UNAUTHORIZED
            self.response.set_body_attribute('message', "Service available to authenticated users only")
            return

        http_method_handler(self, *args)
        
    return secure_http_method_handler
    
## @brief Authenticates a HTTP method handler based on a provided role
#
# With a little help from Peter Cole's Blog
# http://mrcoles.com/blog/3-decorator-examples-and-awesome-python/
#
# @ingroup decorators
#
def role_required(role_name=None):
    
    def _role_required(http_method_handler):

        ## @brief provides a security wrapper for HTTP handlers
        #
        def secure_http_method_handler(self, *args):
    
            # Reference to prestans HTTP Status codes, instance self.response is not available
            from prestans.rest import STATUS as PRESTANS_HTTP_STATUS

            # Role name must be provided
            if not role_name:
                self.response.http_status = PRESTANS_HTTP_STATUS.BAD_REQUEST
                self.response.set_body_attribute('message', "role name can't be None for role_required authentication decorator")
                return
        
            # Authentication context must be set
            if not self.auth_context:
                self.response.http_status = PRESTANS_HTTP_STATUS.UNAUTHORIZED
                self.response.set_body_attribute('message', "Service available to authenticated users only, no auth context provider set in handler")
                return
            
            # Check for the role by calling current_user_has_role
            if not self.auth_context.current_user_has_role(role_name):
                self.response.http_status = PRESTANS_HTTP_STATUS.UNAUTHORIZED
                self.response.set_body_attribute('message', "Service available to authenticated users only")
                return

            http_method_handler(self, *args)
        
        return wraps(http_method_handler)(secure_http_method_handler)
        
    return _role_required
    