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
import sys
import yaml
import importlib

import blessings

from voluptuous import Schema, Required, All, Length, Range, MultipleInvalid

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

import prestans.devel.exception

class Configuration:

    _SCHEMA = {
        Required('name'): str,
        Required('version'): float,
        Required('bind'): str,
        Required('port'): int,
        'append_path': [str],
        'environ': [{
            Required('key'): str,
            Required('value'): str
        }],
        'static': [{
            Required('url'): str,
            Required('path'): str
        }],
        Required('default_app'): str,
        Required('sub_modules'): All([{
            Required('url'): str,
            Required('module'): str,
        }], Length(min=1)),
    }

    def __init__(self, config_path):
        
        try:
            self.base_path = os.path.dirname(config_path)
            parsed_config = yaml.load(file(config_path))
        except IOError, exp:
            raise prestans.devel.exception.Base("[error] unable to read configuration at %s" % config_path)

        try:
            schema = Schema(Configuration._SCHEMA)
            validated_config = schema(parsed_config)
        except MultipleInvalid, exp:
            raise prestans.devel.exception.Base("[error/config] %s" % str(exp), 2)

        #: Make configuration vars into instance vars

        self.name = validated_config['name']
        self.version = validated_config['version']
        self.bind = validated_config['bind']
        self.port = validated_config['port']

        self.append_path = validated_config['append_path']
        self.environ = validated_config['environ']
        self.static = validated_config['static']
        self.default_app = validated_config['default_app']
        self.handlers = validated_config['sub_modules']

class DevServer(object):

    def __init__(self, config):
        self._config = config
        self._terminal = blessings.Terminal()

        #: Append paths
        self._append_paths()
        self._add_environment_vars()

    def run(self):

        _static_file_map = self._create_static_map()
        _handlers = self._add_handlers()

        #: handover to werkzeug
        run_simple(self._config.bind, self._config.port, _handlers,\
         static_files=_static_file_map, use_reloader=True, use_debugger=True, use_evalex=True)

    def _append_paths(self):    

        for path in self._config.append_path:

            module_path = os.path.join(self._config.base_path, path)

            if os.path.exists(module_path):
                sys.path.append(module_path)
            else:
                print "[{t.red}path{t.normal}] ignoring non-existant include path %s".format(t=self._terminal)\
                 % module_path

    def _add_environment_vars(self):

        for entry in self._config.environ:

            key = entry['key']
            value = entry['value']

            os.environ[key] = value

    def _create_static_map(self):

        static_map = dict()

        for entry in self._config.static:

            url = entry['url']
            path = entry['path']

            resource_path = os.path.join(self._config.base_path, path)
            static_map[url] = resource_path

        return static_map

    def _add_handlers(self):

        sub_maps = dict()
        default_application = None

        #: Default application
        default_module = self._config.default_app
        try:
            module_name, wsgi_app = default_module.rsplit(".", 1)
            imported_module = importlib.import_module(module_name)
            default_application = getattr(imported_module, wsgi_app)
        except (ImportError, AttributeError), exp:
            raise prestans.devel.exception.Base("[error] default_app module %s doesn't exists" % default_module)

        #: Sub modules
        for entry in self._config.handlers:
            
            url = entry['url']
            module = entry['module']

            module_name, wsgi_app = module.rsplit(".", 1)
            imported_module = importlib.import_module(module_name)

            try:
                sub_maps[url] = getattr(imported_module, wsgi_app)
            except AttributeError, exp:
                raise prestans.devel.exception.Base("[error] module %s doesn't exists" % entry)

        dispatched_application = DispatcherMiddleware(default_application, sub_maps)

        return dispatched_application
