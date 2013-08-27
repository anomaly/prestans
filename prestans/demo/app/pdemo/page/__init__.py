#!/usr/bin/env python
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

__all__ = ['handlers']

import os
import webapp2

from jinja2 import Environment, FileSystemLoader, Template

from pdemo import config

## @brief incompasses basic required functionality for all static handlers
class Base(webapp2.RequestHandler):

    # def commit(self):
    #     try:
    #         self.db_session.commit()
    #     except:
    #         self.db_session.rollback()

    ## @brief override dispatch to ensure SQL Alchemy session creation
    # def dispatch(self):
    #     self.db_session = yours2take.db.Session()
    #     super(BaseHandler, self).dispatch()
    #     yours2take.db.Session.remove()

    ## @brief Uses the Jinja2 environment to render a tempalte with values
    def render_template(self, template_name, template_values=[]):
        template_env = self.get_template_env()
        template = template_env.get_template("%s.html" % template_name)
        self.response.out.write(template.render(template_values))
    
    ## @brief Jinja templates, consider using webapp2 jinja utilities for this
    def get_template_env(self):
    	script_path = os.path.abspath(os.path.dirname(__file__))
        template_path = os.path.join(script_path, "..", "..", "..", config.get('pdemo', 'template_path'))

        return Environment(loader=FileSystemLoader(template_path))