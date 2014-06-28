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

__all__ = ['JSONSerializer', 'XMLSerializer']


## @package prestans.serializers Provides serializing classes to convert from transfer format to prestans format
#

## @brief Raised if the Python to Serialization fails for the data
# 
# @ingroup exception
#
class SerializationFailedException(Exception):
    pass

## @brief Raised if the serialized format to Python types fails
#
# @ingroup exception
#
class UnserializationFailedException(Exception):
    pass
    

## @brief Defines a protocol for how data can be serizalied and uniserialized
#
# @todo Implement the base loads, dumps and content type method which should throw an exception if used directly
#
class Serializer(object):
    
    ## @brief loads method for serializer
    #
    # @param self The object pointer
    # @param input_string
    #
    @classmethod
    def loads(self, input_string):
        raise Exception("No direct use allowed")
    
    ## @brief dumps method for serializer
    #
    # @param self The object pointer
    # @param serializable_object
    #
    @classmethod
    def dumps(self, serializable_object):
        raise Exception("No direct use allowed")
    
    ## @brief Content type for serializer   
    #
    @classmethod
    def get_content_type(self):
        raise Exception("No direct use allowed")

## @brief Provider for JSON based serializer
#
class JSONSerializer(Serializer):
    
    ## @brief loads method for JSON serializer
    #
    # @param self The object pointer
    # @param input_string
    #
    @classmethod
    def loads(self, input_string):
        import json
        parsed_json = None
        try:
            parsed_json = json.loads(input_string)
        except Exception, exp:
            raise UnserializationFailedException('Input Body data is not valid JSON')
            
        return parsed_json

    ## @brief dumps method for JSON serializer
    #
    # @param self The object pointer
    # @param serializable_object
    #
    @classmethod
    def dumps(self, serializable_object):
        import json
        return json.dumps(serializable_object)
        
    @classmethod
    def get_content_type(self):
        return 'application/json'
        

## @brief Provider for YAML based serialization
#
#  requires PyYAML
#
class YAMLSerializer(Serializer):

    @classmethod
    def loads(self, input_string):
        import yaml
        return yaml.load(input_string)
    
    @classmethod
    def dumps(self, serializable_object):
        import yaml
        return yaml.dump(serializable_object)
        
    @classmethod
    def get_content_type(self):
        return 'text/yaml'
