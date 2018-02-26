import unittest

from prestans.parser import ParameterSet
from prestans import types


class ParameterSetBlueprint(unittest.TestCase):

    def test_invalid(self):

        class BadAttribute(ParameterSet):
            name = types.String()
            invalid = "string"

        class MyModel(types.Model):
            name = types.String()

        class BadArray(ParameterSet):
            tags = types.Array(element_template=MyModel())

        self.assertRaises(TypeError, BadAttribute().blueprint)
        self.assertRaises(TypeError, BadArray().blueprint)

    def test_valid(self):
        class MyParameterSet(ParameterSet):

            name = types.String(
                default="Brad",
                min_length=3,
                max_length=32,
                required=False,
                format="[a-zA-Z]{3, 32}",
                utf_encoding="utf-16",
                description="name for param set",
                trim=False
            )
            tags = types.Array(element_template=types.String())

        parameter_set = MyParameterSet()
        blueprint = parameter_set.blueprint()
        self.assertEquals(blueprint["type"], "tests.parser.test_parameter_set.MyParameterSet")

        name_blueprint = blueprint["fields"]["name"]
        self.assertEquals(name_blueprint["type"], "string")
        self.assertEquals(name_blueprint["constraints"]["default"], "Brad")
        self.assertEquals(name_blueprint["constraints"]["min_length"], 3)
        self.assertEquals(name_blueprint["constraints"]["max_length"], 32)
        self.assertEquals(name_blueprint["constraints"]["required"], False)
        self.assertEquals(name_blueprint["constraints"]["format"], "[a-zA-Z]{3, 32}")
        self.assertEquals(name_blueprint["constraints"]["utf_encoding"], "utf-16")
        self.assertEquals(name_blueprint["constraints"]["description"], "name for param set")
        self.assertEquals(name_blueprint["constraints"]["trim"], False)

        tags_blueprint = blueprint["fields"]["tags"]
        self.assertEquals(tags_blueprint["type"], "array")
        # todo: fill this out with more checks


class ParameterSetValidate(unittest.TestCase):

    def test_bad_attribute_raises_type_error(self):
        from webob.request import Request
        request = Request({})

        class BadAttribute(ParameterSet):
            invalid = "string"

        self.assertRaises(TypeError, BadAttribute().validate, request)

    def test_model_array_raises_type_error(self):
        from webob.request import Request
        request = Request({})

        class MyModel(types.Model):
            name = types.String()

        class ModelArray(ParameterSet):
            model_array = types.Array(element_template=MyModel())

        self.assertRaises(TypeError, ModelArray().validate, request)

    def test_boolean_array_raises_type_error(self):
        from webob.request import Request
        request = Request({})

        class BooleanArray(ParameterSet):
            bool_array = types.Array(element_template=types.Boolean())

        self.assertRaises(TypeError, BooleanArray().validate, request)
