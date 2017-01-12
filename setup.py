#!/usr/bin/env python
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

from setuptools import setup, find_packages

from prestans import __version__

setup(name='prestans',
    version=__version__,
    description='A WSGI compliant REST micro-framework',
    url='https://github.com/anomaly/prestans.git',
    long_description="""
    Prestans is a REST micro-framework built right on top of WSGI, designed to perform and co-exists with other middleware and frameworks that you employ. 

    Our target audience are developers building large REST backends for use with pure Ajax (using a framework like Google Closure) or mobile applications. 

    Prestans is designed for you to "take as much or as little" as you like.

    Features:

    - Built right on top of WSGI, designed ground up to cooperate with other frameworks
    - Strong representative of REST philosophies leveraging HTTP headers and verbs
    - Support for multiple dialects, including formalised patterns for binary content 
    - Handlers maps HTTP verbs to implemented class methods, complimented  with custom 
    request parser and response writer (built on top of WebOb)
    - Unforgivingly strict parsing of requests and responses to ensure data integrity
    - Helper methods to ease transformation of persistent objects to REST responses
    - Pluggable integration to authentication

    """,
    download_url='https://github.com/anomaly/prestans/archive/' + __version__ + '.tar.gz',
    license='New BSD',
    author='Anomaly Software',
    author_email='support@anomaly.net.au',
    maintainer='Anomaly Software',
    maintainer_email='support@anomaly.net.au',
    platforms=['any'],
    scripts=['prestans/bin/pride'],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['WebOb==1.4',],
    extras_require={
        "devel": ["Jinja2"]
    },
    include_package_data = True
)
