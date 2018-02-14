import unittest

from prestans import exception
from prestans import types


class ArrayUnitTest(unittest.TestCase):

    def test_len(self):
        array = types.Array(element_template=types.Integer())

        self.assertEquals(len(array), 0)
        array.append(1)
        self.assertEquals(len(array), 1)
        array.append(2)
        self.assertEquals(len(array), 2)


class ArrayIter(unittest.TestCase):

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


class ArrayGetItem(unittest.TestCase):

    def test_getitem(self):
        array = types.Array(element_template=types.Integer())
        self.assertRaises(IndexError, array.__getitem__, 0)

        array.append(1)
        self.assertEquals(array[0], 1)


class ArrayContains(unittest.TestCase):

    def test_contains(self):
        array = types.Array(element_template=types.Integer())
        self.assertFalse(1 in array)

        array.append(1)
        self.assertTrue(1 in array)


class ArrayMaxLength(unittest.TestCase):

    def test_default(self):
        self.assertIsNone(types.Array(element_template=types.Boolean()).max_length)
        self.assertIsNone(types.Array(element_template=types.Float()).max_length)
        self.assertIsNone(types.Array(element_template=types.Integer()).max_length)
        self.assertIsNone(types.Array(element_template=types.Integer()).max_length)
        self.assertIsNone(types.Array(element_template=types.Date()).max_length)
        self.assertIsNone(types.Array(element_template=types.DateTime()).max_length)
        self.assertIsNone(types.Array(element_template=types.Time()).max_length)
        self.assertIsNone(types.Array(element_template=types.Model()).max_length)

    def test_custom(self):
        self.assertEquals(types.Array(element_template=types.Boolean(), max_length=1).max_length, 1)
        self.assertEquals(types.Array(element_template=types.Float(), max_length=2).max_length, 2)
        self.assertEquals(types.Array(element_template=types.Integer(), max_length=3).max_length, 3)
        self.assertEquals(types.Array(element_template=types.String(), max_length=4).max_length, 4)
        self.assertEquals(types.Array(element_template=types.Date(), max_length=5).max_length, 5)
        self.assertEquals(types.Array(element_template=types.DateTime(), max_length=6).max_length, 6)
        self.assertEquals(types.Array(element_template=types.Time(), max_length=7).max_length, 7)
        self.assertEquals(types.Array(element_template=types.Model(), max_length=8).max_length, 8)


class ArrayMinLength(unittest.TestCase):

    def test_default(self):
        self.assertIsNone(types.Array(element_template=types.Boolean()).min_length)
        self.assertIsNone(types.Array(element_template=types.Float()).min_length)
        self.assertIsNone(types.Array(element_template=types.Integer()).min_length)
        self.assertIsNone(types.Array(element_template=types.String()).min_length)
        self.assertIsNone(types.Array(element_template=types.Date()).min_length)
        self.assertIsNone(types.Array(element_template=types.DateTime()).min_length)
        self.assertIsNone(types.Array(element_template=types.Time()).min_length)
        self.assertIsNone(types.Array(element_template=types.Model()).min_length)

    def test_custom(self):
        self.assertEquals(types.Array(element_template=types.Boolean(), min_length=1).min_length, 1)
        self.assertEquals(types.Array(element_template=types.Float(), min_length=2).min_length, 2)
        self.assertEquals(types.Array(element_template=types.Integer(), min_length=3).min_length, 3)
        self.assertEquals(types.Array(element_template=types.String(), min_length=4).min_length, 4)
        self.assertEquals(types.Array(element_template=types.Date(), min_length=5).min_length, 5)
        self.assertEquals(types.Array(element_template=types.DateTime(), min_length=6).min_length, 6)
        self.assertEquals(types.Array(element_template=types.Time(), min_length=7).min_length, 7)
        self.assertEquals(types.Array(element_template=types.Model(), min_length=8).min_length, 8)


class ArrayDescription(unittest.TestCase):

    def test_default(self):
        self.assertIsNone(types.Array(element_template=types.Boolean()).description)
        self.assertIsNone(types.Array(element_template=types.Float()).description)
        self.assertIsNone(types.Array(element_template=types.Integer()).description)
        self.assertIsNone(types.Array(element_template=types.String()).description)
        self.assertIsNone(types.Array(element_template=types.Date()).description)
        self.assertIsNone(types.Array(element_template=types.DateTime()).description)
        self.assertIsNone(types.Array(element_template=types.Time()).description)
        self.assertIsNone(types.Array(element_template=types.Model()).description)

    def test_custom(self):
        boolean_array = types.Array(element_template=types.Boolean(), description="boolean")
        self.assertEquals(boolean_array.description, "boolean")

        float_array = types.Array(element_template=types.Float(), description="float")
        self.assertEquals(float_array.description, "float")

        integer_array = types.Array(element_template=types.Integer(), description="integer")
        self.assertEquals(integer_array.description, "integer")

        string_array = types.Array(element_template=types.String(), description="string")
        self.assertEquals(string_array.description, "string")

        date_array = types.Array(element_template=types.Date(), description="date")
        self.assertEquals(date_array.description, "date")

        datetime_array = types.Array(element_template=types.DateTime(), description="datetime")
        self.assertEquals(datetime_array.description, "datetime")

        time_array = types.Array(element_template=types.Date(), description="time")
        self.assertEquals(time_array.description, "time")


class ArrayIsScalar(unittest.TestCase):

    def test_data_type(self):
        self.assertTrue(types.Array(element_template=types.Boolean()).is_scalar)
        self.assertTrue(types.Array(element_template=types.Float()).is_scalar)
        self.assertTrue(types.Array(element_template=types.Integer()).is_scalar)
        self.assertTrue(types.Array(element_template=types.String()).is_scalar)

    def test_data_structure(self):
        self.assertFalse(types.Array(element_template=types.Date()).is_scalar)
        self.assertFalse(types.Array(element_template=types.DateTime()).is_scalar)
        self.assertFalse(types.Array(element_template=types.Time()).is_scalar)

    def test_data_collection(self):
        self.assertFalse(types.Array(element_template=types.Model()).is_scalar)

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


class ArrayRemove(unittest.TestCase):

    def test_remove(self):
        array = types.Array(element_template=types.String())
        array.append("dog")
        array.append("cat")
        self.assertEquals(len(array), 2)
        array.remove("dog")
        self.assertEquals(len(array), 1)
        array.remove("cat")
        self.assertEquals(len(array), 0)


class ArrayAppend(unittest.TestCase):

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
            name = types.String()

        array = types.Array(element_template=MyModel())
        self.assertEquals(len(array), 0)

        self.assertRaises(TypeError, array.append, "string")
        self.assertEquals(len(array), 0)

        my_model = MyModel(name="alice")
        validated = array.validate([my_model.as_serializable()])
        self.assertEquals(validated.as_serializable(), [{"name": "alice"}])


class ArrayValidate(unittest.TestCase):

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
        class Person(types.Model):
            first_name = types.String()
            last_name = types.String()
        persons = types.Array(element_template=Person())
        persons.append(Person(first_name="John", last_name="Smith"))

        persons_validated = persons.validate(persons.as_serializable(minified=True), minified=True)
        self.assertEquals(persons_validated.as_serializable(minified=True), [{"a_c": "John", "b_c": "Smith"}])
        self.assertEquals(persons_validated.as_serializable(), [{"first_name": "John", "last_name": "Smith"}])


class ArrayAsSerializable(unittest.TestCase):

    def test_data_type(self):
        array_empty = types.Array(element_template=types.String())
        self.assertEquals(array_empty.as_serializable(), [])

        array_strings = types.Array(element_template=types.String())
        array_strings.append("cat")
        array_strings.append("dog")
        self.assertEquals(array_strings.as_serializable(), ["cat", "dog"])

    def test_data_structure(self):
        from datetime import date
        array_empty = types.Array(element_template=types.Date())
        self.assertEquals(array_empty.as_serializable(), [])

        array_dates = types.Array(element_template=types.Date())
        array_dates.append(date(2018, 1, 1))
        array_dates.append("2018-01-02")
        self.assertEquals(array_dates.as_serializable(), ["2018-01-01", "2018-01-02"])

    def test_data_collection(self):
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

    def test_sub_model(self):

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

    def test_sub_array_data_type(self):
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

    def test_sub_array_model(self):

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

    def test_filtered(self):
        pass

    def test_minified(self):
        pass


class ArrayAttributeRewriteMap(unittest.TestCase):

    def test_data_type(self):
        self.assertIsNone(types.Array(element_template=types.Boolean()).attribute_rewrite_map())
        self.assertIsNone(types.Array(element_template=types.Float()).attribute_rewrite_map())
        self.assertIsNone(types.Array(element_template=types.Integer()).attribute_rewrite_map())
        self.assertIsNone(types.Array(element_template=types.String()).attribute_rewrite_map())

    def test_data_structure(self):
        self.assertIsNone(types.Array(element_template=types.Date()).attribute_rewrite_map())
        self.assertIsNone(types.Array(element_template=types.DateTime()).attribute_rewrite_map())
        self.assertIsNone(types.Array(element_template=types.Time()).attribute_rewrite_map())

    def test_data_collection(self):
        class MyModel(types.Model):
            cat = types.String()
            dog = types.String()

        array = types.Array(element_template=MyModel())
        self.assertEquals(array.attribute_rewrite_map(), MyModel().attribute_rewrite_map())


class ArrayAttributeRewriteReverseMap(unittest.TestCase):

    def test_data_type(self):
        self.assertIsNone(types.Array(element_template=types.Boolean()).attribute_rewrite_reverse_map())
        self.assertIsNone(types.Array(element_template=types.Float()).attribute_rewrite_reverse_map())
        self.assertIsNone(types.Array(element_template=types.Integer()).attribute_rewrite_reverse_map())
        self.assertIsNone(types.Array(element_template=types.String()).attribute_rewrite_reverse_map())

    def test_data_structure(self):
        self.assertIsNone(types.Array(element_template=types.Date()).attribute_rewrite_reverse_map())
        self.assertIsNone(types.Array(element_template=types.DateTime()).attribute_rewrite_reverse_map())
        self.assertIsNone(types.Array(element_template=types.Time()).attribute_rewrite_reverse_map())

    def test_data_collection(self):
        class MyModel(types.Model):
            cat = types.String()
            dog = types.String()

        array = types.Array(element_template=MyModel())
        self.assertEquals(array.attribute_rewrite_reverse_map(), MyModel().attribute_rewrite_reverse_map())


class ArrayGetAttributeFilter(unittest.TestCase):

    def test_data_type(self):
        boolean_array = types.Array(element_template=types.Boolean())
        self.assertFalse(boolean_array.get_attribute_filter())
        self.assertFalse(boolean_array.get_attribute_filter(False))
        self.assertTrue(boolean_array.get_attribute_filter(True))

        float_array = types.Array(element_template=types.Float())
        self.assertFalse(float_array.get_attribute_filter())
        self.assertFalse(float_array.get_attribute_filter(False))
        self.assertTrue(float_array.get_attribute_filter(True))

        integer_array = types.Array(element_template=types.Integer())
        self.assertFalse(integer_array.get_attribute_filter())
        self.assertFalse(integer_array.get_attribute_filter(False))
        self.assertTrue(integer_array.get_attribute_filter(True))

        string_array = types.Array(element_template=types.String())
        self.assertFalse(string_array.get_attribute_filter())
        self.assertFalse(string_array.get_attribute_filter(False))
        self.assertTrue(string_array.get_attribute_filter(True))

    def test_data_structure(self):
        date_array = types.Array(element_template=types.Date())
        self.assertFalse(date_array.get_attribute_filter())
        self.assertFalse(date_array.get_attribute_filter(False))
        self.assertTrue(date_array.get_attribute_filter(True))

        datetime_array = types.Array(element_template=types.DateTime())
        self.assertFalse(datetime_array.get_attribute_filter())
        self.assertFalse(datetime_array.get_attribute_filter(False))
        self.assertTrue(datetime_array.get_attribute_filter(True))

        time_array = types.Array(element_template=types.Time())
        self.assertFalse(time_array.get_attribute_filter())
        self.assertFalse(time_array.get_attribute_filter(False))
        self.assertTrue(time_array.get_attribute_filter(True))

    def test_data_collection(self):
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
