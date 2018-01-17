import unittest

from prestans import types
from prestans.parser import VerbConfig


class VerbConfigTest(unittest.TestCase):

    def test_init(self):
        pass

    def test_blueprint(self):
        verb_config = VerbConfig()
        blueprint = verb_config.blueprint()
        self.assertIsNone(blueprint["response_template"])
        self.assertEquals(blueprint["parameter_sets"], [])
        self.assertIsNone(blueprint["body_template"])
        self.assertIsNone(blueprint["request_attribute_filter"])

        class MyModel(types.Model):
            pass

        response_template = MyModel()
        parameter_sets = []
        body_template = MyModel()
        request_attribute_filter = None

        verb_config = VerbConfig(
            response_template=response_template,
            parameter_sets=parameter_sets,
            body_template=body_template
        )
        blueprint = verb_config.blueprint()
        self.assertEquals(blueprint["response_template"], response_template.blueprint())
        self.assertEquals(blueprint["parameter_sets"], parameter_sets)
        self.assertEquals(blueprint["body_template"], body_template.blueprint())

    def test_response_template(self):

        class MyModel(types.Model):
            pass

        model = MyModel()
        verb_config = VerbConfig(response_template=model)
        self.assertEquals(verb_config.response_template, model)

    def test_response_attribute_filter_template(self):
        pass

    def test_parameter_sets(self):
        pass

    def test_body_template(self):
        class MyModel(types.Model):
            pass

        model = MyModel()
        verb_config = VerbConfig(body_template=model)
        self.assertEquals(verb_config.body_template, model)

    def test_request_attribute_filter(self):
        pass


def test_verb_config_boolean_array():
    boolean_array = types.Array(element_template=types.Boolean())
    VerbConfig(response_template=boolean_array)


def test_verb_config_float_array():
    float_array = types.Array(element_template=types.Float())
    VerbConfig(response_template=float_array)


def test_verb_config_integer_array():
    integer_array = types.Array(element_template=types.Integer())
    VerbConfig(response_template=integer_array)


def test_verb_config_string_array():
    string_array = types.Array(element_template=types.String())
    VerbConfig(response_template=string_array)
