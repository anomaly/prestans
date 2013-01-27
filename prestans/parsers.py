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

__all__ = ['ParameterSet', 'ParserRuleSet', 'RequestParser', 'NotParserRuleSetObjectException', 'NotParameterSetObjectException']

## @package prestans.parsers Provides classes to construct request parsers
#

import inspect, string

import prestans.types

from prestans import ERROR_MESSAGE

## @brief %NotParserRuleSetObjectException
#
# @ingroup exception
#
class NotParserRuleSetObjectException(Exception):
    pass

## @brief %NotParameterSetObjectException
#
# @ingroup exception
#   
class NotParameterSetObjectException(Exception):
    pass

## @brief %NoSetMatchedException
#
# @ingroup exception
#   
class NoSetMatchedException(Exception):
    pass

## @brief %InvalidParameterSetAttributeException
#
# @ingroup exception
#   
class InvalidParameterSetAttributeException(Exception):
    pass
    
## @brief %InvalidDataTypeException
#
# @ingroup exception
#   
class InvalidDataTypeException(Exception):
    pass

## @brief %RequiresDataCollectionException
#
# @ingroup exception
#
class RequiresDataCollectionException(Exception):
    pass

## @brief %RequiresModelException
#
# @ingroup exception
#
class RequiresModelException(Exception):
    pass

## @brief %BodyTemplateParseException
#
# @ingroup exception
#
class BodyTemplateParseException(Exception):
    pass    
    
## @brief %EmptyBodyException
#
# @ingroup exception
#
class EmptyBodyException(Exception):
    pass

## @brief %ReservedWordException(Exception):
#
# Raised if a prestans reserved word is used in configuring an app level class.
#
# @ingroup exception
#
class ReservedWordException(Exception):
    
    def __init__(self, reserved_word):
        self._reserved_word = reserved_word

    def __str__(self):
        return "reserved word %s not allowed in request"  % (self._reserved_word)

## @brief %ParameterSet is a group of Dataprestans.types that are expected as GET parameters
#
# %ParameterSet defines rules and patterns in which they are acceptable.
# while ParserRuleSet is responsible for running the parse mechanism.
#
class ParameterSet(object):

    ## @brief blueprint support, returnsn a partial dictionary
    def blueprint(self):

        blueprint = dict()
        blueprint['type'] = "%s.%s" % (self.__module__, self.__class__.__name__)

        # Fields
        fields = dict()
        model_class_members = inspect.getmembers(self.__class__)
    
        # Inspects the attributes of a parameter set and tries to validate the input 
        for attribute_name, type_instance in self.__class__.__dict__.iteritems():
            
            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods 
                continue

            if attribute_name == "_response_field_list":
                # Prestans reserved word cannot be used
                raise ReservedWordException("_response_field_list")

            if not issubclass(type_instance.__class__, 
                              prestans.types.String) and not issubclass(type_instance.__class__, 
                              prestans.types.Float) and not issubclass(type_instance.__class__, 
                              prestans.types.Integer):
                
                # Must be a sub class of DataType 
                raise InvalidDataTypeException(ERROR_MESSAGE.NOT_SUBCLASS % (attribute_name, "prestans.types.String/Integer/Float"))

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint

    ## @brief validate method for %ParameterSet
    #
    # Since the introduction of ResponseFieldListParser, the parameter _response_field_list 
    # will be ignore, this is a prestans reserved parameter, and cannot be used by apps.
    # 
    # @param self The object pointer
    # @param request The request object to be validated
    #
    def validate(self, request):
        
        validated_parameter_set = self.__class__()

        # Inspects the attributes of a parameter set and tries to validate the input 
        for attribute_name, type_instance in self.__class__.__dict__.iteritems():
            
            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods 
                continue

            if attribute_name == "_response_field_list":
                # Prestans reserved word cannot be used
                raise ReservedWordException("_response_field_list")

            if not issubclass(type_instance.__class__, 
                              prestans.types.String) and not issubclass(type_instance.__class__, 
                              prestans.types.Float) and not issubclass(type_instance.__class__, 
                              prestans.types.Integer):
                
                # Must be a sub class of DataType 
                raise InvalidDataTypeException(ERROR_MESSAGE.NOT_SUBCLASS % (attribute_name, "prestans.types.String/Integer/Float"))

            try:
                # Get input from parameters, None type returned if nothing provided 
                validation_input = request.get(attribute_name)
                # Validate input based on data type rules, raises DataTypeValidationException if validation fails 
                validation_result = type_instance.validate(validation_input)
                # setattr 
                setattr(validated_parameter_set, attribute_name, validation_result)
            except prestans.types.DataTypeValidationException, exp:
                return None
            
        return validated_parameter_set

## @brief Parsers a well defined JSON protocol used by clients to request fields
#
# { 
#   field_name0: true, 
#   field_name1: false, 
#   collection_name0: true, 
#   collection_name1: false,
#   collection_name2: {
#       sub_field_name0: true,
#       sub_field_name1: false 
#   }
# }
#
class AttributeFilter(object):

    ## @brief wrapper for Model's get_attribute_filter
    #
    @classmethod
    def from_model(self, model_instance, default_value=False):
        
        if issubclass(model_instance.__class__, prestans.types.DataCollection):
            return model_instance.get_attribute_filter(default_value)

        raise TypeError("model_instance must be a sublcass of presatans.types.DataCollection, %s given" % 
                        (model_instance.__class__.__name__))

    ## @brief creates an attribute filter object, optionally populates from a dictionary of booleans
    #
    def __init__(self, from_dictionary=None):
        
        if from_dictionary:
            self._init_from_dictionary(from_dictionary)

    ## @brief check AttributeFilter conforms to the rules set by the template
    #
    # @private
    # @ returns AttributeFilter
    #
    # - If self, has attributes that template_fitler does not contain, throw Exception
    # - If sub list found, perform the first check
    # - If self has a value for an attribute, assign to final AttributeFilter
    # - If not found, assign value from template
    #
    def _conforms_to_template_filter(self, template_filter):

        if not isinstance(template_filter, self.__class__):
            raise TypeError("AttributeFilter can only check conformance against another template filter, %s provided" % 
                            (template_filter.__class__.__name__))

        # Keys from the template
        template_filter_keys = template_filter.keys()
        # Keys from the object itself
        this_filter_keys = self.keys()

        # 1. Check to see if the client has provided unwanted keys
        unwanted_keys = set(this_filter_keys) - set(template_filter_keys)
        if len(unwanted_keys) > 0:
            keys_string = string.join(unwanted_keys, " ")
            raise InvalidDataTypeException("_response_field_list has attributes (%s) that are not part of the template model" % keys_string)

        # 2. Make a attribute_filter that we send back
        evaluated_attribute_filter = AttributeFilter()

        # 3. Evaluate the differences between the two, with template_filter as the standard
        for template_key in template_filter_keys:

            if template_key in this_filter_keys:

                value = getattr(self, template_key)

                #If sub filter and boolean provided with of true, create default filter with value of true
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
        
    ## @brief returns a list of usable keys
    #
    def keys(self):

        keys = list()

        for attribute_name, type_instance in inspect.getmembers(self):

            if attribute_name.startswith('__') or inspect.ismethod(type_instance):
                # Ignore parameters with __ and if they are methods
                continue

            keys.append(attribute_name)

        return keys

    ## @brief contains a particular key, wrapper on self.__dict__.key
    #
    def has_key(self, key):
        return self.__dict__.has_key(key)

    ## @brief return True if attribute is a subfilter
    #
    def is_filter_at_key(self, key):

        if self.has_key(key) and isinstance(attribute_status, self.__class__):
            return True

        return False

    ## @brief returns True if an attribute is visible
    #
    # If attribute is an instance of AttributeFilter, it returns True if all attributes
    # of the sub filter are visible.
    #
    def is_attribute_visible(self, key):
        
        if self.has_key(key):
            attribute_status = getattr(self, key)
            if isinstance(attribute_status, bool) and attribute_status == True:
                return True
            elif isinstance(attribute_status, self.__class__) and \
            attribute_status.are_any_attributes_visible():
                return True

        return False

    ## @brief checks to see if any attributes are set to true
    #
    def are_any_attributes_visible(self):

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

    ## @brief checks to see if all attributes are set to true
    #
    def are_all_attributes_visible(self):

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

    ## @brief turns attribute filter object into python dictionary
    #
    def as_dict(self):

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


    ## @brief private helper to init values from a dictionary, wraps chidlren into AttributeFilter objects
    #
    # @private
    #
    def _init_from_dictionary(self, from_dictionary):
        
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


    ## @brief overrides setattr to allow only booleans or itself
    #
    def __setattr__(self, key, value):

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


## @brief %ParserRuleSet outlines parsing rules for a particular HTTP method
#
# Each RequestParser contains one or more %ParserRuleSet objects.
# It accepts an array of ParameterSet and prestans type or its subclass
# to parse the request body.
#
class ParserRuleSet(object):

    ## @brief Constructor
    #
    # @param self The object pointer
    # @param parameter_sets List of valid parameter sets for this ruleset
    # @param body_template Template for how the request body should be parsed
    # @param request_attribute_filter specifies a filter for incoming request bodies
    # @param response_attribute_filter_template must be of types.Model, provides a list 
    #        of fields the client expects in the response
    # @param response_attribute_filter_start_key a top level key
    #
    def __init__(self, 
                 parameter_sets=None, 
                 body_template=None, 
                 request_attribute_filter=None,
                 response_attribute_filter_template=None,
                 response_attribute_filter_start_key=None):

        if parameter_sets is None:
            self._parameter_sets = None
        else:
            if isinstance(parameter_sets, (list, tuple)):
                # Always makes sure that the parameter_set is iterable 
                self._parameter_sets = parameter_sets
            else:
                self._parameter_sets = [parameter_sets]

        self._body_template = body_template
        self._response_attribute_filter_template = response_attribute_filter_template
        self._request_attribute_filter = request_attribute_filter
        self._response_attribute_filter_start_key = response_attribute_filter_start_key


    ## @brief generates a blueprint to add to API discovery
    #
    def blueprint(self):

        parser_blueprint = dict()

        # Parameter Sets
        parameter_set_blueprints = []
        if self._parameter_sets is not None and len(self._parameter_sets) > 0:
            for parameter_set in self._parameter_sets:
                parameter_set_blueprints.append(parameter_set.blueprint())
        parser_blueprint['parameter_sets'] = parameter_set_blueprints

        # Incoming Body
        incoming_payload_blueprint = None
        if self._body_template is not None:
            incoming_payload_blueprint = self._body_template.blueprint()
        parser_blueprint['incoming_payload'] = incoming_payload_blueprint

        # Request Attribute Filter
        request_attr_filter_blueprint = None
        if self._request_attribute_filter is not None:
            request_attr_filter_blueprint = self._request_attribute_filter.as_dict()
        parser_blueprint['request_attr_filter'] = request_attr_filter_blueprint            

        # Response Attribute Filter Template
        response_attr_filter_template_blueprint = None
        if self._response_attribute_filter_template is not None:
            response_attr_filter_template_blueprint = self._response_attribute_filter_template.as_dict()
        parser_blueprint['response_attr_filter_template'] = response_attr_filter_template_blueprint            

        return parser_blueprint

    ## @brief parses serialized URL parameter to construct an attribute filter
    #
    # @param request handle to the original request
    #
    def _parse_attribute_filter(self, request):

        if not self._response_attribute_filter_template:
            # Not set hence, ignore this part of the parser 
            return None
        
        if not issubclass(self._response_attribute_filter_template.__class__, AttributeFilter):
            # Require body_templates to be a DataCollection, which are Models or Arrays 
            raise RequiresModelException("ParserRuleSet provided object of type %s as AttributeList, AttributeFitler expected" % 
                                         (self._body_template.__class__.__name__))

        evaluated_response_attribute_filter = None

        try:
            unserialized_field_list = request.get_unserialized_attribute_filter_list()
            if not unserialized_field_list:
                return None
        except:
            raise InvalidDataTypeException("_response_field_list data could not be unserialized, validate input")

        # At this point we have a validate attribute filter
        provided_filter = AttributeFilter(from_dictionary=unserialized_field_list)

        # Compare the entire filter from the root level if no sub key is provided
        compare_to_template_filter = self._response_attribute_filter_template

        # Otherwise check to see if the filter has that key
        if self._response_attribute_filter_start_key:
            if self._response_attribute_filter_template.is_filter_at_key(self._response_attribute_filter_start_key):
                compare_to_template_filter = getattr(self._response_attribute_filter_template, self._response_attribute_filter_start_key)
            else:
                raise TypeError("ParserRuleSet response_attribute_filter_start_key %s does not contain an AttributeFilter instance" % 
                    self._response_attribute_filter_start_key)

        # Should be able to compare the provided filter to 
        evaluated_response_attribute_filter = provided_filter._conforms_to_template_filter(self._response_attribute_filter_template)

        return evaluated_response_attribute_filter


    ## @brief returns the first matching %ParameterSet for a given request
    #
    # Only one ParameterSet is valid for each request. The first match is returned immediately.
    # If the application requires multiple combinations, they must create extra ParameterSets.
    #
    # ParameterSet matches are evaluated as OR at all times.
    #
    # If the application has chosen not to validate ParameterSets then this function returns None
    #
    # The following is called by RequestParser
    #
    # @param self The object pointer
    # @param request The request object to validate
    #
    def _parameter_set_for_request(self, request):
        if not self._parameter_sets:
            return None
            
        for parameter_set in self._parameter_sets:
            
            # Must be a ParameterSet, otherwise raise NotParameterSetObjectException 
            if not issubclass(parameter_set.__class__, ParameterSet):
                raise NotParameterSetObjectException(ERROR_MESSAGE.NOT_TYPE % 
                                                     (parameter_set.__class__.__name__, prestans.prestans.types.ParameterSet))

            # Ask parameter set to validate, if successful stop and return 
            try:

                validated_parameter_set = parameter_set.validate(request)
                
                if validated_parameter_set is not None:
                    return validated_parameter_set

            except prestans.types.DataTypeValidationException, exp:
                # Keep trying the others until we have given the others a chance as well 
                continue
                
        # Return None if none of them match, upto the handler to do what suits 
        return None
        
    ## @brief a parsed body of %DataType for a request
    #
    # @param request the prestans request
    # @param environ used by the upload handlers, to be deprecated
    #
    def _parsed_body_for_request(self, request, environ):
        # Parses the contents of the body 

        if not self._body_template:
            # Return none if body_template is not set, this means parsing is to be ignored 
            return None
            
        if not issubclass(self._body_template.__class__, 
                          prestans.types.DataCollection):
            # Require body_templates to be a DataCollection, which are Models or Arrays 
            raise RequiresDataCollectionException(ERROR_MESSAGE.NOT_COLLECTION % 
                                                  (self._body_template.__class__.__name__))
        
        parsed_body_model_instance = None

        try:

            if issubclass(self._body_template.__class__, prestans.types.DataCollection):

                # Raises exception on failure caught by __init__ 
                unserialized_body = request.get_unserialized_body()
                # Parsed body should be a model which is set into the Request Handler 
                parsed_body_model_instance = self._body_template.validate(unserialized_body, 
                                                                          self._request_attribute_filter)
                                
        except prestans.types.DataTypeValidationException, exp:
            raise BodyTemplateParseException(str(exp))
        
        return parsed_body_model_instance


## @brief %RequestParser defines the rules for parsing a REST request
# Generally defined using a list of ParameterSets and Models for each HTTP method. 
# 
# By default the rules for each method are set to None, if left that way the
# parser will ignore the input.
#
# %RequestParser rules are divided into URL, and Body rules.
#
class RequestParser(object):
    
    GET     = None
    POST    = None
    PUT     = None
    PATCH   = None
    DELETE  = None

    ## @brief parse method
    # 
    # If the implementing request parser does not specify a parser for a method, None is returned, 
    # this completely bypasses the parsing process.
    #
    # The implementing request parser must assign an instance of %ParserRuleSet for each HTTP method.
    #
    # %RequestParser will attempt use those rules to parse the input and assign them to the passed in
    # request object. It returns True or False.
    #
    # @param self The object pointer
    # @param response object
    # @param request The request to parse
    #
    def parse(self, request, response, environ):
        
        request_method = request.get_request_method()

        if not self.__class__.__dict__.has_key(request_method) or self.__class__.__dict__[request_method] is None:
            """ Default rule set is None, ignores parsing for Pameters and Body """
            return
        
        if not isinstance(self.__class__.__dict__[request_method], ParserRuleSet):
            """ Handles the developer not assinging an object of type ParserRuleSet """
            raise NotParserRuleSetObjectException(request_method + " does not have a valid ParserRuleSet")
        
        parser_rule_set = self.__class__.__dict__[request_method]

        """ Parse the field filter list """
        response.attribute_filter = parser_rule_set._parse_attribute_filter(request)

        """ Parse parameters or None if nothing matched """
        request.parameter_set = parser_rule_set._parameter_set_for_request(request)
        
        """ Parse request body """
        request.parsed_body_model = parser_rule_set._parsed_body_for_request(request, environ)
