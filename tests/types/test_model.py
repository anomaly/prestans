import unittest

from prestans import exception
from prestans.parser import AttributeFilter
from prestans import types


class ModelUnitTest(unittest.TestCase):

    def test_required(self):
        class MyModel(types.Model):
            pass

        required_default = MyModel()
        self.assertTrue(required_default._required)

        required_true = MyModel(required=True)
        self.assertTrue(required_true._required)

        required_false = MyModel(required=False)
        self.assertFalse(required_false._required)

    def test_default(self):
        pass

    def test_description(self):
        class MyModel(types.Model):
            pass

        description_default = MyModel()
        self.assertIsNone(description_default._description)

        description_value = MyModel(description="description")
        self.assertEquals(description_value._description, "description")

    def test_attribute_count(self):
        class EmptyModel(types.Model):
            pass

        self.assertEquals(EmptyModel().attribute_count(), 0)

        class BasicTypesOnly(types.Model):
            name = types.String()
            age = types.Integer()

        self.assertEquals(BasicTypesOnly().attribute_count(), 2)

        class ModelWithArray(types.Model):
            name = types.String()
            age = types.Integer()
            tags = types.Array(element_template=types.String())

        self.assertEquals(ModelWithArray().attribute_count(), 3)

        class SubModel(types.Model):
            pass

        class ModelWithSub(types.Model):
            name = types.String()
            age = types.Integer()
            sub = SubModel()

        self.assertEquals(ModelWithSub().attribute_count(), 3)

        class ModelWithSubAndArray(types.Model):
            name = types.String()
            age = types.Integer()
            tags = types.Array(element_template=types.String())
            sub = SubModel()

        self.assertEquals(ModelWithSubAndArray().attribute_count(), 4)

    def test_blueprint(self):
        class MyModel(types.Model):
            nick_name = types.String(required=True)
            first_name = types.String(required=True)
            last_name = types.String(required=False)

        blueprint = MyModel(required=False, description="description").blueprint()
        self.assertEquals(blueprint["type"], "model")
        self.assertEquals(blueprint["constraints"]["required"], False)
        self.assertEquals(blueprint["constraints"]["description"], "description")
        self.assertEquals(blueprint["fields"]["nick_name"], MyModel.nick_name.blueprint())
        self.assertEquals(blueprint["fields"]["first_name"], MyModel.first_name.blueprint())
        self.assertEquals(blueprint["fields"]["last_name"], MyModel.last_name.blueprint())

    def test_blueprint_bad_attribute(self):
        class ModelWithBadAttribute(types.Model):
            name = "string"

        self.assertRaises(TypeError, ModelWithBadAttribute().blueprint)

    def test_setattr(self):
        class SubModel(types.Model):
            string = types.String()

        class MyModel(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            age = types.Integer(maximum=120)
            name = types.String()

            sub_model = SubModel()

        sub_model = SubModel()
        sub_model.string = "string"
        self.assertEquals(sub_model.string, "string")

        my_model = MyModel()
        my_model.boolean = True
        my_model.name = "name"
        my_model.age = 21
        my_model.sub_model = sub_model
        self.assertEquals(my_model.boolean, True)
        self.assertEquals(my_model.name, "name")
        self.assertEquals(my_model.age, 21)
        self.assertEquals(my_model.sub_model, sub_model)
        self.assertEquals(my_model.sub_model.string, "string")
        self.assertRaises(KeyError, my_model.__setattr__, "missing", "missing")
        self.assertRaises(exception.ValidationError, my_model.__setattr__, "age", 121)

    def test_create_instance_attributes(self):
        class MyModel(types.Model):
            string = types.String(default="default")
            nothing = None

        my_model = MyModel()
        self.assertEquals(my_model.string, "default")
        my_model = MyModel(string="string")
        self.assertEquals(my_model.string, "string")
        self.assertIsNone(my_model.nothing)

    def test_get_attribute_keys(self):
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        my_model = MyModel()
        self.assertEquals(my_model.get_attribute_keys(), ["name", "tags"])

    def test_get_attribute_filter_base(self):
        attribute_filter = types.Model().get_attribute_filter()
        self.assertEquals(attribute_filter.keys(), [])

    def test_get_attribute_filter(self):
        class SubModel(types.Model):
            colour = types.String()

        class MyModel(types.Model):
            name = types.String()
            sub = SubModel()

        my_model = MyModel()
        attribute_filter = my_model.get_attribute_filter(default_value=True)
        self.assertTrue(attribute_filter.name)
        self.assertTrue(attribute_filter.sub)
        self.assertTrue(attribute_filter.sub.colour)
        self.assertEquals(attribute_filter.keys(), ["name", "sub"])

    def test_attribute_rewrite_map(self):
        class MyModel(types.Model):
            name = types.String()
            first_name = types.String()
            last_name = types.String()

        rewrite_map = {
            "first_name": "a_c",
            "last_name": "b_c",
            "name": "c"
        }

        my_model = MyModel()
        self.assertEquals(my_model.attribute_rewrite_map(), rewrite_map)

    def test_attribute_rewrite_reverse_map(self):
        class MyModel(types.Model):
            name = types.String()
            first_name = types.String()
            last_name = types.String()

        reverse_map = {
            "a_c": "first_name",
            "b_c": "last_name",
            "c": "name"
        }

        my_model = MyModel()
        self.assertEquals(my_model.attribute_rewrite_reverse_map(), reverse_map)

    def test_contains(self):

        class SubModel(types.Model):
            pass

        # check if key can be found in model
        class MyModel(types.Model):
            name = types.String()
            birthday = types.Date()
            tags = types.Array(element_template=types.String())
            sub = SubModel()
            sub_array = types.Array(element_template=SubModel())
        my_model = MyModel()
        self.assertTrue("name" in my_model)
        self.assertTrue("birthday" in my_model)
        self.assertTrue("tags" in my_model)
        self.assertTrue("sub" in my_model)
        self.assertTrue("sub_array" in my_model)
        self.assertFalse("missing"in my_model)

        # check if keys can be found in model and base class
        class ModelWithSingleBase(MyModel):
            extra = types.String()

        single_base = ModelWithSingleBase()
        self.assertTrue("name" in single_base)
        self.assertTrue("birthday" in single_base)
        self.assertTrue("tags" in single_base)
        self.assertTrue("sub" in single_base)
        self.assertTrue("sub_array" in single_base)
        self.assertTrue("extra" in single_base)
        self.assertFalse("missing" in single_base)

        class ModelWithMultiBase(ModelWithSingleBase):
            another = types.String()

        multi_base = ModelWithMultiBase()
        self.assertTrue("name" in multi_base)
        self.assertTrue("birthday" in multi_base)
        self.assertTrue("tags" in multi_base)
        self.assertTrue("sub" in multi_base)
        self.assertTrue("sub_array" in multi_base)
        self.assertTrue("extra" in multi_base)
        self.assertTrue("another" in multi_base)
        self.assertFalse("missing" in multi_base)

    def test_generate_attribute_token_rewrite_map(self):
        class MyModel(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

        my_model = MyModel()
        rewrite_map = my_model.generate_attribute_token_rewrite_map()
        self.assertEquals(
            rewrite_map,
            {
                "boolean": "a",
                "float": "b",
                "integer": "c",
                "string": "d"
            }
        )

    def test_generate_attribute_tokens(self):
        class MyModel(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()
        my_model = MyModel()
        tokens = my_model.generate_attribute_tokens()
        self.assertEquals(tokens, ["boolean", "float", "integer", "string"])

    def test_generate_minified_keys(self):
        self.assertEquals(types.Model.generate_minified_keys(3), ["a", "b", "c"])
        self.assertEquals(types.Model.generate_minified_keys(5), ["a", "b", "c", "d", "e"])

        self.assertEquals(types.Model.generate_minified_keys(3, "_"), ["_a", "_b", "_c"])
        self.assertEquals(types.Model.generate_minified_keys(5, "_"), ["_a", "_b", "_c", "_d", "_e"])

        self.assertEquals(types.Model.generate_minified_keys(29), [
            "a", "b", "c", "d", "e", "f", "g", "h", "i",
            "j", "k", "l", "m", "n", "o", "p", "q", "r",
            "s", "t", "u", "v", "w", "x", "y", "z",
            "aa", "ab", "ac"
        ])

        self.assertEquals(types.Model.generate_minified_keys(55), [
            "a", "b", "c", "d", "e", "f", "g", "h", "i",
            "j", "k", "l", "m", "n", "o", "p", "q", "r",
            "s", "t", "u", "v", "w", "x", "y", "z",
            "aa", "ab", "ac", "ad", "ae", "af", "ag", "ah", "ai",
            "aj", "ak", "al", "am", "an", "ao", "ap", "aq", "ar",
            "as", "at", "au", "av", "aw", "ax", "ay", "az",
            "ba", "bb", "bc"
        ])

    def test__generate_attribute_key(self):
        self.assertEquals(types.Model.generate_attribute_key(0), "a")
        self.assertEquals(types.Model.generate_attribute_key(1), "b")
        self.assertEquals(types.Model.generate_attribute_key(25), "z")
        self.assertEquals(types.Model.generate_attribute_key(26), "aa")
        self.assertEquals(types.Model.generate_attribute_key(27), "bb")
        self.assertEquals(types.Model.generate_attribute_key(51), "zz")
        self.assertEquals(types.Model.generate_attribute_key(52), "aaa")
        self.assertEquals(types.Model.generate_attribute_key(54), "ccc")
        self.assertEquals(types.Model.generate_attribute_key(77), "zzz")


class ModelAsSerializable(unittest.TestCase):

    def test_as_serializable(self):
        from datetime import date
        from datetime import datetime
        from datetime import time

        class SubModel(types.Model):
            name = types.String()

        class MyModel(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

            date = types.Date()
            datetime = types.DateTime()
            time = types.Time()

            sub = SubModel()

        my_model = MyModel()
        my_model.boolean = True
        my_model.float = 33.3
        my_model.integer = 22
        my_model.string = "string"
        my_model.date = date(2018, 1, 18)
        my_model.datetime = datetime(2018, 1, 18, 13, 14, 15)
        my_model.time = time(12, 13, 14)
        my_model.sub.name = "name"

        serialized = my_model.as_serializable()
        self.assertTrue(isinstance(serialized, dict))
        self.assertEquals(serialized["boolean"], True)
        self.assertEquals(serialized["float"], 33.3)
        self.assertEquals(serialized["integer"], 22)
        self.assertEquals(serialized["string"], "string")
        self.assertEquals(serialized["date"], "2018-01-18")
        self.assertEquals(serialized["datetime"], "2018-01-18 13:14:15")
        self.assertEquals(serialized["time"], "12:13:14")
        self.assertEquals(serialized["sub"]["name"], "name")

    def test_as_serializable_minified(self):
        from datetime import date
        from datetime import datetime
        from datetime import time

        class SubModel(types.Model):
            name = types.String()

        class MyModel(types.Model):
            boolean = types.Boolean()
            date = types.Date()
            datetime = types.DateTime()
            float = types.Float()
            integer = types.Integer()
            string = types.String()
            sub = SubModel()
            time = types.Time()

        my_model = MyModel()
        my_model.boolean = True
        my_model.float = 33.3
        my_model.integer = 22
        my_model.string = "string"
        my_model.date = date(2018, 1, 18)
        my_model.datetime = datetime(2018, 1, 18, 13, 14, 15)
        my_model.time = time(12, 13, 14)
        my_model.sub.name = "name"

        serialized = my_model.as_serializable(minified=True)
        self.assertTrue(isinstance(serialized, dict))
        self.assertEquals(serialized["a"], True)
        self.assertEquals(serialized["b"], "2018-01-18")
        self.assertEquals(serialized["c"], "2018-01-18 13:14:15")
        self.assertEquals(serialized["d"], 33.3)
        self.assertEquals(serialized["e"], 22)
        self.assertEquals(serialized["f"], "string")
        self.assertEquals(serialized["g"]["a"], "name")
        self.assertEquals(serialized["h"], "12:13:14")

    def test_as_serializable_filtered_default_true(self):
        from datetime import date
        from datetime import datetime
        from datetime import time
        from prestans.parser import AttributeFilter

        class SubModel(types.Model):
            name = types.String()

        class MyModel(types.Model):
            boolean = types.Boolean()
            date = types.Date()
            datetime = types.DateTime()
            float = types.Float()
            integer = types.Integer()
            string = types.String()
            sub = SubModel()
            time = types.Time()

        my_model = MyModel()
        my_model.boolean = True
        my_model.float = 33.3
        my_model.integer = 22
        my_model.string = "string"
        my_model.date = date(2018, 1, 18)
        my_model.datetime = datetime(2018, 1, 18, 13, 14, 15)
        my_model.time = time(12, 13, 14)
        my_model.sub.name = "name"

        attribute_filter = AttributeFilter.from_model(MyModel(), True)
        attribute_filter.float = False
        attribute_filter.string = False

        serialized = my_model.as_serializable(attribute_filter=attribute_filter)
        self.assertTrue(isinstance(serialized, dict))
        self.assertEquals(serialized["boolean"], True)
        self.assertTrue("float" not in serialized)
        self.assertEquals(serialized["integer"], 22)
        self.assertTrue("string" not in serialized)
        self.assertEquals(serialized["date"], "2018-01-18")
        self.assertEquals(serialized["datetime"], "2018-01-18 13:14:15")
        self.assertEquals(serialized["time"], "12:13:14")
        self.assertEquals(serialized["sub"]["name"], "name")

    def test_as_serializable_filtered_default_false(self):
        from datetime import date
        from datetime import datetime
        from datetime import time
        from prestans.parser import AttributeFilter

        class SubModel(types.Model):
            name = types.String()

        class MyModel(types.Model):
            boolean = types.Boolean()
            date = types.Date()
            datetime = types.DateTime()
            float = types.Float()
            integer = types.Integer()
            string = types.String()
            sub = SubModel()
            time = types.Time()

        my_model = MyModel()
        my_model.boolean = True
        my_model.float = 33.3
        my_model.integer = 22
        my_model.string = "string"
        my_model.date = date(2018, 1, 18)
        my_model.datetime = datetime(2018, 1, 18, 13, 14, 15)
        my_model.time = time(12, 13, 14)
        my_model.sub.name = "name"

        attribute_filter = AttributeFilter.from_model(MyModel(), False)
        attribute_filter.float = True
        attribute_filter.string = True

        serialized = my_model.as_serializable(attribute_filter=attribute_filter)
        self.assertEquals(serialized, {"float": 33.3, "string": "string"})

        attribute_filter = AttributeFilter.from_model(MyModel(), False)
        attribute_filter.sub.name = True

        serialized = my_model.as_serializable(attribute_filter=attribute_filter)
        self.assertEquals(serialized, {"sub": {"name": "name"}})

    def test_as_serializable_filtered_only_child_of_type_model(self):
        from prestans.parser import AttributeFilter

        class SubModel(types.Model):
            name = types.String()

        class ParentModel(types.Model):
            sub = SubModel()

        attribute_filter = AttributeFilter.from_model(ParentModel(), False)
        attribute_filter.sub.name = True

        parent_model = ParentModel()
        parent_model.sub.name = "james"

        serialized = parent_model.as_serializable(attribute_filter=attribute_filter)
        self.assertEquals(serialized, {"sub": {"name": "james"}})

    def test_none_attributes_skips_further_checks(self):
        class Person(types.Model):
            first_name = types.String(required=True)
            last_name = types.String(required=False)

        person = Person(first_name="Carol")
        serialized = person.as_serializable()
        self.assertEquals(serialized["first_name"], "Carol")
        self.assertEquals(serialized["last_name"], None)



class ModelValidate(unittest.TestCase):
    def test_required_rejects_none(self):

        class MyModel(types.Model):
            pass

        self.assertRaises(exception.RequiredAttributeError, MyModel(required=True).validate, None)

    def test_required_rejects_non_dict_type(self):

        class MyModel(types.Model):
            pass

        self.assertRaises(exception.RequiredAttributeError, MyModel(required=True).validate, False)
        self.assertRaises(exception.RequiredAttributeError, MyModel(required=True).validate, 3)
        self.assertRaises(exception.RequiredAttributeError, MyModel(required=True).validate, 3.33)
        self.assertRaises(exception.RequiredAttributeError, MyModel(required=True).validate, "string")

    def test_not_required_accepts_none(self):
        class MyModel(types.Model):
            pass

        self.assertEquals(MyModel(required=False).validate(None), None)

    def test_sets_none_for_invisible_attributes(self):
        class MyModel(types.Model):
            visible = types.String(default="visible")
            invisible = types.String(default="invisible")

        my_model = MyModel()
        self.assertEquals(my_model.visible, "visible")
        self.assertEquals(my_model.invisible, "invisible")

        attribute_filter = AttributeFilter.from_model(MyModel(), default_value=False)
        attribute_filter.visible = True

        validated = my_model.validate({}, attribute_filter)
        self.assertEquals(validated.visible, "visible")
        self.assertIsNone(validated.invisible)

        attribute_filter.visible = False
        attribute_filter.invisible = True

        validated = my_model.validate({}, attribute_filter)
        self.assertIsNone(validated.visible)
        self.assertEquals(validated.invisible, "invisible")

    def test_rejects_bad_attribute_type(self):

        class MyModel(types.Model):
            bad_attribute_type = "string"

        self.assertRaises(TypeError, MyModel().validate, {})

    def test_child_data_collection(self):
        class ChildModel(types.Model):
            age = types.Integer()

        class ParentModel(types.Model):
            name = types.String()
            child = ChildModel()

        parent_model = ParentModel()
        parent_model.name = "Nathan"
        parent_model.child.age = 30

        validated = ParentModel().validate(parent_model.as_serializable())
        self.assertEquals(validated.name, "Nathan")
        self.assertEquals(validated.child.age, 30)

    def test_child_data_collection_filtered(self):
        class ChildModel(types.Model):
            name = types.String()
            age = types.Integer()

        class ParentModel(types.Model):
            name = types.String()
            child = ChildModel()
            percent = types.Float()

        parent_model = ParentModel()
        parent_model.name = "Nathan"
        parent_model.percent = 33.3
        parent_model.child.name = "Steve"
        parent_model.child.age = 30

        parent_filter = AttributeFilter.from_model(ParentModel(default=False))
        parent_filter.name = True
        parent_filter.percent = True
        parent_filter.child.name = True
        parent_filter.child.age = True

        validated = ParentModel().validate(parent_model.as_serializable(attribute_filter=parent_filter))
        self.assertEquals(validated.name, "Nathan")
        self.assertEquals(validated.percent, 33.3)
        self.assertEquals(validated.child.name, "Steve")
        self.assertEquals(validated.child.age, 30)

        parent_filter.name = False
        parent_filter.child.name = False

        validated = ParentModel().validate(
            parent_model.as_serializable(attribute_filter=parent_filter),
            attribute_filter=parent_filter
        )
        self.assertEquals(validated.name, None)
        self.assertEquals(validated.percent, 33.3)
        self.assertEquals(validated.child.name, None)
        self.assertEquals(validated.child.age, 30)

    def test_minified_true(self):
        class Person(types.Model):
            first_name = types.String()
            last_name = types.String()

        person = Person(first_name="john", last_name="smith")
        person_validated = person.validate(person.as_serializable(minified=True), minified=True)
        self.assertEquals(person_validated.as_serializable(), {"first_name": "john", "last_name": "smith"})
        self.assertEquals(person_validated.as_serializable(minified=True), {"a_c": "john", "b_c": "smith"})

    def test_child_failing_to_validate_raises_validation_error(self):
        class Person(types.Model):
            first_name = types.String(required=True)
            last_name = types.String(required=True)

        person = Person(first_name="john")
        self.assertRaises(exception.ValidationError, Person().validate, person.as_serializable())
