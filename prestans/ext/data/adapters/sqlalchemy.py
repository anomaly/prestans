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
__all__ = ['ModelAdapter']

from prestans.ext.data import adapters


def adapt_persistent_instance(persistent_object, target_rest_class=None, attribute_filter=None):
    """
    Wrapper on adapters.adapt_persistent_instance for SQLAlchemy
    """
    return adapters.adapt_persistent_instance(persistent_object, target_rest_class, attribute_filter)


def adapt_persistent_collection(persistent_collection, target_rest_class=None, attribute_filter=None):
    """
    Wrapper on adapters.adapt_persistent_collection for SQLAlchemy
    """
    return adapters.adapt_persistent_collection(persistent_collection, target_rest_class, attribute_filter)
    

class ModelAdapter(adapters.ModelAdapter):

    def __init__(self, rest_model_class, persistent_model_class):
        import logging
        logger = logging.getLogger("prestans")
        logger.warn("direct use of %s has been deprecated please use %s instead" % (
            self.__module__ + "." + self.__class__.__name__,
            adapters.ModelAdapter.__module__ + "." + adapters.ModelAdapter.__name__
        ))
        super(ModelAdapter, self).__init__(rest_model_class, persistent_model_class)
