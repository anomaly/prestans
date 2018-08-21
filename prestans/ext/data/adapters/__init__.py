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
import inspect

from prestans.types import Model


class ModelAdapter(object):
    
    def __init__(self, rest_model_class, persistent_model_class):

        if issubclass(rest_model_class, Model):
            self._rest_model_class = rest_model_class
        else:
            raise TypeError("rest_model_class must be sub class of prestans.types.Model")

        self._persistent_model_class = persistent_model_class

    @property
    def persistent_model_class(self):
        return self._persistent_model_class
    
    @property
    def rest_model_class(self):
        return self._rest_model_class
            
    def adapt_persistent_to_rest(self, persistent_object):
        raise NotImplementedError("adapt_persistent_to_rest direct use not allowed")


class AdapterRegistryManager(object):
    """
    AdapterRegistryManager keeps track of rest to persistent model maps

    AdapterRegistryManager should not be instantiated by the applications, a singleton
    instance supplied by this package.
    """

    def __init__(self):
        self._persistent_map = dict()
        self._rest_map = dict()

    @classmethod
    def generate_signature(cls, class_or_instance):
        if inspect.isclass(class_or_instance):
            return class_or_instance.__module__ + "." + class_or_instance.__name__
        else:
            return class_or_instance.__class__.__module__ + "." + class_or_instance.__class__.__name__

    def register_adapter(self, model_adapter):
        
        if not isinstance(model_adapter, ModelAdapter):
            msg = "Registry received instance of type %s is not a ModelAdapter" % model_adapter.__class__.__name__
            raise TypeError(msg)
        
        rest_class_signature = self.generate_signature(model_adapter.rest_model_class)
        persistent_class_signature = self.generate_signature(model_adapter.persistent_model_class)

        # store references to how a rest model maps to a persistent model and vice versa
        self._persistent_map[persistent_class_signature] = model_adapter
        self._rest_map[rest_class_signature] = model_adapter
        
    def get_adapter_for_persistent_model(self, persistent_model):
        """
        :param persistent_model: instance of persistent model
        :return: the matching model adapter
        :rtype: ModelAdapter
        """
        class_signature = self.generate_signature(persistent_model)
        
        if class_signature not in self._persistent_map:
            raise TypeError("No registered Data Adapter for class %s" % class_signature)

        return self._persistent_map[class_signature]
        
    def get_adapter_for_rest_model(self, rest_model):
        """
        :param rest_model: instance of REST model
        :return: the matching model adapter
        :rtype: ModelAdapter
        """
        class_signature = self.generate_signature(rest_model)
        
        if class_signature not in self._rest_map:
            raise TypeError("No registered Data Adapter for class %s" % class_signature)

        return self._rest_map[class_signature]


# singleton instantiated if adapter package is imported
registry = AdapterRegistryManager()
