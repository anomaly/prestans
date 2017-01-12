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
"""
Contains development tools for prestans.
"""
__all__ = []

import argparse
import os

from prestans import exception
from prestans import __version__

class ArgParserFactory(object):
    """
    Argument parser factory.
    """

    def __init__(self):

        self._arg_parser = argparse.ArgumentParser(
            description="command line tools to compliment the prestans framework",
            epilog="pride is distributed by the prestans project <http://github.com/anomaly/prestans/> under the the New BSD license."
        )

        self._subparsers_handle = self._arg_parser.add_subparsers(dest="sub_command")

        self._add_generate_sub_commands()

        self._arg_parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + __version__
        )

    def parse(self):
        """
        Method to start the argument parsing.
        """
        return self._arg_parser.parse_args()

    def _add_generate_sub_commands(self):
        """
        Subcommands for generating models for usage by clients.
        Currently supports Google Closure.
        """

        gen_parser = self._subparsers_handle.add_parser(
            name="gen",
            help="generate client side model stubs, filters"
            )

        gen_parser.add_argument(
            "-t",
            "--template",
            choices=['closure.model', 'closure.filter'],
            default='closure.model',
            required=True,
            dest="template",
            help="template to use for client side code generation"
            )

        gen_parser.add_argument(
            "-m",
            "--model",
            required=True,
            dest="model_path",
            help="path to models description file"
            )


        gen_parser.add_argument(
            "-o",
            "--output",
            default=".",
            dest="output",
            help="output path for generated code"
            )

        gen_parser.add_argument(
            "-n",
            "--namespace",
            required=True,
            dest="namespace",
            help="namespace to use with template e.g prestans.data.model"
            )

        gen_parser.add_argument(
            "-fn",
            "--filter-namespace",
            required=False,
            default=None,
            dest="filter_namespace",
            help="filter namespace to use with template e.g prestans.data.filter"
            )

class CommandDispatcher(object):
    """
    Processes the user's commands.
    """

    def __init__(self, args):
        self._args = args

    def dispatch(self):
        """
        Start processing the user's commands.
        """

        if self._args.sub_command == "gen":
            self._dispatch_gen()

    def _dispatch_gen(self):
        """
        Process the generate subset of commands.
        """

        if not os.path.isdir(self._args.output):
            raise exception.Base("%s is not a writeable directory" % self._args.output)

        if not os.path.isfile(self._args.model_path):
            raise exception.Base("failed to read model file %s" % self._args.model_path)

        import prestans.devel.gen
        preplate = prestans.devel.gen.Preplate(
            template_type=self._args.template,
            model_file=self._args.model_path,
            namespace=self._args.namespace,
            filter_namespace=self._args.filter_namespace,
            output_directory=self._args.output)

        preplate.run()
        