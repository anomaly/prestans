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
            model_python_file = os.path.split(self._model_file)[1:][0]
            namespace = model_python_file.split(".")[0]
            models = __import__(namespace, globals(), locals(), [])
        except ImportError as import_error:
            print ("\nFailed to process %s, %s" % (self._model_file, import_error))
            sys.exit(1)

        for name, type_instance in iter(models.__dict__.items()):
            if name.startswith('__') or inspect.ismethod(type_instance) or not inspect.isclass(type_instance) or\
             not issubclass(type_instance, prestans.types.Model):
                continue

            blueprint = type_instance().blueprint()
            for field_name, field_blueprint in iter(blueprint['fields'].items()):
                field_blueprint['map_name'] = type_instance().attribute_rewrite_map()[field_name]
            blueprints.append(blueprint)

        return blueprints


class Preplate(object):

    def __init__(self, template_type, model_file, namespace, filter_namespace, output_directory):
        
        self._template_type = template_type
        self._model_file = model_file
        self._namespace = namespace
        self._filter_namespace = filter_namespace
        self._output_directory = output_directory

        from jinja2 import Environment
        from jinja2 import PackageLoader

        loader = PackageLoader('prestans', 'devel/gen/templates')
        self._template_engine = Environment(trim_blocks=True, loader=loader)
        self._template_engine.globals["isinstance"] = isinstance
        self._template_engine.globals["list"] = list

    @property
    def template_type(self):
        return self._template_type

    @property
    def model_file(self):
        return self._model_file

    @property
    def namespace(self):
        return self._namespace

    @property
    def filter_namespace(self):
        return self._filter_namespace

    @property
    def output_directory(self):
        return self._output_directory

    @property
    def template_engine(self):
        return self._template_engine

    def run(self):

        template = None
        if self._template_type == "closure.model":
            from prestans.devel.gen.closure import Model
            template = Model(
                template_engine=self._template_engine,
                model_file=self._model_file,
                namespace=self._namespace,
                filter_namespace=self._filter_namespace,
                output_directory=self._output_directory
            )
        elif self._template_type == "closure.filter":
            from prestans.devel.gen.closure import Filter
            template = Filter(
                template_engine=self._template_engine,
                model_file=self._model_file,
                namespace=self._namespace,
                output_directory=self._output_directory
            )

        if template is None:
            return 1
        
        return template.run()
