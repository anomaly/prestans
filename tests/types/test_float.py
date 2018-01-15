import unittest

from prestans import exception
from prestans.types import Float


class FloatUnitTest(unittest.TestCase):

    def test_types(self):
        types = Float()
        self.assertRaises(exception.ParseFailedError, types.validate, "string")

    def test_required(self):
        required = Float(required=True)
        self.assertRaises(exception.RequiredAttributeError, required.validate, None)
        self.assertEqual(required.validate(1.0), 1.0)

    def test_not_required(self):
        not_required = Float(required=False)
        self.assertEqual(not_required.validate(1.0), 1.0)
        self.assertEqual(not_required.validate(None), None)

    def test_default(self):
        default = Float(default=6.0)
        self.assertEqual(default.validate(5.0), 5.0)
        self.assertEqual(default.validate(None), 6.0)

    def test_minimum(self):
        positive_range = Float(minimum=1.0, maximum=5.0)
        self.assertRaises(exception.LessThanMinimumError, positive_range.validate, 0.0)
        self.assertRaises(exception.LessThanMinimumError, positive_range.validate, 0.5)
        self.assertEqual(positive_range.validate(1.0), 1.0)
        self.assertEqual(positive_range.validate(1.5), 1.5)

        negative_range = Float(minimum=-5.0, maximum=-1.0)
        self.assertRaises(exception.LessThanMinimumError, negative_range.validate, -7.0)
        self.assertRaises(exception.LessThanMinimumError, negative_range.validate, -6.0)
        self.assertEqual(negative_range.validate(-5.0), -5.0)
        self.assertEqual(negative_range.validate(-4.0), -4.0)

    def text_maximum(self):
        positive_range = Float(minimum=1.0, maximum=5.0)
        self.assertEqual(positive_range.validate(4.0), 4.0)
        self.assertEqual(positive_range.validate(4.5), 4.5)
        self.assertEqual(positive_range.validate(5.0), 5.0)
        self.assertRaises(exception.MoreThanMaximumError, positive_range.validate, 6.5)
        self.assertRaises(exception.MoreThanMaximumError, positive_range.validate, 7.0)

        negative_range = Float(minimum=-5.0, maximum=-1.0)
        self.assertEqual(negative_range.validate(-3.0), -3.0)
        self.assertEqual(negative_range.validate(-2.0), -2.0)
        self.assertEqual(negative_range.validate(-1.0), -1.0)
        self.assertRaises(exception.MoreThanMaximumError, negative_range.validate, -0.5)
        self.assertRaises(exception.MoreThanMaximumError, negative_range.validate, 0.0)

    def test_choices(self):
        choices = Float(choices=[1.0, 3.0])
        self.assertRaises(exception.InvalidChoiceError, choices.validate, 0.0)
        self.assertRaises(exception.InvalidChoiceError, choices.validate, 2.0)
        self.assertRaises(exception.InvalidChoiceError, choices.validate, 4.0)
        self.assertEqual(choices.validate(1.0), 1.0)
        self.assertEqual(choices.validate(3.0), 3.0)
