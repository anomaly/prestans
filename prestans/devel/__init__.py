# -*- coding: utf-8 -*-
#
#  prestans, A WSGI compliant REST micro-framework
#  http://prestans.org
#
#  Copyright (c) 2015, Anomaly Software Pty Ltd.
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


__all__ = ['gen', 'serve']

import argparse
import os

#import prestans.devel.serve
#import prestans.devel.gen
import exception

class ArgParserFactory(object):

    #:
    #:
    #:
    def __init__(self):

        self._arg_parser = argparse.ArgumentParser(
            description="command line tools to compliment the prestans framework",
            epilog="pride is distributed by the prestans project <http://github.com/anomaly/prestans/> under the the New BSD license."
        )

        subparsers_handle = self._arg_parser.add_subparsers(dest="sub_command")

        self._add_generate_build_commands(subparsers_handle)
        self._add_generate_sub_commands(subparsers_handle)
        self._add_server_sub_commands(subparsers_handle)

    #:
    #: public message to fire argparser
    #:
    def parse(self):
        return self._arg_parser.parse_args()

    #:
    #: build subcommand
    #:
    def _add_generate_build_commands(self, subparsers_handle):

        gen_parser = subparsers_handle.add_parser(
            name="build",
            help="builds deployable javascript, css and server"
            )

        build_sub_parser = gen_parser.add_subparsers(dest="build-sub-commands")

        #:
        #: build a distribution
        #:
        build_sub_parser.add_parser(
            name="dist",
            help="builds distributable application"
            )

        #:
        #: Javascript
        #:
        build_sub_parser.add_parser(
            name="js",
            help="builds distributable javascript"
            )

        #:
        #: CSS
        #:
        build_sub_parser.add_parser(
            name="css",
            help="builds distributable css"
            )

    #:
    #: gen subcommand
    #:
    def _add_generate_sub_commands(self, subparsers_handle):

        gen_parser = subparsers_handle.add_parser(
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



    #:
    #: server subcommand
    #:
    #: --config path to configuration file
    #:
    def _add_server_sub_commands(self, subparsers_handle):

        server_parser = subparsers_handle.add_parser(
            name="serve",
            help="runs a local HTTP WSGI server for your prestans project"
            )

        server_parser.add_argument(
            "-c",
            "--config",
            default="./devserver.yaml",
            dest="config_path",
            help="path to prestans devserver configuration"
            )


class CommandDispatcher:

    def __init__(self, args):
        self._args = args

    def dispatch(self):
        
        if self._args.sub_command == "gen":
            self._dispatch_gen()
        elif self._args.sub_command == "build":
            self._dispatch_build()
        elif self._args.sub_command == "serve":
            self._dispatch_serve()

    def _dispatch_gen(self):

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

    def _dispatch_build(self):
        print self._args

    def _dispatch_serve(self):
        import prestans.devel.serve
        server_config = prestans.devel.serve.Configuration(self._args.config_path)
        dev_server = serve.DevServer(server_config)
        dev_server.run()
        