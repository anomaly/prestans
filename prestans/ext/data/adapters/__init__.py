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

from prestans import exception
from prestans import parser
from prestans import types


class ModelAdapter(object):
    
    def __init__(self, rest_model_class, persistent_model_class):
        """
        :param rest_model_class:
        :param persistent_model_class:
        """

        if issubclass(rest_model_class, types.Model):
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

    def adapt_persistent_to_rest(self, persistent_object, attribute_filter=None):
        """
        adapts a persistent model to a rest model by inspecting
        """

        rest_model_instance = self.rest_model_class()

        for attribute_key in rest_model_instance.get_attribute_keys():

            rest_attr = getattr(self.rest_model_class, attribute_key)

            # don't bother processing if the persistent model doesn't have this attribute
            if not hasattr(persistent_object, attribute_key):

                if isinstance(rest_attr, types.Model):
                    #: If the attribute is a Model, then we set it to None otherwise we get a model
                    #: with default values, which is invalid when constructing responses
                    try:
                        setattr(rest_model_instance, attribute_key, None)
                    # catch any exception thrown from setattr to give a usable error message
                    except TypeError as exp:
                        raise TypeError('Attribute %s, %s' % (attribute_key, str(exp)))

                continue
            # ignore class methods
            elif inspect.ismethod(getattr(persistent_object, attribute_key)):
                import logging
                logging.error("ignoring method: "+attribute_key)
                continue
            # attribute is not visible don't bother processing
            elif isinstance(attribute_filter, parser.AttributeFilter) and \
                    not attribute_filter.is_attribute_visible(attribute_key):
                continue

            # handles prestans array population from SQLAlchemy relationships
            elif isinstance(rest_attr, types.Array):

                persistent_attr_value = getattr(persistent_object, attribute_key)
                rest_model_array_handle = getattr(rest_model_instance, attribute_key)

                # iterator uses the .append method exposed by prestans arrays to validate
                # and populate the collection in the instance.
                for collection_element in persistent_attr_value:
                    if isinstance(rest_attr.element_template, types.Boolean) or \
                       isinstance(rest_attr.element_template, types.Float) or \
                       isinstance(rest_attr.element_template, types.Integer) or \
                       isinstance(rest_attr.element_template, types.String):
                        rest_model_array_handle.append(collection_element)
                    else:
                        element_adapter = registry.get_adapter_for_rest_model(rest_attr.element_template)

                        # check if there is a sub model filter
                        sub_attribute_filter = None
                        if attribute_filter and attribute_key in attribute_filter:
                            sub_attribute_filter = getattr(attribute_filter, attribute_key)

                        adapted_rest_model = element_adapter.adapt_persistent_to_rest(
                            collection_element,
                            sub_attribute_filter
                        )
                        rest_model_array_handle.append(adapted_rest_model)

            elif isinstance(rest_attr, types.Model):

                try:
                    persistent_attr_value = getattr(persistent_object, attribute_key)

                    if persistent_attr_value is None:
                        adapted_rest_model = None
                    else:
                        model_adapter = registry.get_adapter_for_rest_model(rest_attr)

                        # check if there is a sub model filter
                        sub_attribute_filter = None
                        if isinstance(attribute_filter, parser.AttributeFilter) and \
                                attribute_key in attribute_filter:
                            sub_attribute_filter = getattr(attribute_filter, attribute_key)

                        adapted_rest_model = model_adapter.adapt_persistent_to_rest(
                            persistent_attr_value,
                            sub_attribute_filter
                        )

                    setattr(rest_model_instance, attribute_key, adapted_rest_model)

                except TypeError as exp:
                    raise TypeError('Attribute %s, %s' % (attribute_key, str(exp)))
                except exception.DataValidationException as exp:
                    raise exception.InconsistentPersistentDataError(attribute_key, str(exp))

            else:

                # otherwise copy the value to the rest model
                try:
                    persistent_attr_value = getattr(persistent_object, attribute_key)
                    setattr(rest_model_instance, attribute_key, persistent_attr_value)
                except TypeError as exp:
                    raise TypeError('Attribute %s, %s' % (attribute_key, str(exp)))
                except exception.ValidationError as exp:
                    raise exception.InconsistentPersistentDataError(attribute_key, str(exp))

        return rest_model_instance


def adapt_persistent_instance(persistent_object, target_rest_class=None, attribute_filter=None):
    """
    Adapts a single persistent instance to a REST model; at present this is a
    common method for all persistent backends.

    Refer to: https://groups.google.com/forum/#!topic/prestans-discuss/dO1yx8f60as
    for discussion on this feature
    """

    # try and get the adapter and the REST class for the persistent object
    if target_rest_class is None:
        adapter_instance = registry.get_adapter_for_persistent_model(persistent_object)
    else:
        if inspect.isclass(target_rest_class):
            target_rest_class = target_rest_class()

        adapter_instance = registry.get_adapter_for_persistent_model(persistent_object, target_rest_class)

    # would raise an exception if the attribute_filter differs from the target_rest_class
    if attribute_filter is not None and isinstance(attribute_filter, parser.AttributeFilter):
        parser.AttributeFilter.from_model(target_rest_class).conforms_to_template_filter(attribute_filter)

    return adapter_instance.adapt_persistent_to_rest(persistent_object, attribute_filter)


def adapt_persistent_collection(persistent_collection, target_rest_class=None, attribute_filter=None):
    # ensure that collection is iterable and has at least one element
    persistent_collection_length = 0

    # attempt to detect the length of the persistent_collection
    if persistent_collection and isinstance(persistent_collection, (list, tuple)):
        persistent_collection_length = len(persistent_collection)
    # SQLAlchemy query
    elif persistent_collection and persistent_collection.__module__ == "sqlalchemy.orm.query":
        persistent_collection_length = persistent_collection.count()
    # Google App Engine NDB
    elif persistent_collection and persistent_collection.__module__ == "google.appengine.ext.ndb":
        persistent_collection_length = persistent_collection.count()

    # if the persistent_collection is empty then return a blank array
    if persistent_collection_length == 0:
        return types.Array(element_template=target_rest_class())

    # try and get the adapter and the REST class for the persistent object
    if target_rest_class is None:
        adapter_instance = registry.get_adapter_for_persistent_model(
            persistent_collection[0]
        )
    else:
        if inspect.isclass(target_rest_class):
            target_rest_class = target_rest_class()

        adapter_instance = registry.get_adapter_for_persistent_model(
            persistent_collection[0],
            target_rest_class
        )

    adapted_models = types.Array(element_template=adapter_instance.rest_model_class())

    for persistent_object in persistent_collection:
        adapted_models.append(adapter_instance.adapt_persistent_to_rest(persistent_object, attribute_filter))

    return adapted_models


class AdapterRegistryManager(object):
    """
    AdapterRegistryManager keeps track of rest to persistent model maps

    New AdapterRegistryManager's should not be instantiated by the application, a singleton
    instance is supplied by this package.
    """
    DEFAULT_REST_ADAPTER = "prestans_rest_default_adapter"

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

        # store references to rest model
        self._rest_map[rest_class_signature] = model_adapter

        if persistent_class_signature not in self._persistent_map:
            self._persistent_map[persistent_class_signature] = dict()

        # store a reference to the adapter under both REST signature and default key
        # the default is always the last registered model (to match behaviour before this was patched)
        self._persistent_map[persistent_class_signature][self.DEFAULT_REST_ADAPTER] = model_adapter
        self._persistent_map[persistent_class_signature][rest_class_signature] = model_adapter

    def register_persistent_rest_pair(self, persistent_model_class, rest_model_class):
        """
        :param persistent_model_class:
        :param rest_model_class:
        """
        self.register_adapter(ModelAdapter(
            rest_model_class=rest_model_class,
            persistent_model_class=persistent_model_class
        ))

    def clear_registered_adapters(self):
        """
        Clears all of the currently registered model adapters
        """
        self._persistent_map.clear()
        self._rest_map.clear()

    def get_adapter_for_persistent_model(self, persistent_model, rest_model=None):
        """
        :param persistent_model: instance of persistent model
        :param rest_model: specific REST model
        :return: the matching model adapter
        :rtype: ModelAdapter
        """
        persistent_signature = self.generate_signature(persistent_model)
        
        if persistent_signature in self._persistent_map:
            sub_map = self._persistent_map[persistent_signature]

            # return the first match if REST model was not specified
            if rest_model is None:
                return self._persistent_map[persistent_signature][self.DEFAULT_REST_ADAPTER]
            else:
                rest_sig = self.generate_signature(rest_model)
                if rest_sig in sub_map:
                    return self._persistent_map[persistent_signature][rest_sig]

        raise TypeError("No registered Data Adapter for class %s" % persistent_signature)
        
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
