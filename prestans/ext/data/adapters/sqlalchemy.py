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

__all__ = ['QueryResultIterator', 'ModelAdapter']

## @package prestans.ext.data.adapters.sqlalchemy SQLAlchemy specific implementation of Data Adapter
#

from prestans.ext.data import adapters
import prestans.parsers
import prestans.types
import inspect

## @brief base implementation that translates record sets into prestans arrays
#
def QueryResultIterator(collection, target_rest_instance=None, attribute_filter=None):
        
    """ Ensure that colleciton is iterable and has atleast one element """
    collection_length = 0
    
    """ Attempt to reliably detect the length of the collection """
    if collection and isinstance(collection, (list, tuple)):
        collection_length = len(collection)
    elif collection and collection.__module__ == "sqlalchemy.orm.query":
        collection_length = collection.count()
        
    """ If the collection is empty then return a blank array """
    if collection_length == 0:
        return prestans.types.Array()
        
    """ Try and get the adapter and the REST class for the persistent object """
    if target_rest_instance is None:
        adapter_instance = adapters.registry.get_adapter_for_persistent_model(collection[0])
    else:
        if inspect.isclass(target_rest_instance):
            target_rest_instance = target_rest_instance()
        
        adapter_instance = adapters.registry.get_adapter_for_rest_model(target_rest_instance)
        
    adapted_models = prestans.types.Array(element_template=adapter_instance.rest_model_class())
    
    for persistent_object in collection:
        adapted_models.append(adapter_instance.adapt_persistent_to_rest(persistent_object, attribute_filter))
        
    return adapted_models

## @brief Provide a brige between REST models and SQLAlchemy objects
#   
class ModelAdapter(adapters.ModelAdapter):
    
    ## @brief adapts a persistent model to a rest model by inspecting
    #
    def adapt_persistent_to_rest(self, persistent_object, attribute_filter=None):

        rest_model_instance = self.rest_model_class()
        
        for attribute_key in rest_model_instance.get_attribute_keys():                           

            rest_attr = getattr(self.rest_model_class, attribute_key)

            if not hasattr(persistent_object, attribute_key):
                # Don't bother processing if the persistent model doesn't have this attribute

                if issubclass(rest_attr.__class__, prestans.types.Model):
                    # If the attribute is a Model, then we set it to None otherwise we get a model 
                    # with default values, which is invalid when constructing responses
                    try:
                        setattr(rest_model_instance, attribute_key, None)
                    #catch any exception thrown from setattr to give a useable error message
                    except prestans.types.DataTypeValidationException, exp:
                        raise prestans.types.DataTypeValidationException('Attribute %s, %s' % (attribute_key, str(exp)))
                    
                continue
            #Attribute not visible don't bother processing
            elif isinstance(attribute_filter, prestans.parsers.AttributeFilter) and not attribute_filter.is_attribute_visible(attribute_key):
                continue
            elif issubclass(rest_attr.__class__, prestans.types.Array):        
                # Handles prestans array population from SQLAlchemy relationships 

                persistent_attr_value = getattr(persistent_object, attribute_key)
                rest_model_array_handle = rest_model_instance.__dict__[attribute_key]
                
                # Iterator uses the .append method exposed by prestans arrays to validate
                # and populate the collection in the instance.
                for collection_element in persistent_attr_value:
                    if type(rest_attr._element_template) == type(prestans.types.String()):
                        rest_model_array_handle.append(collection_element)
                    elif type(rest_attr._element_template) == type(prestans.types.Integer()):
                        rest_model_array_handle.append(collection_element)
                    elif type(rest_attr._element_template) == type(prestans.types.Float()):
                        rest_model_array_handle.append(collection_element)
                    elif type(rest_attr._element_template) == type(prestans.types.Boolean()):
                        rest_model_array_handle.append(collection_element)
                    else:
                        element_adapter = adapters.registry.get_adapter_for_rest_model(rest_attr._element_template)

                        #Check if there is a sub model filter
                        sub_attribute_filter = None
                        if attribute_filter and attribute_filter.has_key(attribute_key):
                            sub_attribute_filter = getattr(attribute_filter, attribute_key)

                        adapted_rest_model = element_adapter.adapt_persistent_to_rest(collection_element, sub_attribute_filter)                    
                        rest_model_array_handle.append(adapted_rest_model)
            
            elif issubclass(rest_attr.__class__, prestans.types.Model):
                
                try:
                    persistent_attr_value = getattr(persistent_object, attribute_key)
                    
                    if persistent_attr_value is None:
                        adapted_rest_model = None
                    else:
                        model_adapter = adapters.registry.get_adapter_for_rest_model(rest_attr)

                        #Check if there is a sub model filter
                        sub_attribute_filter = None
                        if isinstance(attribute_filter, prestans.parsers.AttributeFilter) and attribute_filter.has_key(attribute_key):
                            sub_attribute_filter = getattr(attribute_filter, attribute_key)

                        adapted_rest_model = model_adapter.adapt_persistent_to_rest(persistent_attr_value, sub_attribute_filter)
                    setattr(rest_model_instance, attribute_key, adapted_rest_model)
                    
                except prestans.types.DataTypeValidationException, exp:
                    raise prestans.types.DataTypeValidationException('Attribute %s, %s' % (attribute_key, str(exp)))
                
            else:
                
                """ Otherwise copy the value to the rest model """
                try:
                    persistent_attr_value = getattr(persistent_object, attribute_key)
                    setattr(rest_model_instance, attribute_key, persistent_attr_value)
                except prestans.types.DataTypeValidationException, exp:
                    raise prestans.types.DataTypeValidationException('Attribute %s, %s' % (attribute_key, str(exp)))

            
        return rest_model_instance