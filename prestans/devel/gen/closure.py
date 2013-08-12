import os
import re

import prestans.devel.gen
import prestans.devel.gen.templates.closure.filter
import prestans.devel.gen.templates.closure.model

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

        self._type = blueprint['type']

        #Basic types
        if self._type == 'string':
            self._required = blueprint['constraints']['required']
            self._min_length = blueprint['constraints']['min_length']
            self._max_length = blueprint['constraints']['max_length']
        elif self._type == 'integer':
            self._required = blueprint['constraints']['required']
        elif self._type == 'float':
            self._required = blueprint['constraints']['required']
        elif self._type == 'boolean':
            self._required = blueprint['constraints']['required']
        #Complex types
        elif self._type == 'model':
            self._required = blueprint['constraints']['required']
            self._model_template = blueprint['constraints']['model_template']
        elif self._type == 'array':
            self._required = blueprint['constraints']['required']
            self._element_template = blueprint['constraints']['element_template']


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
        return self._required

    #array
    @property
    def is_model(self):
        return False

class Model(object):

    def __init__(self, model_file, namespace, output_directory):
        self._model_file = model_file
        self._namespace = namespace
        self._output_directory = output_directory
        self._template = prestans.devel.gen.templates.closure.model

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            model_name = model_blueprint['constraints']['model_template']
            attributes = list()

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                attributes.append(attribute)

            #write out template
            filename = '%s.js' % (model_name)
            output_file = open(os.path.join(self._output_directory, filename), 'w+')

            output_file.write(self._template.render(namespace=self._namespace, name=model_name, attributes=attributes))
            output_file.close()

            print "%-30s -> %-30s" %(model_name, model_name)

        return 0

class Filter(object):

    def __init__(self, template_engine, model_file, namespace, output_directory):
        self._model_file = model_file
        self._namespace = namespace
        self._output_directory = output_directory
        self._template_engine = template_engine
        self._template = self._template_engine.get_template("closure/filter.tpl")

    def run(self):

        inspector = prestans.devel.gen.Inspector(model_file=self._model_file)
        blueprints = inspector.inspect()

        for model_blueprint in blueprints:

            model_name = model_blueprint['constraints']['model_template']
            attributes = list()

            for field_name, field_blueprint in model_blueprint['fields'].iteritems():

                attribute = AttributeMetaData(name=field_name, blueprint=field_blueprint)
                attributes.append(attribute)

            #write out template
            filename = '%s.js' % (model_name)
            output_file = open(os.path.join(self._output_directory, filename), 'w+')

            output_file.write(self._template.render(namespace=self._namespace, name=model_name, attributes=attributes))
            output_file.close()

            print "%-30s -> %s.js" % (model_name, model_name)



        return 0
