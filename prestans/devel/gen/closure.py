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

import os
import re

import prestans.devel.gen
import prestans.types


def udl_to_cc(text, ignore_first=False):
    text = text.lower()
    camel_case = re.sub(r"_(.)", lambda pat: pat.group(1).upper(), text)
    if not ignore_first:
        camel_case = camel_case[0:1].upper()+camel_case[1:]
    return camel_case


class BasicTypeElementTemplate(object):

    def __init__(self, blueprint_type, blueprint):
        
        self._blueprint_type = blueprint_type
        self._required = None
        self._default = None
        self._minimum = None
        self._maximum = None
        self._min_length = None
        self._max_length = None
        self._choices = None
        self._format = None
        self._trim = None

        if self._blueprint_type == "string":
            self._required = blueprint['required']
            self._min_length = blueprint['min_length']
            self._max_length = blueprint['max_length']
            self._default = blueprint['default']
            self._choices = blueprint['choices']
            self._format = blueprint['format']
            self._trim = blueprint['trim']
            self._client_class_name = "String"
        elif self._blueprint_type == 'integer':
            self._required = blueprint['required']
            self._default = blueprint['default']
            self._minimum = blueprint['minimum']
            self._maximum = blueprint['maximum']
            self._choices = blueprint['choices']
            self._client_class_name = "Integer"
        elif self._blueprint_type == 'float':
            self._required = blueprint['required']
            self._default = blueprint['default']
            self._minimum = blueprint['minimum']
            self._maximum = blueprint['maximum']
            self._choices = blueprint['choices']
            self._client_class_name = "Float"
        elif self._blueprint_type == 'boolean':
            self._required = blueprint['required']
            self._default = blueprint['default']
            self._client_class_name = "Boolean"

        if self._required is None:
            self._required = True

    @property
    def blueprint_type(self):
        return self._blueprint_type

    @property
    def client_class_name(self):
        return self._client_class_name

    @property
    def required(self):
        if self._required:
            return "true"
        else:
            return "false"

    @property
    def trim(self):
        if self._trim:
            return "true"
        else:
            return "false"

    @property
    def default(self):
        #dates are check first otherwise string will catch them
        #if self._default == prestans.types.DateTime.CONSTANT.NOW:
        #    return "prestans.types.DateTime.NOW"
        #elif self._default == prestans.types.Date.CONSTANT.TODAY:
        #    return "prestans.types.Date.TODAY"
        #elif self._default == prestans.types.Time.CONSTANT.NOW:
        #    return "prestans.types.Time.NOW"
        if self._default is None:
            return "null"
        elif type(self._default) == str:
            return "\"%s\"" % (self._default)
        elif type(self._default) == bool:
            if self._default:
                return "true"
            else:
                return "false"
        else:
            return self._default

    @property
    def minimum(self):
        if self._minimum is None:
            return "null"
        else:
            return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            return "null"
        else:
            return self._maximum

    # string and array
    @property
    def min_length(self):
        if self._min_length is None:
            return "null"
        else:
            return self._min_length

    @property
    def max_length(self):
        if self._max_length is None:
            return "null"
        else:
            return self._max_length

    @property
    def format(self):
        if self._format is None:
            return "null"

        formatted = self._format.replace("\\", "\\\\")
        return "\"%s\"" % formatted

    @property
    def choices(self):
        if self._choices is None:
            return "null"
        else:
            return self._choices


class AttributeMetaData(object):

    def __init__(self, name, blueprint):
        self._name = name
        self._blueprint = blueprint
        self._required = None
        self._default = None
        self._minimum = None
        self._maximum = None
        self._min_length = None
        self._max_length = None
        self._choices = None
        self._format = None
        self._trim = None

        self._blueprint_type = blueprint['type']
        self._map_name = blueprint['map_name']

        # basic types
        if self._blueprint_type == 'string':
            self._required = blueprint['constraints']['required']
            self._min_length = blueprint['constraints']['min_length']
            self._max_length = blueprint['constraints']['max_length']
            self._default = blueprint['constraints']['default']
            self._choices = blueprint['constraints']['choices']
            self._format = blueprint['constraints']['format']
            self._trim = blueprint['constraints']['trim']
            self._client_class_name = "String"
        elif self._blueprint_type == 'integer':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._minimum = blueprint['constraints']['minimum']
            self._maximum = blueprint['constraints']['maximum']
            self._choices = blueprint['constraints']['choices']
            self._client_class_name = "Integer"
        elif self._blueprint_type == 'float':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._minimum = blueprint['constraints']['minimum']
            self._maximum = blueprint['constraints']['maximum']
            self._choices = blueprint['constraints']['choices']
            self._client_class_name = "Float"
        elif self._blueprint_type == 'boolean':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._client_class_name = "Boolean"
        elif self._blueprint_type == 'datetime':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._timezone = blueprint['constraints']['timezone']
            self._utc = blueprint['constraints']['utc']
            self._client_class_name = "DateTime"
        elif self._blueprint_type == 'date':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._client_class_name = "Date"
        elif self._blueprint_type == 'time':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._client_class_name = "Time"
        elif self._blueprint_type == 'data_url_file':
            self._required = blueprint['constraints']['required']
            self._allowed_mime_types = blueprint['constraints']['allowed_mime_types']
            self._client_class_name = "DataURLFile"
        # complex types
        elif self._blueprint_type == 'model':
            self._required = blueprint['constraints']['required']
            self._model_template = blueprint['constraints']['model_template']
            self._client_class_name = "Model"
        elif self._blueprint_type == 'array':
            self._required = blueprint['constraints']['required']
            self._min_length = blueprint['constraints']['min_length']
            self._max_length = blueprint['constraints']['max_length']
            self._client_class_name = "Array"

            element_template = blueprint['constraints']['element_template']

            if element_template['type'] == 'model':
                self._element_template_is_model = True
                self._element_template = element_template['constraints']['model_template']
            else:
                self._element_template_is_model = False
                self._element_template = BasicTypeElementTemplate(
                    blueprint_type=element_template['type'],
                    blueprint=element_template['constraints']
                )

    @property
    def name(self):
        return self._name
    
    @property
    def cc(self):
        return udl_to_cc(self._name)

    @property
    def ccif(self):
        return udl_to_cc(self._name, True)

    @property
    def blueprint_type(self):
        return self._blueprint_type

    @property
    def client_class_name(self):
        return self._client_class_name

    @property
    def map_name(self):
        return self._map_name

    @property
    def required(self):
        if self._required:
            return "true"
        else:
            return "false"

    @property
    def trim(self):
        if self._trim:
            return "true"
        else:
            return "false"

    @property
    def timezone(self):
        if self._timezone:
            return "true"
        else:
            return "false"

    @property
    def utc(self):
        if self._utc:
            return "true"
        else:
            return "false"

    @property
    def allowed_mime_types(self):
        return self._allowed_mime_types

    @property
    def default(self):
        # dates are checked first otherwise string will catch them
        if self._default == prestans.types.DateTime.CONSTANT.NOW:
            return "prestans.types.DateTime.NOW"
        elif self._default == prestans.types.Date.CONSTANT.TODAY:
            return "prestans.types.Date.TODAY"
        elif self._default == prestans.types.Time.CONSTANT.NOW:
            return "prestans.types.Time.NOW"
        elif self._default is None:
            return "null"
        elif type(self._default) == str:
            return "\"%s\"" % self._default
        elif type(self._default) == bool:
            if self._default:
                return "true"
            else:
                return "false"
        else:
            return self._default

    @property
    def format(self):
        if self._format is None:
            return "null"

        formatted = self._format.replace("\\", "\\\\")
        return "\"%s\"" % formatted

    @property
    def minimum(self):
        if self._minimum is None:
            return "null"
        else:
            return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            return "null"
        else:
            return self._maximum

    @property
    def choices(self):
        if self._choices is None:
            return "null"
        else:
            return self._choices

    # string and array
    @property
    def min_length(self):
        if self._min_length is None:
            return "null"
        else:
            return self._min_length

    @property
    def max_length(self):
        if self._max_length is None:
            return "null"
        else:
            return self._max_length

    # model
    @property
    def model_template(self):
        return self._model_template

    # array
    @property
    def element_template(self):
        return self._element_template

    @property
    def element_template_is_model(self):
        return self._element_template_is_model


class Base(object):

    def __init__(self, template_engine, model_file, namespace, output_directory):
        self._template_engine = template_engine
        self._model_file = model_file
        self._namespace = namespace
        self._output_directory = output_directory
        self._dependencies = list()
        self._attribute_string = ""

    def add_filter_dependency(self, attribute):

        dependency = None
        if attribute.blueprint_type == 'array' and attribute.element_template_is_model:
            dependency = "%s.%s" % (self._namespace, attribute.element_template)
        elif attribute.blueprint_type == 'model':
            dependency = "%s.%s" % (self._namespace, attribute.model_template)

        if dependency is not None and dependency not in self._dependencies:
            self._dependencies.append(dependency)

    def add_model_dependency(self, attribute):

        dependency = None
        if attribute.blueprint_type == 'array' and attribute.element_template_is_model:
            dependency = "%s.%s" % (self._namespace, attribute.element_template)
        elif attribute.blueprint_type == 'array':
            dependency = "%s.%s" % ("prestans.types", attribute.element_template.client_class_name)
        elif attribute.blueprint_type == 'model':
            dependency = "%s.%s" % (self._namespace, attribute.model_template)
        else:
            dependency = "prestans.types.%s" % attribute.client_class_name

        if dependency is not None and dependency not in self._dependencies:
            self._dependencies.append(dependency)

    # used in filters
    def add_attribute_string(self, attribute):
        if attribute.blueprint_type == 'model':
            self._attribute_string += "this.%s_.anyFieldsEnabled() || " % attribute.ccif
        elif attribute.blueprint_type == 'array' and attribute.element_template_is_model:
            self._attribute_string += "this.%s_.anyFieldsEnabled() || " % attribute.ccif
        else:
            self._attribute_string += "this.%s_ || " % attribute.ccif

    @property
    def attribute_string(self):
        return self._attribute_string[:-4]


class Model(Base):

    def __init__(self, template_engine, model_file, namespace, filter_namespace, output_directory):
    
        Base.__init__(self, template_engine, model_file, namespace, output_directory)
        self._filter_namespace = filter_namespace
        self._template = self._template_engine.get_template("closure/model/model.jinja")

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            model_name = model_blueprint['constraints']['model_template']
            attributes = list()
            self._dependencies = list()
            self._attribute_string = ""

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)                
                attributes.append(attribute)

                self.add_model_dependency(attribute)

            self._dependencies.sort()

            # write out template
            filename = '%s.js' % model_name
            output_file = open(os.path.join(self._output_directory, filename), 'w+')

            project_namespace = self._namespace.split(".")[0]

            output_file.write(self._template.render(
                namespace=self._namespace,
                project=project_namespace,
                filter_namespace=self._filter_namespace,
                name=model_name,
                attributes=attributes,
                dependencies=self._dependencies
            ))
            output_file.close()

            print ("%-30s -> %s.%s.js" %(model_name, self._namespace, model_name))

        print ("\nGenerated %i model(s)" % len(blueprints))

        return 0


class Filter(Base):

    def __init__(self, template_engine, model_file, namespace, output_directory):

        Base.__init__(self, template_engine, model_file, namespace, output_directory)
        self._template = self._template_engine.get_template("closure/filter/filter.jinja")

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            model_name = model_blueprint['constraints']['model_template']
            attributes = list()
            self._dependencies = list()
            self._attribute_string = ""

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                attributes.append(attribute)

                self.add_filter_dependency(attribute)
                self.add_attribute_string(attribute)

            self._dependencies.sort()

            # write out template
            filename = '%s.js' % model_name
            output_file = open(os.path.join(self._output_directory, filename), 'w+')

            project_namespace = self._namespace.split(".")[0]

            output_file.write(self._template.render(
                namespace=self._namespace,
                project=project_namespace,
                name=model_name,
                attributes=attributes,
                dependencies=self._dependencies,
                attribute_string=self.attribute_string
            ))
            output_file.close()

            print ("%-30s -> %s.%s.js" % (model_name, self._namespace, model_name))

        print ("\nGenerated %i filter(s)" % len(blueprints))

        return 0
