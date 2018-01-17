import unittest

from prestans.parser import AttributeFilter
from prestans import types


class AttributeFilterTest(unittest.TestCase):

    def test_init(self):

        # check from dictionary
        from_dict = AttributeFilter({"true": True, "false": False})
        self.assertTrue(from_dict.true)
        self.assertFalse(from_dict.false)

        # todo: check template model

        # # check is_array_scalar
        # self.assertFalse(AttributeFilter().is_array_scalar)
        # self.assertTrue(AttributeFilter(is_array_scalar=True).is_array_scalar)
        # self.assertFalse(AttributeFilter(is_array_scalar=False).is_array_scalar)

        # check keyword args
        keywords_args = AttributeFilter({"true": True, "changed_to_false": True}, changed_to_false=False)
        self.assertTrue(keywords_args.true)
        self.assertFalse(keywords_args.changed_to_false)

    def test_from_model(self):

        # check that non data collection raises exception
        self.assertRaises(TypeError, AttributeFilter.from_model, model_instance="string")

        # check that array scalar returns filter todo: work out how to further test this
        array_scalar = AttributeFilter.from_model(types.Array(element_template=types.String()))
        self.assertTrue(isinstance(array_scalar, AttributeFilter))

        # check that a model is constructed correctly and default values work
        class MyModel(types.Model):
            name = types.String()
            age = types.Integer()
            tags = types.Array(element_template=types.String())

        default = AttributeFilter.from_model(model_instance=MyModel())
        self.assertFalse(default.name)
        self.assertFalse(default.age)
        self.assertFalse(default.tags)

        default_false = AttributeFilter.from_model(model_instance=MyModel(), default_value=False)
        self.assertFalse(default_false.name)
        self.assertFalse(default_false.age)
        self.assertFalse(default_false.tags)

        default_true = AttributeFilter.from_model(model_instance=MyModel(), default_value=True)
        self.assertTrue(default_true.name)
        self.assertTrue(default_true.age)
        self.assertTrue(default_true.tags)

        # check keyword args
        keyword_args = AttributeFilter.from_model(model_instance=MyModel(), age=True)
        self.assertFalse(keyword_args.name)
        self.assertTrue(keyword_args.age)
        self.assertFalse(keyword_args.tags)

        self.assertRaises(KeyError, AttributeFilter.from_model, model_instance=MyModel(), missing=True)

    def test_conforms_to_template_filter(self):
        pass

    def test_keys(self):
        # test created from dict
        from_dict = AttributeFilter({"a": True, "b": False, "c": True})
        from_dict_keys = from_dict.keys()
        self.assertEquals(from_dict_keys, ["a", "b", "c"])

        # todo: test created from model

    def test_has_key(self):
        # from dict
        from_dict = AttributeFilter({"a": True, "b": False, "c": True})
        self.assertTrue(from_dict.has_key("a"))
        self.assertTrue(from_dict.has_key("b"))
        self.assertTrue(from_dict.has_key("c"))
        self.assertFalse(from_dict.has_key("d"))

        # from model

    def test_is_filter_at_key(self):
        pass

    def test_is_attribute_visible(self):
        pass

    def test_are_any_attributes_visible(self):
        pass

    def test_are_all_attributes_visible(self):
        pass

    def test_set_all_attribute_values(self):
        pass

    def test_as_dict(self):
        pass

    def test_init_from_dictionary(self):
        pass

    def test_setattr(self):
        pass


def test_from_model_boolean_array():
    boolean_array = types.Array(element_template=types.Boolean())
    AttributeFilter.from_model(model_instance=boolean_array, default_value=True)


def test_from_model_float_array():
    float_array = types.Array(element_template=types.Float())
    AttributeFilter.from_model(model_instance=float_array, default_value=True)


def test_from_model_integer_array():
    integer_array = types.Array(element_template=types.Integer())
    AttributeFilter.from_model(model_instance=integer_array, default_value=True)


def test_from_model_string_array():
    string_array = types.Array(element_template=types.String())
    AttributeFilter.from_model(model_instance=string_array, default_value=True)
