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

__all__ = ['ClientThrottleProvider']

from functools import wraps

## @package prestans.throttle providers skeleton for an Throttle Provider
#
#
class ClientThrottleProvider(object):

    ## @brief Common constructor that lets API designers setup thorttle rules
    def __init__(self, requests_per_minute=20):
        self._requests_per_minute = requests_per_minute

    def get_connected_client_id(self):
        """ 
            Returns an identifier for the requesting client, the can either be
            a unique identifier per user for APIs that can't identify logged in users
            or IP addresses, or via a cookie, refer to rest.handler.handler_will_run
            for the opportunity to use Cookies 

        """
        pass

    def is_throttled(self):
        """ Return a boolean to indicate if the current client is throttled """
        pass


## @brief provides a decorator for RESTRequestHandler methods to check for authenticated users
#
# @ingroup decorators
#
#
def throttle(http_method_handler):
    
    ## @brief provides a security wrapper for HTTP handlers
    #
    @wraps(http_method_handler)
    def throttled_http_method_handler(self, *args):
    
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
        
    return throttled_http_method_handler