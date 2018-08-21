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
from prestans.types import Array, Date, DateTime, Float, Integer, String


class ParameterSet(object):
    """
    ParameterSet is a group of prestans.types that are expected as GET parameters

    ParameterSet defines rules and patterns in which they are acceptable.
    while ParserRuleSet is responsible for running the parse mechanism.
    """

    def getmembers(self):
        """
        :return: list of members as name, type tuples
        :rtype: list
        """
        return filter(
            lambda m: not m[0].startswith("__") and not inspect.isfunction(m[1]) and not inspect.ismethod(m[1]),
            inspect.getmembers(self.__class__)
        )

    def blueprint(self):
        """
        blueprint support, returns a partial dictionary
        """

        blueprint = dict()
        blueprint['type'] = "%s.%s" % (self.__module__, self.__class__.__name__)

        # Fields
        fields = dict()

        # inspects the attributes of a parameter set and tries to validate the input
        for attribute_name, type_instance in self.getmembers():

            # must be one of the following types
            if not isinstance(type_instance, String) and \
               not isinstance(type_instance, Float) and \
               not isinstance(type_instance, Integer) and \
               not isinstance(type_instance, Date) and \
               not isinstance(type_instance, DateTime) and \
               not isinstance(type_instance, Array):
                raise TypeError("%s should be instance of\
                 prestans.types.String/Integer/Float/Date/DateTime/Array" % attribute_name)

            if isinstance(type_instance, Array):
                if not isinstance(type_instance.element_template, String) and \
                   not isinstance(type_instance.element_template, Float) and \
                   not isinstance(type_instance.element_template, Integer):
                    raise TypeError("%s should be instance of \
                        prestans.types.String/Integer/Float/Array" % attribute_name)

            fields[attribute_name] = type_instance.blueprint()

        blueprint['fields'] = fields
        return blueprint

    def validate(self, request):
        """
        validate method for %ParameterSet

        Since the introduction of ResponseFieldListParser, the parameter _response_field_list
        will be ignored, this is a prestans reserved parameter, and cannot be used by apps.

        :param request: The request object to be validated
        :type request: webob.request.Request
        :return The validated parameter set
        :rtype: ParameterSet
        """

        validated_parameter_set = self.__class__()

        # Inspects the attributes of a parameter set and tries to validate the input
        for attribute_name, type_instance in self.getmembers():

            #: Must be one of the following types
            if not isinstance(type_instance, String) and \
               not isinstance(type_instance, Float) and \
               not isinstance(type_instance, Integer) and \
               not isinstance(type_instance, Date) and \
               not isinstance(type_instance, DateTime) and \
               not isinstance(type_instance, Array):
                raise TypeError("%s should be of type \
                    prestans.types.String/Integer/Float/Date/DateTime/Array" % attribute_name)

            if issubclass(type_instance.__class__, Array):

                if not isinstance(type_instance.element_template, String) and \
                   not isinstance(type_instance.element_template, Float) and \
                   not isinstance(type_instance.element_template, Integer):
                    raise TypeError("%s elements should be of \
                        type prestans.types.String/Integer/Float" % attribute_name)

            try:

                #: Get input from parameters
                #: Empty list returned if key is missing for getall
                if issubclass(type_instance.__class__, Array):
                    validation_input = request.params.getall(attribute_name)
                #: Key error thrown if key is missing for getone
                else:
                    try:
                        validation_input = request.params.getone(attribute_name)
                    except KeyError:
                        validation_input = None

                #: Validate input based on data type rules,
                #: raises DataTypeValidationException if validation fails
                validation_result = type_instance.validate(validation_input)

                setattr(validated_parameter_set, attribute_name, validation_result)

            except exception.DataValidationException as exp:
                raise exception.ValidationError(
                    message=str(exp),
                    attribute_name=attribute_name,
                    value=validation_input,
                    blueprint=type_instance.blueprint())

        return validated_parameter_set
