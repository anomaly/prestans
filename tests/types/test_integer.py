import unittest

from prestans.exception import InvalidChoiceError
from prestans.exception import LessThanMinimumError
from prestans.exception import MoreThanMaximumError
from prestans.exception import ParseFailedError
from prestans.exception import RequiredAttributeError
from prestans.types import Integer


class IntegerUnitTest(unittest.TestCase):

    def test_invalid_types(self):
        types = Integer()
        self.assertRaises(ParseFailedError, types.validate, "string")

    def test_required(self):
        required = Integer(required=True)
        self.assertRaises(RequiredAttributeError, required.validate, None)
        self.assertEqual(required.validate(1), 1)

    def test_not_required(self):
        not_required = Integer(required=False)
        self.assertEqual(not_required.validate(1), 1)
        self.assertEqual(not_required.validate(None), None)

    def test_default(self):
        integer = Integer()
        self.assertIsNone(integer.default)

        integer = Integer(default=6)
        self.assertEquals(integer.default, 6)
        self.assertEqual(integer.validate(None), 6)
        self.assertEqual(integer.validate(5), 5)

    def test_minimum(self):
        integer = Integer()
        self.assertIsNone(integer.minimum)

        positive_range = Integer(minimum=1, maximum=5)
        self.assertEquals(positive_range.minimum, 1)
        self.assertEquals(positive_range.maximum, 5)
        self.assertRaises(LessThanMinimumError, positive_range.validate, -2)
        self.assertRaises(LessThanMinimumError, positive_range.validate, -1)
        self.assertRaises(LessThanMinimumError, positive_range.validate, 0)
        self.assertEqual(positive_range.validate(1), 1)
        self.assertEqual(positive_range.validate(2), 2)
        self.assertEqual(positive_range.validate(3), 3)

        negative_range = Integer(minimum=-5, maximum=-1)
        self.assertEquals(negative_range.minimum, -5)
        self.assertEquals(negative_range.maximum, -1)
        self.assertRaises(LessThanMinimumError, negative_range.validate, -8)
        self.assertRaises(LessThanMinimumError, negative_range.validate, -7)
        self.assertRaises(LessThanMinimumError, negative_range.validate, -6)
        self.assertEqual(negative_range.validate(-5), -5)
        self.assertEqual(negative_range.validate(-4), -4)
        self.assertEqual(negative_range.validate(-3), -3)

        zero_min_range = Integer(minimum=0)
        self.assertRaises(LessThanMinimumError, zero_min_range.validate, -1)
        self.assertEqual(zero_min_range.validate(0), 0)

    def text_maximum(self):
        integer = Integer()
        self.assertIsNone(integer.maximum)

        positive_range = Integer(minimum=1, maximum=5)
        self.assertEqual(positive_range.validate(0), 0)
        self.assertEqual(positive_range.validate(3), 3)
        self.assertEqual(positive_range.validate(4), 4)
        self.assertEqual(positive_range.validate(5), 5)
        self.assertRaises(MoreThanMaximumError, positive_range.validate, 6)
        self.assertRaises(MoreThanMaximumError, positive_range.validate, 7)
        self.assertRaises(MoreThanMaximumError, positive_range.validate, 8)

        negative_range = Integer(minimum=-5, maximum=-1)
        self.assertEqual(negative_range.validate(-3), -3)
        self.assertEqual(negative_range.validate(-2), -2)
        self.assertEqual(negative_range.validate(-1), -1)
        self.assertRaises(MoreThanMaximumError, negative_range.validate, 0)
        self.assertRaises(MoreThanMaximumError, negative_range.validate, 1)
        self.assertRaises(MoreThanMaximumError, negative_range.validate, 2)

        zero_max_range = Integer(maximum=0)
        self.assertEqual(zero_max_range.validate(-1), -1)
        self.assertRaises(MoreThanMaximumError, zero_max_range.validate, 1)

    def test_choices(self):
        integer = Integer()
        self.assertIsNone(integer.choices)

        integer = Integer(choices=[1,5])
        self.assertRaises(InvalidChoiceError, integer.validate, 3)
        self.assertRaises(InvalidChoiceError, integer.validate, 4)
        self.assertEqual(integer.validate(1), 1)
        self.assertEqual(integer.validate(5), 5)
