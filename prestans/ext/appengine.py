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

__all__ = ['AppEngineAuthContextProvider']

## @package prestans.appengine Providers Google AppEngine specific implementation of providers
#
# appengine is not imported as part of "all", this has to be explicity imported by the user.
#

from prestans.provider import auth
from prestans.provider import cache
from prestans.provider import throttle

from google.appengine.api import oauth
from google.appengine.api import users
from google.appengine.api import memcache

import os

_IS_DEVELOPMENT_SERVER = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')

#:
#: Provides Authentication Context for Google's AppEngine Environment
#:
#:
#: auth.AuthContextProvider implementation for Google AppEngine, uses google.appengine.api.users
#: to determine logged in users and return a reference to the current user.
#:
#: Refer to decorators in handlers package for more information.
#:
class AppEngineAuthContextProvider(auth.Base):
    
    #:
    #: Overriden is_authenticated_user for Google AppEngine
    #: Uses google.appengine.api.users method get_current_user to check if a user is logged in 
    #:
    def is_authenticated_user(self):
        return users.get_current_user() is not None
      
    #:  
    #: Overriden get_current_user for Google AppEngine
    #: Checks for oauth capable request first, if this fails fall back to standard users API
    #:
    def get_current_user(self):

        if _IS_DEVELOPMENT_SERVER:
            return users.get_current_user()
        else:
            try:
                user = oauth.get_current_user()
            except oauth.OAuthRequestError, exp:
                user = users.get_current_user()
            return user
  
#:      
#: Provides a wrapper on AppEngine's memcache implementation 
#:
class AppEngineMemcacheProvider(cache.Base):
    
    def __init__(self, key_provider=None):
        self.key_provider = key_provider
    
    def get(self, key):
        memcache.get(key)       
    
    def set(self, key, value, expiry=60, namespace=None):
        memcache.set(key, value, expiry)
        
    def add(self, key, value, expiry=60, namespace=None):
        memcache.add(key, value, expiry, namespace)
        
    def delete(self, key, seconds=0, namespace=None):
        memcache.delete(key, seconds, namespace)
        
    def flush_all(self):
        memcache.flush_all()

