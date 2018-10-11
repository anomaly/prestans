import unittest

from prestans.devel.gen.closure import BasicTypeElementTemplate
from prestans import types


class BasicTypeElementTemplateTest(unittest.TestCase):

    def test_string_default(self):
        string_type = types.String()

        string = BasicTypeElementTemplate(string_type.blueprint())
        self.assertEqual(string.blueprint_type, "string")
        self.assertEqual(string.client_class_name, "String")
        self.assertEqual(string.required, "true")
        self.assertEqual(string.trim, "true")
        self.assertEqual(string.default, "null")
        self.assertEqual(string.min_length, "null")
        self.assertEqual(string.max_length, "null")
        self.assertEqual(string.format, "null")
        self.assertEqual(string.choices, "null")

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
        self.assertEqual(string.blueprint_type, "string")
        self.assertEqual(string.client_class_name, "String")
        self.assertEqual(string.required, "false")
        self.assertEqual(string.trim, "false")
        self.assertEqual(string.default, "\"default\"")
        self.assertEqual(string.min_length, 1)
        self.assertEqual(string.max_length, 5)
        self.assertEqual(string.format, "\"[a-z]{2, 8}\"")
        self.assertEqual(string.choices, ["a", "b", "c"])

    def test_integer_default(self):
        integer_type = types.Integer()

        integer = BasicTypeElementTemplate(integer_type.blueprint())
        self.assertEqual(integer.blueprint_type, "integer")
        self.assertEqual(integer.client_class_name, "Integer")
        self.assertEqual(integer.required, "true")
        self.assertEqual(integer.default, "null")
        self.assertEqual(integer.minimum, "null")
        self.assertEqual(integer.maximum, "null")
        self.assertEqual(integer.choices, "null")

    def test_integer_given_values(self):
        integer_type = types.Integer(
            required=False,
            default=3,
            minimum=1,
            maximum=5,
            choices=[1, 3, 5]
        )

        integer = BasicTypeElementTemplate(integer_type.blueprint())
        self.assertEqual(integer.blueprint_type, "integer")
        self.assertEqual(integer.client_class_name, "Integer")
        self.assertEqual(integer.required, "false")
        self.assertEqual(integer.default, 3)
        self.assertEqual(integer.minimum, 1)
        self.assertEqual(integer.maximum, 5)
        self.assertEqual(integer.choices, [1, 3, 5])

    def test_float_default(self):
        float_type = types.Float()

        float_basic = BasicTypeElementTemplate(float_type.blueprint())
        self.assertEqual(float_basic.blueprint_type, "float")
        self.assertEqual(float_basic.client_class_name, "Float")
        self.assertEqual(float_basic.required, "true")
        self.assertEqual(float_basic.default, "null")
        self.assertEqual(float_basic.minimum, "null")
        self.assertEqual(float_basic.maximum, "null")
        self.assertEqual(float_basic.choices, "null")

    def test_float_given_values(self):
        float_type = types.Float(
            required=False,
            default=4.56,
            minimum=1.0,
            maximum=5.0,
            choices=[1.0, 4.56, 5.0]
        )

        float_basic = BasicTypeElementTemplate(float_type.blueprint())
        self.assertEqual(float_basic.blueprint_type, "float")
        self.assertEqual(float_basic.client_class_name, "Float")
        self.assertEqual(float_basic.required, "false")
        self.assertEqual(float_basic.default, 4.56)
        self.assertEqual(float_basic.minimum, 1.0)
        self.assertEqual(float_basic.maximum, 5.0)
        self.assertEqual(float_basic.choices, [1.0, 4.56, 5.0])

    def test_boolean_default(self):
        boolean_type = types.Boolean()

        string = BasicTypeElementTemplate(boolean_type.blueprint())
        self.assertEqual(string.blueprint_type, "boolean")
        self.assertEqual(string.client_class_name, "Boolean")
        self.assertEqual(string.required, "true")
        self.assertEqual(string.default, "null")

    def test_boolean_given_values(self):
        boolean_type = types.Boolean(
            required=False,
            default=True
        )

        string = BasicTypeElementTemplate(boolean_type.blueprint())
        self.assertEqual(string.blueprint_type, "boolean")
        self.assertEqual(string.client_class_name, "Boolean")
        self.assertEqual(string.required, "false")
        self.assertEqual(string.default, "true")

        boolean_type = types.Boolean(
            required=False,
            default=False
        )

        string = BasicTypeElementTemplate(boolean_type.blueprint())
        self.assertEqual(string.blueprint_type, "boolean")
        self.assertEqual(string.client_class_name, "Boolean")
        self.assertEqual(string.required, "false")
        self.assertEqual(string.default, "false")
