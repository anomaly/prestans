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

        # test created from model
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        from_model = AttributeFilter.from_model(model_instance=MyModel())
        self.assertEquals(from_model.keys(), ["name", "tags"])

    def test_has_key(self):
        # from dict
        from_dict = AttributeFilter({"a": True, "b": False, "c": True})
        self.assertTrue(from_dict.has_key("a"))
        self.assertTrue(from_dict.has_key("b"))
        self.assertTrue(from_dict.has_key("c"))
        self.assertFalse(from_dict.has_key("d"))

        # from model
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        from_model = AttributeFilter.from_model(model_instance=MyModel())
        self.assertTrue(from_model.has_key("name"))
        self.assertTrue(from_model.has_key("tags"))
        self.assertFalse(from_model.has_key("age"))

    def test_is_filter_at_key(self):

        class SubModel(types.Model):
            name = types.String()

        class ModelWithSub(types.Model):
            tags = types.Array(element_template=types.String())
            sub_model = SubModel()

        attribute_filter = AttributeFilter.from_model(model_instance=ModelWithSub())
        self.assertTrue(attribute_filter.is_filter_at_key("sub_model"))
        self.assertFalse(attribute_filter.is_filter_at_key("tags"))

    def test_is_attribute_visible(self):

        dict_a = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": True,
                "b": False
            }
        }

        filter_a = AttributeFilter(dict_a)
        self.assertTrue(filter_a.is_attribute_visible("a"))
        self.assertFalse(filter_a.is_attribute_visible("b"))
        self.assertTrue(filter_a.is_attribute_visible("c"))
        self.assertFalse(filter_a.is_attribute_visible("d"))

        dict_b = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": True,
                "b": True
            }
        }

        filter_b = AttributeFilter(dict_b)
        self.assertTrue(filter_b.is_attribute_visible("a"))
        self.assertFalse(filter_b.is_attribute_visible("b"))
        self.assertTrue(filter_b.is_attribute_visible("c"))
        self.assertTrue(filter_b.is_attribute_visible("d"))

    def test_are_any_attributes_visible(self):
        some_visible = AttributeFilter({"a": True, "b": False, "c": True})
        self.assertTrue(some_visible.are_any_attributes_visible())

        none_visible = AttributeFilter({"a": False, "b": False, "c": False})
        self.assertFalse(none_visible.are_any_attributes_visible())

        sub_visible = AttributeFilter({"a": {"a": True}, "b": False, "c": True})
        self.assertTrue(sub_visible.are_any_attributes_visible())

    def test_are_all_attributes_visible(self):
        all_visible = AttributeFilter({"a": True, "b": True, "c": True})
        self.assertTrue(all_visible.are_all_attributes_visible())

        some_invisible = AttributeFilter({"a": True, "b": True, "c": False})
        self.assertFalse(some_invisible.are_all_attributes_visible())

        sub_visible = AttributeFilter({"a": {"a": True}, "b": True, "c": True})
        self.assertTrue(sub_visible.are_all_attributes_visible())

        sub_invisible = AttributeFilter({"a": {"a": False}, "b": True, "c": True})
        self.assertFalse(sub_invisible.are_all_attributes_visible())

    def test_set_all_attribute_values(self):
        mixed = {"a": True, "b": False, "c": True, "d": {"a": False}}
        attribute_filter = AttributeFilter(mixed)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertFalse(attribute_filter.is_attribute_visible("d"))
        attribute_filter.set_all_attribute_values(True)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertTrue(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertTrue(attribute_filter.is_attribute_visible("d"))
        attribute_filter.set_all_attribute_values(False)
        self.assertFalse(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertFalse(attribute_filter.is_attribute_visible("c"))
        self.assertFalse(attribute_filter.is_attribute_visible("d"))

    def test_as_dict(self):
        dict_a = {
            "a": False,
            "b": True,
            "c": {
                "a": True,
                "b": False
            }
        }
        filter_a = AttributeFilter(dict_a)
        self.assertEquals(filter_a.as_dict(), dict_a)

        dict_b = {
            "a": False,
            "b": {
                "a": False,
                "b": True
            },
            "c": False
        }
        filter_b = AttributeFilter(dict_b)
        self.assertEquals(filter_b.as_dict(), dict_b)

    @unittest.skip("currently broken")
    def test_init_from_dictionary(self):
        self.assertRaises(TypeError, AttributeFilter, "string")

        class MyModel(types.Model):
            name = types.String()

        self.assertRaises(TypeError, AttributeFilter, {"name": True}, template_model="string")

        attribute_filter = AttributeFilter({"name": True}, template_model=MyModel())

        self.assertRaises(TypeError, AttributeFilter, {"name": "string"})

    def test_setattr(self):
        source_dict = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": True,
                "b": False
            }
        }

        attribute_filter = AttributeFilter(source_dict)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertFalse(attribute_filter.is_attribute_visible("d"))
        attribute_filter.a = False
        attribute_filter.b = True
        attribute_filter.c = False
        attribute_filter.d = True
        self.assertFalse(attribute_filter.is_attribute_visible("a"))
        self.assertTrue(attribute_filter.is_attribute_visible("b"))
        self.assertFalse(attribute_filter.is_attribute_visible("c"))
        self.assertTrue(attribute_filter.is_attribute_visible("d"))

        self.assertRaises(TypeError, attribute_filter.a, "string")
        self.assertRaises(TypeError, attribute_filter.b, None)

    def test_from_model_boolean_array(self):
        boolean_array = types.Array(element_template=types.Boolean())
        AttributeFilter.from_model(model_instance=boolean_array, default_value=True)

    def test_from_model_float_array(self):
        float_array = types.Array(element_template=types.Float())
        AttributeFilter.from_model(model_instance=float_array, default_value=True)

    def test_from_model_integer_array(self):
        integer_array = types.Array(element_template=types.Integer())
        AttributeFilter.from_model(model_instance=integer_array, default_value=True)

    def test_from_model_string_array(self):
        string_array = types.Array(element_template=types.String())
        AttributeFilter.from_model(model_instance=string_array, default_value=True)
