__all__ = ['closure', 'templates']

import inspect
import jinja2
import os
import sys

import prestans.devel.gen.closure
import prestans.types

class Inspector(object):

    def __init__(self, model_file):
        self._model_file = model_file

    def inspect(self):

        blueprints = list()

        try:
            sys.path.append(os.path.dirname(self._model_file))
            models = __import__("models", globals(), locals(), [])
        except ImportError, import_error:
            print "\npreplate requires "
            sys.exit(1)

        for name, type_instance in models.__dict__.iteritems():
            if name.startswith('__') or inspect.ismethod(type_instance) or not inspect.isclass(type_instance) or not issubclass(type_instance, prestans.types.Model):
                continue

            blueprint = type_instance().blueprint()
            blueprints.append(blueprint)


        return blueprints

class Preplate(object):

    def __init__(self, template_type, model_file, namespace, output_directory):
        
        self._template_type = template_type
        self._model_file = model_file
        self._namespace = namespace
        self._output_directory = output_directory
        loader = jinja2.PackageLoader('prestans', 'devel/gen/templates')
        self._template_engine = jinja2.Environment(trim_blocks=True, loader=loader)
        self._template_engine.globals["isinstance"] = isinstance
        self._template_engine.globals["list"] = list

    def run(self):

        template = None
        if self._template_type == "closure.model":
            template = prestans.devel.gen.closure.Model(template_engine=self._template_engine, model_file=self._model_file, namespace=self._namespace, output_directory=self._output_directory)
        elif self._template_type == "closure.filter":
            template = prestans.devel.gen.closure.Filter(template_engine=self._template_engine, model_file=self._model_file, namespace=self._namespace, output_directory=self._output_directory)

        if template is None:
            return 1
        
        return template.run()