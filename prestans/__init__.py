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

__all__ = ['types', 'parsers', 'handlers', 'serializers', 'rest', 'auth', 'cache']

## @package prestans Core prestans package
#
# @defgroup exception Exceptions
# @defgroup constants Constants
# @defgroup decorators Decorators 
# @defgroup adapters Adapters
#
# @defgroup appengine AppEngine Specific Implementation of prestans providers
#

__version__ = '1.0'
__authors__ = ['Devraj Mukherjee', 'Bradley Mclain']

## @brief Constants to produce consistent error messages for all Data Types.
#
# Exclusively used in exception handling.
#
# @ingroup constants
#
class ERROR_MESSAGE(object):

    NO_DIRECT_USE               = '%s should not be used directly, use a subclass'
    
    NO_KEY                      = 'attribute %s not defined in %s'
    ARRAY_TYPE_ERROR            = 'array expects type %s, given %s'
    
    CANT_PARSE_VALUE            = 'value %s is not acceptable for type %s'
    NOT_SUBCLASS                = '%s is not a subclass of %s'
    NOT_ACCEPTABLE              = 'does not have an acceptable value, no default values set'
    LESS_THAN_MINIMUM           = 'value is less than expected minimum of %i'
    MORE_THAN_MAXIMUM           = 'value is greater than expected maximum of %i'
    LESS_THAN_MIN_LENGTH        = 'length is smaller than expected length of %i'
    MORE_THAN_MAX_LENGTH        = 'length is greater than allowed length of %i'
    NOT_IN_CHOICES              = 'value is not in list of allowed choices'

    NOT_TYPE                    = '%s not of type %s'
    NOT_ITERABLE                = 'provided value to collection is not iterable'
    NOT_COLLECTION              = '%s is not a prestans.types.DataCollection, bodies must be collections'
    NOT_MODEL                   = '%s is not a prestans.types.Model'
    
    NOT_PYTHON_ARRAY            = 'failed to serialize collection (array) to python type'
    
    REQUIRED_PARAMETER_MISSING  = 'required parameter missing'
    DOESNOT_MATCH_STRING_FORMAT = '%s does not match the expected string format'
    
    ADAPTER_NOT_REGISTERED      = 'No adapter registered for Class %s'
    
    INVALID_META_VALUE          = 'Invalid value for meta attribute %s in DataType %s'
    