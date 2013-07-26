# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
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

__all__ = ['Config']

import inspect
import string

import prestans.exception

#:
#:
#:

class Config(object):

    def __init__(self, GET=None, POST=None, PUT=None, PATCH=None, DELETE=None):
        self._GET = GET
        self._POST = POST
        self._PUT = PUT
        self._PATCH = PATCH
        self._DELETE = DELETE

class ParameterSet(object):
    pass


#:
#:
#:

class AttributeFilter(object):
    #: 
    #:  { 
    #:    field_name0: true, 
    #:    field_name1: false, 
    #:    collection_name0: true, 
    #:    collection_name1: false,
    #:    collection_name2: {
    #:        sub_field_name0: true,
    #:        sub_field_name1: false 
    #:    }
    #:  }

    @classmethod
    def from_model(self, model_instance, default_value=False):
        #:
        #: wrapper for Model's get_attribute_filter
        #:

        if issubclass(model_instance.__class__, prestans.types.DataCollection):
            return model_instance.get_attribute_filter(default_value)

        raise TypeError("model_instance must be a sublcass of presatans.types.DataCollection, %s given" % 
                        (model_instance.__class__.__name__))

    def __init__(self, from_dictionary=None):
        #:
        #: Creates an attribute filter object, optionally populates from a 
        #: dictionary of booleans
        #:
        
        if from_dictionary:
            self._init_from_dictionary(from_dictionary)

    def _conforms_to_template_filter(self, template_filter):
        #:
        #: Check AttributeFilter conforms to the rules set by the template
        #:
        #: - If self, has attributes that template_fitler does not contain, throw Exception
        #: - If sub list found, perform the first check
        #: - If self has a value for an attribute, assign to final AttributeFilter
        #:- If not found, assign value from template
        #:       

        if not isinstance(template_filter, self.__class__):
            raise TypeError("AttributeFilter can only check conformance against another template filter, %s provided" % 
                            (template_filter.__class__.__name__))

        #:
        #: Keys from the template
        #:
        template_filter_keys = template_filter.keys()
        # Keys from the object itself
        this_filter_keys = self.keys()

        #:
        #: 1. Check to see if the client has provided unwanted keys
        #:
        unwanted_keys = set(this_filter_keys) - set(template_filter_keys)
        if len(unwanted_keys) > 0:
            keys_string = string.join(unwanted_keys, " ")
            raise InvalidDataTypeException("_response_field_list has attributes (%s) that are not part of the template model" % keys_string)

        #:
        #: 2. Make a attribute_filter that we send back
        #:
        evaluated_attribute_filter = AttributeFilter()

        #:
        #: 3. Evaluate the differences between the two, with template_filter as the standard
        #:
        for template_key in template_filter_keys:

            if template_key in this_filter_keys:

                value = getattr(self, template_key)

                #:
                #: If sub filter and boolean provided with of true, create default filter 
                #: with value of true
                #:
                if isinstance(value, bool) and \
                value is True and \
                isinstance(getattr(template_filter, template_key), AttributeFilter):
                    setattr(evaluated_attribute_filter, template_key, getattr(template_filter, template_key))
                elif isinstance(value, bool):
                    setattr(evaluated_attribute_filter, template_key, value)
                elif isinstance(value, self.__class__):
                    # Attribute lists sort themselves out, to produce sub Attribute Filters 
                    template_sub_list = getattr(template_filter, template_key)
                    this_sub_list = getattr(self, template_key)
                    setattr(evaluated_attribute_filter, template_key, this_sub_list._conforms_to_template_filter(template_sub_list))
            else:
                setattr(evaluated_attribute_filter, template_key, getattr(template_filter, template_key))

        return evaluated_attribute_filter
        
    def keys(self):
        #: 
        #: returns a list of usable keys
        #: 

        keys = list()

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            keys.append(attribute_name)

        return keys

    def has_key(self, key):
        #: 
        #: contains a particular key, wrapper on self.__dict__.key
        #: 
        return self.__dict__.has_key(key)

    def is_filter_at_key(self, key):
        #: 
        #: return True if attribute is a subfilter
        #: 

        if self.has_key(key) and isinstance(attribute_status, self.__class__):
            return True

        return False

    def is_attribute_visible(self, key):
        #: 
        #: returns True if an attribute is visible
        #: 
        #: If attribute is an instance of AttributeFilter, it returns True if all attributes
        #: of the sub filter are visible.
        #:         
        if self.has_key(key):
            attribute_status = getattr(self, key)
            if isinstance(attribute_status, bool) and attribute_status == True:
                return True
            elif isinstance(attribute_status, self.__class__) and \
            attribute_status.are_any_attributes_visible():
                return True

        return False

    def are_any_attributes_visible(self):
        #: 
        #: checks to see if any attributes are set to true
        #: 

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods 
                continue

            if isinstance(type_instance, bool) and type_instance == True:
                return True
            elif isinstance(type_instance, self.__class__) and \
            type_instance.are_all_attributes_visible() == True:
                # Serialise attribute filter children to dictioanaries 
                return True

        return False

    def are_all_attributes_visible(self):
        #: 
        #: checks to see if all attributes are set to true
        #:         

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            if isinstance(type_instance, bool) and type_instance == False:
                return False
            elif isinstance(type_instance, self.__class__) and type_instance.are_all_attributes_visible() == False:
                # Serialise attribute filter children to dictioanaries 
                return False

        return True

    def as_dict(self):
        #: 
        #: turns attribute filter object into python dictionary
        #:         

        output_dictionary = dict()

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods 
                continue

            if isinstance(type_instance, bool):
                output_dictionary[attribute_name] = type_instance
            elif isinstance(type_instance, self.__class__):
                # Serialise attribute filter children to dictioanaries 
                output_dictionary[attribute_name] = type_instance.as_dict()

        return output_dictionary


    def _init_from_dictionary(self, from_dictionary):
        #: 
        #: Private helper to init values from a dictionary, wraps chidlren into 
        #: AttributeFilter objects
        #: 

        if not isinstance(from_dictionary, dict):
            raise TypeError("from_dictionary must be of type dict, %s provided" % 
                            (from_dictionary.__class__.__name__))

        for key, value in from_dictionary.iteritems():

            if not isinstance(value, (bool, dict)):
                # Check to see we can work with the value 
                raise TypeError("AttributeFilter input for key %s must be boolean or dict, %s provided" % 
                                (key, value.__class__.__name__))

            # Either keep the value of wrap it up with AttributeFilter 
            if isinstance(value, bool):
                setattr(self, key, value)
            elif isinstance(value, dict):
                setattr(self, key, AttributeFilter(from_dictionary=value))


    def __setattr__(self, key, value):
        #: 
        #: Overrides setattr to allow only booleans or an AttributeFilter
        #: 

        # Set internal fields
        if key[0:1] == "_":
            self.__dict__[key] = value
            return

        # Values should either be boolean or type of self
        if isinstance(value, (bool, self.__class__)):
            self.__dict__[key] = value
            return

        raise TypeError("%s name in %s must be of type Boolean or AttributeFilter, given %s" % 
                        (key, self.__class__.__name__, value.__class__.__name__))

#:
#:
#:

class ParserRuleSet(object):
    pass

#:
#:
#:

class RequestParser(object):
    
    GET     = None
    POST    = None
    PUT     = None
    PATCH   = None
    DELETE  = None

    def parse(self, request, response, environ):
        #: 
        #: If the implementing request parser does not specify a parser for a method, None is returned, 
        #: this completely bypasses the parsing process.
        #: 
        #: The implementing request parser must assign an instance of %ParserRuleSet for each HTTP method.
        #: 
        #: RequestParser will attempt use those rules to parse the input and assign them to the passed in
        #: request object. It returns True or False.
        #: 
        #: self The object pointer
        #: response object
        #: request The request to parse
        #: 
        
        request_method = request.get_request_method()

        if not self.__class__.__dict__.has_key(request_method) or self.__class__.__dict__[request_method] is None:
            #: 
            #: Default rule set is None, ignores parsing for Pameters and Body 
            #: 
            return
        
        if not isinstance(self.__class__.__dict__[request_method], ParserRuleSet):
            #:  
            #: Handles the developer not assinging an object of type ParserRuleSet 
            #: 
            raise NotParserRuleSetObjectException(request_method + " does not have a valid ParserRuleSet")
        
        parser_rule_set = self.__class__.__dict__[request_method]

        #: Parse parameters or None if nothing matched
        request.parameter_set = parser_rule_set._parameter_set_for_request(request)
        
        #: Parse request body
        request.parsed_body_model = parser_rule_set._parsed_body_for_request(request, environ)

        #: Parse the field filter list
        response.attribute_filter = parser_rule_set._parse_attribute_filter(request)