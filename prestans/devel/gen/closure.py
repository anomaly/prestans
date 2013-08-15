import os
import re

import prestans.devel.gen
import prestans.devel.gen.templates.closure.filter
import prestans.devel.gen.templates.closure.model
import prestans.types

def udl_to_cc(text, ignoreFirst=False):
    text = text.lower()
    camel_case = re.sub(r"_(.)", lambda pat: pat.group(1).upper(), text)
    if not ignoreFirst:
        camel_case = camel_case[0:1].upper()+camel_case[1:]
    return camel_case

class AttributeMetaData(object):

    #used for
    def __str__(self):
        return "%s" % (self._name)

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

        self._type = blueprint['type']

        #Basic types
        if self._type == 'string':
            self._required = blueprint['constraints']['required']
            self._min_length = blueprint['constraints']['min_length']
            self._max_length = blueprint['constraints']['max_length']
            self._default = blueprint['constraints']['default']
            self._choices = blueprint['constraints']['choices']
            self._format = blueprint['constraints']['format']
        elif self._type == 'integer':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._minimum = blueprint['constraints']['minimum']
            self._maximum = blueprint['constraints']['maximum']
            self._choices = blueprint['constraints']['choices']
        elif self._type == 'float':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
            self._minimum = blueprint['constraints']['minimum']
            self._maximum = blueprint['constraints']['maximum']
            self._choices = blueprint['constraints']['choices']
        elif self._type == 'boolean':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
        elif self._type == 'datetime':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
        elif self._type == 'date':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
        elif self._type == 'time':
            self._required = blueprint['constraints']['required']
            self._default = blueprint['constraints']['default']
        #Complex types
        elif self._type == 'model':
            self._required = blueprint['constraints']['required']
            self._model_template = blueprint['constraints']['model_template']
        elif self._type == 'array':
            self._required = blueprint['constraints']['required']
            self._min_length = blueprint['constraints']['min_length']
            self._max_length = blueprint['constraints']['max_length']

            element_template = blueprint['constraints']['element_template']

            if element_template['type'] == 'model':
                self._element_template_is_model = True
                self._element_template = element_template['constraints']['model_template']
            else:
                self._element_template_is_model = False
                self._element_template = element_template['type'].capitalize()


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
    def type(self):
        return self._type

    @property
    def required(self):
        if self._required:
            return "true"
        else:
            return "false"

    @property
    def default(self):
        #dates are check first otherwise string will catch them
        if self._default == prestans.types.DateTime.CONSTANT.NOW:
            return "prestans.types.DateTime.NOW"
        elif self._default == prestans.types.Date.CONSTANT.TODAY:
            return "prestans.types.Date.TODAY"
        elif self._default == prestans.types.Time.CONSTANT.NOW:
            return "prestans.types.Time.NOW"
        elif self._default is None:
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

    @property
    def choices(self):
        if self._choices is None:
            return "null"
        else:
            return self._choices

    #string and array
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

    #model
    @property
    def model_template(self):
        return self._model_template

    #array
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
        if attribute.type == 'array':
            dependency = "%s.%s" % (self._namespace, attribute.element_template)
        elif attribute.type == 'model':
            dependency = "%s.%s" % (self._namespace, attribute.model_template)

        if dependency is not None and dependency not in self._dependencies:
            self._dependencies.append(dependency)

    def add_model_dependency(self, attribute):

        dependency = None
        if attribute.type == 'array' and attribute.element_template_is_model:
            dependency = "%s.%s" % (self._namespace, attribute.element_template)
        elif attribute.type == 'array':
            dependency = "%s.%s" % ("prestans.types", attribute.element_template)
        elif attribute.type == 'model':
            dependency = "%s.%s" % (self._namespace, attribute.model_template)
        else:
            dependency = "prestans.types.%s" % (attribute.type.capitalize())

        if dependency is not None and dependency not in self._dependencies:
            self._dependencies.append(dependency)

    #used in filters
    def add_attribute_string(self, attribute):
        if attribute.type == 'model':
            self._attribute_string += "this.%s_.anyFieldsEnabled() || " % (attribute.ccif)
        elif attribute.type == 'array':
            self._attribute_string += "this.%s_.anyFieldsEnabled() || " % (attribute.ccif)
        else:
            self._attribute_string += "this.%s_ || " % (attribute.ccif)

    @property
    def attribute_string(self):
        return self._attribute_string[:-4]

class Model(Base):

    def __init__(self, template_engine, model_file, namespace, output_directory):
    
        Base.__init__(self, template_engine, model_file, namespace, output_directory)
        self._template = self._template_engine.get_template("closure/model.jinja")

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            model_name = model_blueprint['constraints']['model_template']
            attributes = list()
            self._dependencies = list()

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                attributes.append(attribute)

                self.add_model_dependency(attribute)

            #write out template
            filename = '%s.js' % (model_name)
            output_file = open(os.path.join(self._output_directory, filename), 'w+')

            output_file.write(self._template.render(namespace=self._namespace, name=model_name, attributes=attributes, dependencies=self._dependencies))
            output_file.close()

            print "%-30s -> %s.%s.js" %(model_name, self._namespace, model_name)

        return 0

class Filter(Base):

    def __init__(self, template_engine, model_file, namespace, output_directory):

        Base.__init__(self, template_engine, model_file, namespace, output_directory)
        self._template = self._template_engine.get_template("closure/filter.jinja")

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            model_name = model_blueprint['constraints']['model_template']
            attributes = list()

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                attributes.append(attribute)

                self.add_filter_dependency(attribute)
                self.add_attribute_string(attribute)

            #write out template
            filename = '%s.js' % (model_name)
            output_file = open(os.path.join(self._output_directory, filename), 'w+')

            output_file.write(self._template.render(namespace=self._namespace, name=model_name, attributes=attributes, dependencies=self._dependencies, attribute_string=self.attribute_string))
            output_file.close()

            print "%-30s -> %s.%s.js" % (model_name, self._namespace, model_name)



        return 0
