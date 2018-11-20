import unittest

from prestans.parser import AttributeFilter
from prestans import types


class ThirdLevel(types.Model):
    third = types.String()


class SecondLevel(types.Model):
    second = types.String()
    third_level = types.Array(element_template=ThirdLevel())


class FirstLevel(types.Model):
    first = types.String()
    second_level = types.Array(element_template=SecondLevel())


class AttributeFilterImmutableInit(unittest.TestCase):

    def test_init(self):
        pass


class AttributeFilterImmutableIsAttributeVisible(unittest.TestCase):

    def test_correct_values_returned(self):

        attribute_filter = AttributeFilter.from_model(FirstLevel(), False)
        immutable_filter = attribute_filter.as_immutable()

        self.assertFalse(immutable_filter.is_attribute_visible("first"))
        self.assertFalse(immutable_filter.is_attribute_visible("second_level"))
        self.assertFalse(immutable_filter.second_level.is_attribute_visible("second"))
        self.assertFalse(immutable_filter.second_level.is_attribute_visible("third_level"))
        self.assertFalse(immutable_filter.second_level.third_level.is_attribute_visible("third"))

        attribute_filter.second_level.second = True
        immutable_filter = attribute_filter.as_immutable()

        self.assertFalse(immutable_filter.is_attribute_visible("first"))
        self.assertTrue(immutable_filter.is_attribute_visible("second_level"))
        self.assertTrue(immutable_filter.second_level.is_attribute_visible("second"))
        self.assertFalse(immutable_filter.second_level.is_attribute_visible("third_level"))
        self.assertFalse(immutable_filter.second_level.third_level.is_attribute_visible("third"))

        attribute_filter.second_level.third_level.third = True
        immutable_filter = attribute_filter.as_immutable()

        self.assertFalse(immutable_filter.is_attribute_visible("first"))
        self.assertTrue(immutable_filter.is_attribute_visible("second_level"))
        self.assertTrue(immutable_filter.second_level.is_attribute_visible("second"))
        self.assertTrue(immutable_filter.second_level.is_attribute_visible("third_level"))
        self.assertTrue(immutable_filter.second_level.third_level.is_attribute_visible("third"))



