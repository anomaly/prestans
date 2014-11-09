#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2012, Anomaly Software Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
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
#  DISCLAIMED. IN NO EVENT SHALL Anomaly Software BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from distutils.core import setup

setup(name='prestans',
      version='1.2.1',
      description='A WSGI compliant REST micro-framework',
      long_description='',
      download_url='',
      license='New BSD',
      classifiers=[
      	'Environment :: Web Environment',
      	'Intended Audience :: Developers',
      	'Operating System :: MacOS :: MacOS X',
      	'Operating System :: POSIX',
      	'Programming Language :: Python'
      ],
      author='Devraj Mukherjee, Bradley Mclain',
      author_email='devraj@gmail.com',
      url='https://github.com/prestans',
      scripts=['prestans/bin/preplate', 'prestans/bin/preplate2', 'prestans/bin/presh'],
      packages=['prestans', 'prestans.ext', 'prestans.ext.data', 'prestans.ext.data.adapters'],
      install_requires=['webob==1.2.3',],
     )
