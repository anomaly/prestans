#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
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

__all__ = ['AdapterRegistryManager', 'Adapter', 'CollectionAdapter', 'ModelAdapter']

## @package prestans.ext.data.adapters contains adapters to translate stored models to prestans types
#

from prestans import ERROR_MESSAGE

import prestans.types

## @brief AdapterRegistryManager keeps track of rest to persistent model maps
#
# AdapterRegistryManager should not be instantiated by the applications, a singleton
# instance supplied by this package.
#
class AdapterRegistryManager:

    def __init__(self):
        self._persistent_map = {}
        self._rest_map = {}

    ## @brief registers an adapter into the singleton registry
    #
    # @param model_adapter must be an instance of a subclass of prestans.ext.data.adapters.ModelAdapter
    #
    def register_adapter(self, model_adapter):
        
        if not issubclass(model_adapter.__class__, Adapter):
            raise Exception(ERROR_MESSAGE.NOT_SUBCLASS % (model_adapter.__class__.__name, 'Adapter'))
        
        rest_class_signature = model_adapter.rest_model_class.__module__ + "." + model_adapter.rest_model_class.__name__
        persistent_class_signature = model_adapter.persistent_model_class.__module__ + "." + model_adapter.persistent_model_class.__name__
        
        """ Store references to how a rest model maps to a persistent model and vice versa """
        self._persistent_map[persistent_class_signature] = model_adapter
        self._rest_map[rest_class_signature] = model_adapter
        
    def get_adapter_for_persistent_model(self, persistent_model):
        
        class_signature = persistent_model.__class__.__module__ + "." + persistent_model.__class__.__name__
        
        if not self._persistent_map.has_key(class_signature):
            raise Exception(ERROR_MESSAGE.ADAPTER_NOT_REGISTERED % class_signature)
        return self._persistent_map[class_signature]
        
    def get_adapter_for_rest_model(self, rest_model):
        
        class_signature = rest_model.__class__.__module__ + "." + rest_model.__class__.__name__
        
        if not self._rest_map.has_key(class_signature):
            raise Exception(ERROR_MESSAGE.ADAPTER_NOT_REGISTERED % class_signature)
        return self._rest_map[class_signature]

## @brief registry is globally available and all models must add to this registry
#
#  registry is a singleton, apps can create their own registry, but its to use the singleton
#  purely for performance reasons.
#    
registry = AdapterRegistryManager()    

## @package prestans.ext.data.adapter contains adapters to translate stored models to prestans types
#

## @brief Adapter is an abstract base class, used by RESTResponse to identify a collection
#
# @ingroup adapters
#
class Adapter(object):
    pass
    

## @brief translates a stored model to prestans rest models
#
# @ingroup adapters
#
class ModelAdapter(Adapter):
    
    def __init__(self, rest_model_class, persistent_model_class):
        self._rest_model_class = rest_model_class
        self._persistent_model_class = persistent_model_class
        
    """ Properties """

    def _get_persistent_model_class(self):
        return self._persistent_model_class
        
    persistent_model_class = property(_get_persistent_model_class)
    
    def _get_rest_model_class(self):
        return self._rest_model_class
        
    rest_model_class = property(_get_rest_model_class)
    
    """ The following methods are stubs, these should be implemented for the specific backends """
    
    ## @brief adapts a persistent model to a rest model by inspecting
    #
    def adapt_persistent_to_rest(self, persistent_object):
        raise Exception(ERROR_MESSAGE.NO_DIRECT_USE % ('ModelAdapter'))
        