#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.org
#
#  Copyright (c) 2014, Anomaly Software Pty Ltd.
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
import string
import signal
import getpass
import base64
import argparse

__version_info__ = (2, 0)
__version__ = '.'.join(str(v) for v in __version_info__)

def ctrlc_handler(signal, frame):
    print ""
    sys.exit(2)

def main():

    signal.signal(signal.SIGINT, ctrlc_handler)

    #: Parse the command 
    parser_factory = prestans.devel.ArgParserFactory()
    args = parser_factory.parse()

    try:
        #: Dispatch the command to the right module
        command_dispatcher = prestans.devel.CommandDispatcher(args)
        return command_dispatcher.dispatch()
    except prestans.devel.exception.Base, exp:
        print ("%s\n"  % exp)
        return exp.error_code


if __name__ == "__main__":

    directory = os.path.dirname(__file__)
    prestans_path = os.path.join(directory, "..", "..")

    #:
    #: While in development attempt to import prestans from top dir
    #:
    if os.path.isdir(prestans_path):
        sys.path.insert(0, prestans_path)

    import prestans.devel
    import prestans.devel.exception

    sys.exit(main())