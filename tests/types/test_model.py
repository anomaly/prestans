import unittest

from prestans import exception
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

        class ModelWithBadAttribute(types.Model):
            name = "string"

        self.assertRaises(TypeError, ModelWithBadAttribute().blueprint)

    def test_setattr(self):
        class MyModel(types.Model):
            name = types.String()
            age = types.Integer(maximum=120)

        my_model = MyModel()
        my_model.name = "name"
        my_model.age = 21
        self.assertEquals(my_model.name, "name")
        self.assertEquals(my_model.age, 21)
        self.assertRaises(KeyError, my_model.__setattr__, "missing", "missing")
        self.assertRaises(exception.ValidationError, my_model.__setattr__, "age", 121)

    def test_get_attribute_keys(self):
        class MyModel(types.Model):
            name = types.String()
            tags = types.Array(element_template=types.String())

        my_model = MyModel()
        self.assertEquals(my_model.get_attribute_keys(), ["name", "tags"])

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

    def test_validate(self):

        # check validate fails when None is passed to required
        class MyModel(types.Model):
            pass

        self.assertRaises(exception.RequiredAttributeError, MyModel(required=True).validate, None)

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

    def test_has_key(self):

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
        self.assertTrue(my_model.has_key("name"))
        self.assertTrue(my_model.has_key("birthday"))
        self.assertTrue(my_model.has_key("tags"))
        self.assertTrue(my_model.has_key("sub"))
        self.assertTrue(my_model.has_key("sub_array"))
        self.assertFalse(my_model.has_key("missing"))

        # check if keys can be found in model and base class
        class ModelWithSingleBase(MyModel):
            extra = types.String()

        single_base = ModelWithSingleBase()
        self.assertTrue(single_base.has_key("name"))
        self.assertTrue(single_base.has_key("birthday"))
        self.assertTrue(single_base.has_key("tags"))
        self.assertTrue(single_base.has_key("sub"))
        self.assertTrue(single_base.has_key("sub_array"))
        self.assertTrue(single_base.has_key("extra"))
        self.assertFalse(single_base.has_key("missing"))

        class ModelWithMultiBase(ModelWithSingleBase):
            another = types.String()

        multi_base = ModelWithMultiBase()
        self.assertTrue(multi_base.has_key("name"))
        self.assertTrue(multi_base.has_key("birthday"))
        self.assertTrue(multi_base.has_key("tags"))
        self.assertTrue(multi_base.has_key("sub"))
        self.assertTrue(multi_base.has_key("sub_array"))
        self.assertTrue(multi_base.has_key("extra"))
        self.assertTrue(multi_base.has_key("another"))
        self.assertFalse(multi_base.has_key("missing"))

    def test__generate_attribute_token_rewrite_map(self):
        pass

    def test__generate_attribute_tokens(self):
        pass

    def test__generate_minified_keys(self):
        pass

    def test__generate_attribute_key(self):
        self.assertEquals(types.Model._generate_attribute_key(0), "a")
        self.assertEquals(types.Model._generate_attribute_key(1), "b")
        self.assertEquals(types.Model._generate_attribute_key(25), "z")
        self.assertEquals(types.Model._generate_attribute_key(26), "aa")
        self.assertEquals(types.Model._generate_attribute_key(27), "bb")
        self.assertEquals(types.Model._generate_attribute_key(51), "zz")
        self.assertEquals(types.Model._generate_attribute_key(52), "aaa")
        self.assertEquals(types.Model._generate_attribute_key(54), "ccc")
        self.assertEquals(types.Model._generate_attribute_key(77), "zzz")

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

    def test_as_serializable_filtered(self):
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
