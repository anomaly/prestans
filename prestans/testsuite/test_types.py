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
        
        self.required = prestans.types.String(required=True)
        self.not_required = prestans.types.String(required=False)
        self.type = prestans.types.String()
        self.default = prestans.types.String(default="orange")
        self.length = prestans.types.String(min_length=5, max_length=7)
        self.format = prestans.types.String(format="[0-9]{2}[a-z]{5}[0-9]{3}")
        self.choices = prestans.types.String(choices=["apple", "banana"])

    def test_required(self):
        self.assertRaises(prestans.exception.RequiredAttributeError, self.required.validate, None)
        self.assertRaises(prestans.exception.RequiredAttributeError, self.required.validate, "")
        self.assertEqual(self.required.validate("apple"), "apple")

        self.assertEqual(self.not_required.validate("apple"), "apple")
        self.assertEqual(self.not_required.validate(""), "")
        self.assertEqual(self.not_required.validate(None), None)

    def test_type(self):
        self.assertEqual(self.type.validate("orange"), "orange")
        self.assertEqual(self.type.validate(1), "1")
        self.assertEqual(self.type.validate(1.0), "1.0")
        self.assertEqual(self.type.validate(True), "True")

    def test_default(self):
        self.assertEqual(self.default.validate(None), "orange")
        self.assertEqual(self.default.validate("apple"), "apple")

    def test_min_length(self):
        self.assertRaises(prestans.exception.MinimumLengthError, self.length.validate, "1234")
        self.assertEqual(self.length.validate("12345"), "12345")

    def test_max_length(self):
        self.assertRaises(prestans.exception.MaximumLengthError, self.length.validate, "123456789")
        self.assertEqual(self.length.validate("1234567"), "1234567")

    def test_format(self):
        self.assertRaises(prestans.exception.InvalidFormatError, self.format.validate, "cat")
        self.assertRaises(prestans.exception.InvalidFormatError, self.format.validate, "ab45678as")
        self.assertEqual(self.format.validate("12abcde123"), "12abcde123")
        self.assertEqual(self.format.validate("89uwxyz789"), "89uwxyz789")

    def test_choices(self):
        self.assertRaises(prestans.exception.InvalidChoiceError, self.choices.validate, "orange")
        self.assertRaises(prestans.exception.InvalidChoiceError, self.choices.validate, "grape")

        self.assertEqual(self.choices.validate("apple"), "apple")
        self.assertEqual(self.choices.validate("banana"), "banana")

    def test_encoding(self):
        pass

    def tearDown(self):
        pass

class IntegerTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._integer = prestans.types.Integer(
            default=1,
            minimum=1,
            maximum=5
        )

        self._choices = prestans.types.Integer(
            choices=[1,5]
        )

    def test_default(self):
        self.assertEqual(self._integer.validate(None), 1)

    def test_minimum(self):
        self.assertRaises(prestans.exception.LessThanMinimumError, self._integer.validate, -1)

    def text_maximum(self):
        self.assertRaises(prestans.exception.MoreThanMaximumError, self._integer.validate, 6)

    def test_choices(self):
        self.assertRaises(prestans.exception.InvalidChoiceError, self._choices.validate, 3)

    def tearDown(self):
        pass


class FloatTypeUnitTest(unittest.TestCase):

    def setUp(self):
        
        self._float = prestans.types.Float(
            default=1.0,
            minimum=1.0,
            maximum=20.0,
        )

        self._choices = prestans.types.Float(
            choices=[1.0, 3.0]
        )

    def test_default(self):
        self.assertEqual(self._float.validate(1.0), 1.0)

    def test_minimum(self):
        self.assertRaises(prestans.exception.LessThanMinimumError, self._float.validate, 0.5)

    def text_maximum(self):
        self.assertRaises(prestans.exception.MoreThanMaximumError, self._float.validate, 21.5)

    def test_choices(self):
        self.assertRaises(prestans.exception.InvalidChoiceError, self._choices.validate, 0.0)
        self.assertRaises(prestans.exception.InvalidChoiceError, self._choices.validate, 2.0)
        self.assertRaises(prestans.exception.InvalidChoiceError, self._choices.validate, 4.0)

    def tearDown(self):
        pass

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
        pass

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
        pass


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
        pass

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
        pass

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
        pass

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
        pass

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
        pass

if __name__ == '__main__':
    unittest.main()