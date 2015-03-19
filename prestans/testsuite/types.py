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

import unittest

import prestans.types
import prestans.exception

class StringTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._string = prestans.types.String(
            default="orange",
            min_length=1,
            max_length=20,
            choices=['orange','mango','banana'],
            )

    def test_default(self):
        self.assertEqual(self._string._default, "orange", "Check default value")

    def test_length(self):
        pass

    def test_regex_format(self):
        pass

    def test_choices(self):
        pass

    def test_encoding(self):
        pass

    def tearDown(self):
        self._string = None

class IntegerTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._integer = prestans.types.Integer(
            default=1,
            minimum=1,
            maximum=20,
            )

    def test_default(self):
        self.assertEqual(self._integer.validate(1), 1)

    def test_minimum(self):
        self.assertRaises(prestans.exception.LessThanMinimumError, self._integer.validate(-1))

    def text_maximum(self):
        self.assertRaises(prestans.exception.MoreThanMaximumError, self._integer.validate(21))

    def test_choices(self):
        self.assertRaises(prestans.exception.InvalidChoiceError, self._integer.validate(2))

    def tearDown(self):
        self._integer = None


class FloatTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._float = prestans.types.Float(
            default=1.0,
            minimum=1.0,
            maximum=20.0,
            )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._float = None

class BooleanTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._boolean = prestans.types.Boolean(
            default=True,
            )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._boolean = None

class DataURLFileTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._data_url_file = prestans.types.DataURLFile(
            allowed_mime_types=[],
            )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._data_url_file = None


class DateTimeTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._datetime = prestans.types.DateTime(
            default=True,
            )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._datetime = None

class DateTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._date = prestans.types.Date(
            default=True,
            )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._date = None

class TimeTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._time = prestans.types.Time(
            default=True,
            )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._date = None

class ArrayTypeUnitTest(unittest.TestCase):

    def setUp(self):        
        self._string_array = prestans.types.Array(
            element_template=prestans.types.String()
        )
        self._integer_array = prestans.types.Array(
            element_template=prestans.types.Integer()
        )

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def test_append(self):
        pass

    def tearDown(self):
        self._array = None

class ModelTypeUnitTest(unittest.TestCase):

    class TestModel(prestans.types.Model):

        string = prestans.types.String(required=True, max_length=10)

    def setUp(self):
        
        self._model = ModelTypeUnitTest.TestModel()

    def test_default(self):
        pass

    def test_choices(self):
        pass

    def tearDown(self):
        self._model = None

if __name__ == '__main__':
    unittest.main()