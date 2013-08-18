# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2013, Eternity Technologies Pty Ltd.
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

import os
import sys
import yaml

from blessings import Terminal
from voluptuous import Schema

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

class Configuration:

	_SCHEMA = {
		'name': str,
		'version': float,
		'bind': str,
		'port': int,
		'append_path': str,
		'environ': str,
		'static': str,
		'handlers': str
	}

	def __init__(self, config_path):
		
		parsed_config = yaml.load(file(config_path))
		schema = Schema(Configuration._SCHEMA)

		self.name = parsed_config['name']
		self.version = parsed_config['version']
		self.bind = parsed_config['bind']
		self.port = parsed_config['port']

class DevServer(object):

    def __init__(self, config):
    	self._config = config
    	self._terminal = Terminal()

    def run(self):

    	print "{t.bold}%s{t.normal} ({t.bold}%s{t.normal}) prestans dev server running at; {t.bold}http://%s:%i{t.normal}"\
    	.format(t=self._terminal) \
    	% (self._config.name, self._config.version, self._config.bind, self._config.port)

    def _append_paths(self):
    	pass

    def _create_static_map(self):
    	pass

    def _add_environment_vars(self):
    	pass

    def _add_handlers(self):
    	pass


# sys.path.append('ext/')
# sys.path.append('app/')

# from werkzeug.serving import run_simple
# from werkzeug.wsgi import DispatcherMiddleware

# def application(environ, start_response):

# 	environ['gridlet_config'] = 'conf/app_devel.cfg'

# 	import entry

# 	dispatched_application = DispatcherMiddleware(entry.frontend_wsgi_app, {
# 	    '/api': entry.backend_wsgi_app
# 	})

# 	return dispatched_application(environ, start_response)

# if __name__ == "__main__":
# 	run_simple('localhost', 8000, application, static_files= {'/assets': 'static/assets'},
#                use_reloader=True, use_debugger=True, use_evalex=True)