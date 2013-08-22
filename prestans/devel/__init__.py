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


__all__ = ['gen', 'serve']

import argparse

import serve

class ArgParserFactory(object):

    #:
    #:
    #:
    def __init__(self):

        self._arg_parser = argparse.ArgumentParser(
            description="command line tools to compliment the prestans framework",
            epilog="pride is distributed by the prestans project <http://github.com/prestans/> under the the New BSD license."
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
            choices=['closure-model', 'closure-filter'],
            default='closure-model',
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
            help="namespace to use with template e.g prestans.demo.data"
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
        print self._args

    def _dispatch_build(self):
        print self._args

    def _dispatch_serve(self):
        server_config = serve.Configuration(self._args.config_path)
        dev_server = serve.DevServer(server_config)
        dev_server.run()
        