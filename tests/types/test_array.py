import unittest

from prestans import exception
from prestans import types


class ArrayUnitTest(unittest.TestCase):

    def test_len(self):
        array = types.Array(element_template=types.Integer())
        self.assertEquals(len(array), 0)

        array.append(1)
        self.assertEquals(len(array), 1)

    def test_iter(self):
        elements = ["a", "b", "c"]

        array = types.Array(element_template=types.String())
        array.append(elements[0])
        array.append(elements[1])
        array.append(elements[2])

        index = 0
        for element in array:
            self.assertEquals(element, elements[index])
            index += 1

    def test_getitem(self):
        array = types.Array(element_template=types.Integer())
        self.assertRaises(IndexError, array.__getitem__, 0)

        array.append(1)
        self.assertEquals(array[0], 1)

    def test_contains(self):
        array = types.Array(element_template=types.Integer())
        self.assertFalse(1 in array)

        array.append(1)
        self.assertTrue(1 in array)

    def test_max_length(self):
        default_max = types.Array(element_template=types.Integer())
        self.assertIsNone(default_max.max_length)

        custom_max = types.Array(element_template=types.Integer(), max_length=2)
        self.assertEquals(custom_max.max_length, 2)

    def test_min_length(self):
        default_min = types.Array(element_template=types.Integer())
        self.assertIsNone(default_min.min_length)

        custom_min = types.Array(element_template=types.Integer(), min_length=1)
        self.assertEquals(custom_min.min_length, 1)

    def test_description(self):
        default_description = types.Array(element_template=types.Integer())
        self.assertIsNone(default_description.description)

        custom_description = types.Array(element_template=types.Integer(), description="description")
        self.assertEquals(custom_description.description, "description")

    def test_is_scalar(self):
        string_array = types.Array(element_template=types.String())
        self.assertTrue(string_array.is_scalar)

        integer_array = types.Array(element_template=types.Integer())
        self.assertTrue(integer_array.is_scalar)

        boolean_array = types.Array(element_template=types.Boolean())
        self.assertTrue(boolean_array.is_scalar)

        float_array = types.Array(element_template=types.Float())
        self.assertTrue(float_array.is_scalar)

        model_array = types.Array(element_template=types.Model())
        self.assertFalse(model_array.is_scalar)

    def test_element_template(self):
        float_element_template = types.Float()
        string_element_template = types.String()

        self.assertRaises(TypeError, types.Array, element_template="string")

        array = types.Array(element_template=float_element_template)
        self.assertEquals(array.element_template, float_element_template)
        array.element_template = string_element_template
        self.assertEquals(array.element_template, string_element_template)

    def test_blueprint(self):
        array_default = types.Array(element_template=types.String())
        blueprint_default = array_default.blueprint()
        self.assertEquals(blueprint_default["type"], "array")
        self.assertEquals(blueprint_default["constraints"]["required"], True)
        self.assertEquals(blueprint_default["constraints"]["min_length"], None)
        self.assertEquals(blueprint_default["constraints"]["max_length"], None)
        self.assertEquals(blueprint_default["constraints"]["element_template"], types.String().blueprint())
        self.assertEquals(blueprint_default["constraints"]["description"], None)

        array_custom = types.Array(
            required=False,
            min_length=1,
            max_length=10,
            element_template=types.String(default="cat"),
            description="description"
        )
        blueprint_custom = array_custom.blueprint()
        self.assertEquals(blueprint_custom["type"], "array")
        self.assertEquals(blueprint_custom["constraints"]["required"], False)
        self.assertEquals(blueprint_custom["constraints"]["min_length"], 1)
        self.assertEquals(blueprint_custom["constraints"]["max_length"], 10)
        self.assertEquals(blueprint_custom["constraints"]["element_template"], types.String(default="cat").blueprint())
        self.assertEquals(blueprint_custom["constraints"]["description"], "description")

    def test_remove(self):
        array = types.Array(element_template=types.String())
        array.append("dog")
        array.append("cat")
        self.assertEquals(len(array), 2)
        array.remove("dog")
        self.assertEquals(len(array), 1)
        array.remove("cat")
        self.assertEquals(len(array), 0)

    def test_append_data_type(self):
        array = types.Array(element_template=types.String())
        self.assertEquals(len(array), 0)

        array.append("dog")
        self.assertEquals(len(array), 1)
        self.assertTrue("dog" in array)

        array.append(["cat", "rat"])
        self.assertEquals(len(array), 3)
        self.assertTrue("cat" in array)
        self.assertTrue("rat"in array)

    def test_append_model(self):
        class MyModel(types.Model):
            pass

        array = types.Array(element_template=MyModel())
        self.assertEquals(len(array), 0)

        self.assertRaises(TypeError, array.append, "string")
        self.assertEquals(len(array), 0)

        my_model = MyModel()
        array.append(my_model)
        self.assertEquals(len(array), 1)

    def test_validate_not_required_returns_none(self):
        array = types.Array(required=False, element_template=types.String())
        self.assertIsNone(array.validate(None))

    def test_validate_non_list_type_raises_type_error(self):
        array = types.Array(required=True, element_template=types.String())
        self.assertRaises(TypeError, array.validate, None)
        self.assertRaises(TypeError, array.validate, "string")
        self.assertRaises(TypeError, array.validate, 1)

    def test_validate_min_length(self):
        array = types.Array(min_length=2, element_template=types.String())
        self.assertRaises(exception.LessThanMinimumError, array.validate, [])
        self.assertRaises(exception.LessThanMinimumError, array.validate, [1])
        self.assertRaises(exception.LessThanMinimumError, array.validate, ["string"])

    def test_validate_max_length(self):
        array = types.Array(max_length=2, element_template=types.String())
        self.assertRaises(exception.MoreThanMaximumError, array.validate, [1, 2, 3])
        self.assertRaises(exception.MoreThanMaximumError, array.validate, ["a", "b", "c"])

    def test_validate_filtered(self):
        pass

    def test_validate_minified(self):
        pass

    def test_as_serializable_basic_types(self):
        array_empty = types.Array(element_template=types.String())
        self.assertEquals(array_empty.as_serializable(), [])

        array_strings = types.Array(element_template=types.String())
        array_strings.append("cat")
        array_strings.append("dog")
        self.assertEquals(array_strings.as_serializable(), ["cat", "dog"])

    def test_as_serializable_model(self):
        class MyModel(types.Model):
            name = types.String()
        array_model = types.Array(element_template=MyModel())
        array_model.append(MyModel(name="alice"))
        array_model.append(MyModel(name="bob"))
        array_model.append(MyModel(name="carol"))

        self.assertEquals(
            array_model.as_serializable(),
            [
                {"name": "alice"},
                {"name": "bob"},
                {"name": "carol"}
            ]
        )

    def test_as_serializable_sub_model(self):

        class MyModel(types.Model):
            name = types.String()

        class ParentModel(types.Model):
            name = types.String()
            sub_model = MyModel()

        array_sub_model = types.Array(element_template=ParentModel())

        model_a = ParentModel(name="alice", sub_model={"name": "bob"})
        model_a.name = "alice"
        model_a.sub_model.name = "bob"
        array_sub_model.append(model_a)

        model_b = ParentModel(name="alice", sub_model={"name": "bob"})
        model_b.name = "bob"
        model_b.sub_model.name = "carol"
        array_sub_model.append(model_b)

        self.assertEquals(
            array_sub_model.as_serializable(),
            [
                {"name": "alice", "sub_model": {"name": "bob"}},
                {"name": "bob", "sub_model": {"name": "carol"}}
            ]
        )

    def test_as_serializable_sub_array_data_type(self):
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        my_model = MyModel()
        my_model.name = "alice"
        my_model.tags = ["a", "b", "c"]

        array_sub_array = types.Array(element_template=MyModel())
        array_sub_array.append(my_model)

        self.assertEquals(
            array_sub_array.as_serializable(),
            [
                {"name": "alice", "tags": ["a", "b", "c"]}
            ]
        )

    def test_as_serializable_sub_array_model(self):

        class SubModel(types.Model):
            name = types.String()

        class ParentModel(types.Model):
            name = types.String()
            people = types.Array(element_template=SubModel())

        my_model = ParentModel()
        my_model.name = "alice"
        my_model.people.append(SubModel(name="bob"))

        array_sub_array = types.Array(element_template=ParentModel())
        array_sub_array.append(my_model)

        self.assertEquals(
            array_sub_array.as_serializable(),
            [
                {"name": "alice", "people": [{"name": "bob"}]}
            ]
        )

    def test_as_serializable_filtered(self):
        pass

    def test_as_serializable_minified(self):
        pass

    def test_attribute_rewrite_map(self):
        class MyModel(types.Model):
            cat = types.String()
            dog = types.String()

        array = types.Array(element_template=MyModel())
        self.assertEquals(array.attribute_rewrite_map(), MyModel().attribute_rewrite_map())

    def test_attribute_rewrite_reverse_map(self):
        class MyModel(types.Model):
            cat = types.String()
            dog = types.String()

        array = types.Array(element_template=MyModel())
        self.assertEquals(array.attribute_rewrite_reverse_map(), MyModel().attribute_rewrite_reverse_map())

    def test_get_attribute_filter_basic_types(self):
        array = types.Array(element_template=types.String())
        self.assertFalse(array.get_attribute_filter())
        self.assertFalse(array.get_attribute_filter(False))
        self.assertTrue(array.get_attribute_filter(True))

    def test_get_attribute_filter_models(self):
        class MyModel(types.Model):
            cat = types.String()

        cat = MyModel()
        cat.cat = "cat"

        array = types.Array(element_template=MyModel())
        array.append(cat)
        attribute_filter = array.get_attribute_filter()
        self.assertTrue("cat" in attribute_filter)
        self.assertFalse("dog" in attribute_filter)
        self.assertFalse(attribute_filter.cat)

        attribute_filter = array.get_attribute_filter(True)
        self.assertTrue("cat" in attribute_filter)
        self.assertFalse("dog" in attribute_filter)
        self.assertTrue(attribute_filter.cat)
