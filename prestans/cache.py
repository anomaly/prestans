#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2012, Eternity Technologies Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
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

__all__ = ['CacheProvider']

from functools import wraps

## @package prestans.cache Providers Caching layer for use by prestans applications
#
#  
#

## @brief CacheKeyProvider has HTTP method maps just like the RESTRequestHandler and returns cache key names
#
# Ensure that the method signatures match your corresponding HTTP request handler.
#
# A copy of the request object is passed onto the CacheKeyProvider to allow checks against the parsed 
# ParameterSet and Request body.
#
# The Default CacheKeyProvier returns None for all key names, None ignores cache providion
#
# Refer to the decorators that set the auto cache handling rules
# 
class CacheKeyProvider:
    
    request = None
    
    def get(self, *args):
        return None
        
    def post(self, *args):
        return None
        
    def put(self, *args):
        return None
        
    def delete(self, *args):
        return None

## @brief CacheProvider subclasses provide a wrapper to various Cache providers
#
# Instances of this class can not be used directly. Use an implementation like MemcacheCacheProvider or
# appengine.AppEngineMemcacheProvider 
#
# The aim is to provide a meta layer to interact with caching layers, to make applicaiton
# code portable across platforms.
#
class CacheProvider:
    
    def __init__(self, key_provider=CacheKeyProvider()):
        self.key_provider = key_provider
    
    def get(self, key):
        raise Exception('CacheProvider may not be used directly')
        
    def set(self, key, value, expiry=60):
        raise Exception('CacheProvider may not be used directly')
        
    def add(self, key, value, expiry=60):
        raise Exception('CacheProvider may not be used directly')
        
    def delete(self, key):
        raise Exception('CacheProvider may not be used directly')
        
    def flush_all(self):
        raise Exception('CacheProvider may not be used directly')

## @brief MemecacheCacheProvider is a wrapper for standard Memecache servers
#   
class MemcacheCacheProvider(CacheProvider):
    pass
    
    
## @brief fetch rule decorator
# 
# @ingroup decorators
#   
def fetch(original_function):
    
    @wraps(original_function)
    def cacheable_original_function(self, *args):

        if self.__class__.cache_provider and self.__class__.cache_provider.key_provider:

            # Reference to prestans HTTP Status codes, instance self.response is not available
            from prestans.rest import STATUS as PRESTANS_HTTP_STATUS
            
            # Depending on the function that was called in the handler we get a reference to 
            # a function with the same name and singature in the KeyProvider instance
            http_hook_name = original_function.__name__
            function_hook = getattr(self.__class__.cache_provider.key_provider, http_hook_name)

            # Ask the function hook for the key
            cache_key_name = function_hook(*args)
        
            # Returns cached content if the provider is able to return a result
            if cache_key_name and self.__class__.cache_provider.get(cache_key_name):
                self.response.body = self.__class__.cache_provider.get(cache_key_name)
                self.response.http_status = PRESTANS_HTTP_STATUS.NOT_MODIFIED
                return
                
        # Perform original_function if cache could not match key
        original_function(self, *args)
    
    return cacheable_original_function

## @brief clear rule decorator
# 
# @ingroup decorators
#       
def clear(original_function):
    
    @wraps(original_function)
    def clear_cache_original_function(self, *args):
        
        if self.__class__.cache_provider and self.__class__.cache_provider.key_provider:

            cache_key_name = self.__class__.cache_proivder.key_provider.get(*args)
            
            if cache_key_name:
                self.__class__.cache_proivder.delete(cache_key_name)
            
        original_function(self, *args)
        
    return clear_cache_original_function
