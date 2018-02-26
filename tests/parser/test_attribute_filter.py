import unittest

from prestans import exception
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
        kwargs = AttributeFilter({"true": True, "changed_to_false": True}, changed_to_false=False)
        self.assertTrue(kwargs.true)
        self.assertFalse(kwargs.changed_to_false)

        # check missing keyword arg
        self.assertRaises(KeyError, AttributeFilter, {"true": True, "false": False}, missing=True)

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

        # check exception raised if template is not an AttributeFilter
        self.assertRaises(TypeError, AttributeFilter().conforms_to_template_filter, "string")

        filter_a = AttributeFilter({"a": True, "b": {"a": True}, "c": False})
        filter_b = AttributeFilter({"a": False, "b": {"a": False}, "d": True})

        # check exception raised if keys differ
        self.assertRaises(exception.AttributeFilterDiffers, filter_a.conforms_to_template_filter, filter_b)

        filter_c = AttributeFilter({"a": False, "b": {"a": False}, "c": False})

        # check that source values are copied across to template
        merged_filter = filter_a.conforms_to_template_filter(filter_c)
        self.assertTrue(merged_filter.is_attribute_visible("a"))
        self.assertTrue(merged_filter.is_attribute_visible("b"))
        self.assertTrue(merged_filter.b.is_attribute_visible("a"))
        self.assertFalse(merged_filter.is_attribute_visible("c"))

    def test_keys_empty(self):
        empty_dict = AttributeFilter()
        empty_dict_keys = empty_dict.keys()
        self.assertEquals(empty_dict_keys, [])

    def test_keys_dict(self):
        # test created from dict
        from_dict = AttributeFilter({"a": True, "b": False, "c": True})
        from_dict_keys = from_dict.keys()
        self.assertEquals(from_dict_keys, ["a", "b", "c"])

    def test_keys_from_model(self):
        # test created from model
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        from_model = AttributeFilter.from_model(model_instance=MyModel())
        self.assertEquals(from_model.keys(), ["name", "tags"])


class AttributeFilterContains(unittest.TestCase):

    def test_from_dict(self):
        from_dict = AttributeFilter({"a": True, "b": False, "c": True})
        self.assertTrue("a" in from_dict)
        self.assertTrue("b" in from_dict)
        self.assertTrue("c" in from_dict)
        self.assertFalse("d" in from_dict)

    def test_from_model(self):
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        from_model = AttributeFilter.from_model(model_instance=MyModel())
        self.assertTrue("name" in from_model)
        self.assertTrue("tags" in from_model)
        self.assertFalse("age" in from_model)


class AttributeFilterIsFilterAtKey(unittest.TestCase):

    def test_is_filter_at_key(self):

        class SubModel(types.Model):
            name = types.String()

        class ModelWithSub(types.Model):
            tags = types.Array(element_template=types.String())
            sub_model = SubModel()

        attribute_filter = AttributeFilter.from_model(model_instance=ModelWithSub())
        self.assertTrue(attribute_filter.is_filter_at_key("sub_model"))
        self.assertFalse(attribute_filter.is_filter_at_key("tags"))


class AttributeFilterIsAttributeVisible(unittest.TestCase):

    def test_true_returns_true(self):
        values = {
            "a": True,
            "b": True,
            "c": True
        }

        attribute_filter = AttributeFilter(values)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertTrue(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))

    def test_false_returns_false(self):
        values = {
            "a": False,
            "b": False,
            "c": False
        }

        attribute_filter = AttributeFilter(values)
        self.assertFalse(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertFalse(attribute_filter.is_attribute_visible("c"))

    def test_mixed_returns_correct(self):
        values = {
            "a": False,
            "b": True,
            "c": False
        }

        attribute_filter = AttributeFilter(values)
        self.assertFalse(attribute_filter.is_attribute_visible("a"))
        self.assertTrue(attribute_filter.is_attribute_visible("b"))
        self.assertFalse(attribute_filter.is_attribute_visible("c"))

    def test_fully_visible_sub_filter_returns_true(self):
        values = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": True,
                "b": True
            }
        }

        attribute_filter = AttributeFilter(values)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertTrue(attribute_filter.is_attribute_visible("d"))

    def test_fully_invisible_sub_filter_returns_false(self):
        values = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": False,
                "b": False
            }
        }

        attribute_filter = AttributeFilter(values)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertFalse(attribute_filter.is_attribute_visible("d"))

    def test_partially_visible_sub_filter_returns_true(self):
        values = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": True,
                "b": False
            }
        }

        attribute_filter = AttributeFilter(values)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertTrue(attribute_filter.is_attribute_visible("d"))


class AttributeFilterAreAnyAttributesVisible(unittest.TestCase):

    def test_all_true_returns_true(self):
        attribute_filter = AttributeFilter({"a": True, "b": True, "c": True})
        self.assertTrue(attribute_filter.are_any_attributes_visible())

    def test_any_true_returns_true(self):
        attribute_filter = AttributeFilter({"a": True, "b": False, "c": True})
        self.assertTrue(attribute_filter.are_any_attributes_visible())

    def test_all_false_returns_false(self):
        attribute_filter = AttributeFilter({"a": False, "b": False, "c": False})
        self.assertFalse(attribute_filter.are_any_attributes_visible())

    def test_visible_sub_filter_returns_true(self):
        attribute_filter = AttributeFilter({"a": {"a": True}, "b": False, "c": False})
        self.assertTrue(attribute_filter.are_any_attributes_visible())

    def test_invisible_sub_filter_returns_false(self):
        attribute_filter = AttributeFilter({"a": {"a": False}, "b": False, "c": False})
        self.assertFalse(attribute_filter.are_any_attributes_visible())


class AttributeFilterAreAllAttributesVisible(unittest.TestCase):

    def test_all_true_returns_true(self):
        attribute_filter = AttributeFilter({"a": True, "b": True, "c": True})
        self.assertTrue(attribute_filter.are_all_attributes_visible())

    def test_all_false_returns_false(self):
        attribute_filter = AttributeFilter({"a": False, "b": False, "c": False})
        self.assertFalse(attribute_filter.are_all_attributes_visible())

    def test_any_false_returns_false(self):
        attribute_filter = AttributeFilter({"a": True, "b": True, "c": False})
        self.assertFalse(attribute_filter.are_all_attributes_visible())

    def test_visible_sub_filter_returns_true(self):
        attribute_filter = AttributeFilter({"a": {"a": True}, "b": True, "c": True})
        self.assertTrue(attribute_filter.are_all_attributes_visible())

    def test_invisible_sub_filter_returns_false(self):
        attribute_filter = AttributeFilter({"a": {"a": False}, "b": True, "c": True})
        self.assertFalse(attribute_filter.are_all_attributes_visible())


class AttributeFilterSetAllAttributeValues(unittest.TestCase):

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


class AttributeFilterAsDict(unittest.TestCase):

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


class AttributeFilterInitFromDictionary(unittest.TestCase):

    def test_init_from_dictionary(self):
        self.assertRaises(TypeError, AttributeFilter, "string")

        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        self.assertRaises(TypeError, AttributeFilter, {"name": True}, template_model="string")
        self.assertRaises(TypeError, AttributeFilter, {"name": "string"})

        # check that filter is correctly reversed
        attribute_filter = AttributeFilter({"a": True}, template_model=MyModel())
        self.assertTrue(attribute_filter.is_attribute_visible("name"))

        # todo: check that exception is throw when invalid keys are passed
        # self.assertRaises(
        #     exception.AttributeFilterDiffers,
        #     AttributeFilter,
        #     from_dictionary={"a": True, "c": False},
        #     template_model=MyModel()
        # )


class AttributeFilterSetAttr(unittest.TestCase):

    def test_setattr(self):
        values = {
            "a": True,
            "b": False,
            "c": True,
            "d": {
                "a": True,
                "b": False
            }
        }

        attribute_filter = AttributeFilter(values)
        self.assertTrue(attribute_filter.is_attribute_visible("a"))
        self.assertFalse(attribute_filter.is_attribute_visible("b"))
        self.assertTrue(attribute_filter.is_attribute_visible("c"))
        self.assertTrue(attribute_filter.is_attribute_visible("d"))
        attribute_filter.a = False
        attribute_filter.b = True
        attribute_filter.c = False
        attribute_filter.d = False
        self.assertFalse(attribute_filter.is_attribute_visible("a"))
        self.assertTrue(attribute_filter.is_attribute_visible("b"))
        self.assertFalse(attribute_filter.is_attribute_visible("c"))
        self.assertFalse(attribute_filter.is_attribute_visible("d"))

        self.assertRaises(TypeError, attribute_filter.__setattr__ , "a", "string")
        self.assertRaises(TypeError, attribute_filter.__setattr__, "missing", None)

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
