import unittest

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
        pass

    def test_setattr(self):
        pass

    def test_get_attribute_keys(self):
        pass

    def test_get_attribute_filter(self):
        pass

    def test_validate(self):
        pass

    def test_attribute_rewrite_map(self):
        pass

    def test_attribute_rewrite_reverse_map(self):
        pass

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

    def test__generate_minfied_keys(self):
        pass

    def test__generate_attribute_key(self):
        pass

    def test_as_serializable(self):
        pass