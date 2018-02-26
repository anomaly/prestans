import unittest

from prestans.devel.gen.closure import BasicTypeElementTemplate
from prestans import types


class BasicTypeElementTemplateTest(unittest.TestCase):

    def test_string_default(self):
        string_type = types.String()

        string = BasicTypeElementTemplate(string_type.blueprint())
        self.assertEquals(string.blueprint_type, "string")
        self.assertEquals(string.client_class_name, "String")
        self.assertEquals(string.required, "true")
        self.assertEquals(string.trim, "true")
        self.assertEquals(string.default, "null")
        self.assertEquals(string.min_length, "null")
        self.assertEquals(string.max_length, "null")
        self.assertEquals(string.format, "null")
        self.assertEquals(string.choices, "null")

    def test_string_given_values(self):
        string_type = types.String(
            required=False,
            trim=False,
            default="default",
            min_length=1,
            max_length=5,
            format="[a-z]{2, 8}",
            choices=["a", "b", "c"]
        )

        string = BasicTypeElementTemplate(string_type.blueprint())
        self.assertEquals(string.blueprint_type, "string")
        self.assertEquals(string.client_class_name, "String")
        self.assertEquals(string.required, "false")
        self.assertEquals(string.trim, "false")
        self.assertEquals(string.default, "\"default\"")
        self.assertEquals(string.min_length, 1)
        self.assertEquals(string.max_length, 5)
        self.assertEquals(string.format, "\"[a-z]{2, 8}\"")
        self.assertEquals(string.choices, ["a", "b", "c"])

    def test_integer_default(self):
        integer_type = types.Integer()

        integer = BasicTypeElementTemplate(integer_type.blueprint())
        self.assertEquals(integer.blueprint_type, "integer")
        self.assertEquals(integer.client_class_name, "Integer")
        self.assertEquals(integer.required, "true")
        self.assertEquals(integer.default, "null")
        self.assertEquals(integer.minimum, "null")
        self.assertEquals(integer.maximum, "null")
        self.assertEquals(integer.choices, "null")

    def test_integer_given_values(self):
        integer_type = types.Integer(
            required=False,
            default=3,
            minimum=1,
            maximum=5,
            choices=[1, 3, 5]
        )

        integer = BasicTypeElementTemplate(integer_type.blueprint())
        self.assertEquals(integer.blueprint_type, "integer")
        self.assertEquals(integer.client_class_name, "Integer")
        self.assertEquals(integer.required, "false")
        self.assertEquals(integer.default, 3)
        self.assertEquals(integer.minimum, 1)
        self.assertEquals(integer.maximum, 5)
        self.assertEquals(integer.choices, [1, 3, 5])

    def test_float_default(self):
        float_type = types.Float()

        float_basic = BasicTypeElementTemplate(float_type.blueprint())
        self.assertEquals(float_basic.blueprint_type, "float")
        self.assertEquals(float_basic.client_class_name, "Float")
        self.assertEquals(float_basic.required, "true")
        self.assertEquals(float_basic.default, "null")
        self.assertEquals(float_basic.minimum, "null")
        self.assertEquals(float_basic.maximum, "null")
        self.assertEquals(float_basic.choices, "null")

    def test_float_given_values(self):
        float_type = types.Float(
            required=False,
            default=4.56,
            minimum=1.0,
            maximum=5.0,
            choices=[1.0, 4.56, 5.0]
        )

        float_basic = BasicTypeElementTemplate(float_type.blueprint())
        self.assertEquals(float_basic.blueprint_type, "float")
        self.assertEquals(float_basic.client_class_name, "Float")
        self.assertEquals(float_basic.required, "false")
        self.assertEquals(float_basic.default, 4.56)
        self.assertEquals(float_basic.minimum, 1.0)
        self.assertEquals(float_basic.maximum, 5.0)
        self.assertEquals(float_basic.choices, [1.0, 4.56, 5.0])

    def test_boolean_default(self):
        boolean_type = types.Boolean()

        string = BasicTypeElementTemplate(boolean_type.blueprint())
        self.assertEquals(string.blueprint_type, "boolean")
        self.assertEquals(string.client_class_name, "Boolean")
        self.assertEquals(string.required, "true")
        self.assertEquals(string.default, "null")

    def test_boolean_given_values(self):
        boolean_type = types.Boolean(
            required=False,
            default=True
        )

        string = BasicTypeElementTemplate(boolean_type.blueprint())
        self.assertEquals(string.blueprint_type, "boolean")
        self.assertEquals(string.client_class_name, "Boolean")
        self.assertEquals(string.required, "false")
        self.assertEquals(string.default, "true")

        boolean_type = types.Boolean(
            required=False,
            default=False
        )

        string = BasicTypeElementTemplate(boolean_type.blueprint())
        self.assertEquals(string.blueprint_type, "boolean")
        self.assertEquals(string.client_class_name, "Boolean")
        self.assertEquals(string.required, "false")
        self.assertEquals(string.default, "false")
