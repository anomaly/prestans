import unittest

from prestans import types
from prestans.parser import AttributeFilter
from prestans.parser import ParameterSet
from prestans.parser import VerbConfig


class VerbConfigTest(unittest.TestCase):

    def test_init_response_template(self):
        class MyModel(types.Model):
            pass

        my_model = MyModel()
        verb_config = VerbConfig(response_template=my_model)
        self.assertEquals(verb_config.response_template, my_model)

        # todo: check correct attribute filter template is generated
        # self.assertEquals(verb_config.response_attribute_filter_template, AttributeFilter.from_model(
        #     model_instance=MyModel(),
        #     default_value=False
        # ))

        binary_response = types.BinaryResponse()
        self.assertEquals(VerbConfig(response_template=binary_response).response_template, binary_response)

        self.assertRaises(TypeError, VerbConfig, response_template="string")

    def test_init_response_attribute_filter_default_value(self):
        pass

    def test_init_parameter_sets_single(self):
        param_set = ParameterSet()

        self.assertRaises(TypeError, VerbConfig, parameter_sets="string")

        verb_config = VerbConfig(parameter_sets=param_set)
        self.assertEquals(verb_config.parameter_sets, [param_set])

    def test_init_parameter_sets_array(self):
        param_set1 = ParameterSet()
        param_set2 = ParameterSet()

        self.assertRaises(TypeError, VerbConfig, parameter_sets=[param_set1, "string"])

        verb_config = VerbConfig(parameter_sets=[param_set1, param_set2])
        self.assertEquals(verb_config.parameter_sets, [param_set1, param_set2])

    def test_init_body_template(self):
        class MyModel(types.Model):
            pass

        my_model = MyModel()
        self.assertEquals(VerbConfig(body_template=my_model).body_template, my_model)

        self.assertRaises(TypeError, VerbConfig, body_template="string")

    def test_init_request_attribute_filter(self):
        self.assertIsNone(VerbConfig().request_attribute_filter)

        attribute_filter = AttributeFilter()
        self.assertEquals(VerbConfig(request_attribute_filter=attribute_filter).request_attribute_filter, attribute_filter)
        self.assertRaises(TypeError, VerbConfig, request_attribute_filter="string")

    def test_blueprint_default(self):
        blueprint = VerbConfig().blueprint()
        self.assertIsNone(blueprint["response_template"])
        self.assertEquals(blueprint["parameter_sets"], [])
        self.assertIsNone(blueprint["body_template"])
        self.assertIsNone(blueprint["request_attribute_filter"])

    def test_blueprint(self):

        class MyModel(types.Model):
            pass

        class MyParamSet(ParameterSet):
            pass

        param_set = MyParamSet()
        response_template = MyModel()
        parameter_sets = [param_set, param_set]
        body_template = MyModel()
        attribute_filter = AttributeFilter({"name": True})

        verb_config = VerbConfig(
            response_template=response_template,
            parameter_sets=parameter_sets,
            body_template=body_template,
            request_attribute_filter=attribute_filter
        )
        blueprint = verb_config.blueprint()
        self.assertEquals(blueprint["response_template"], response_template.blueprint())
        self.assertEquals(blueprint["parameter_sets"], [param_set.blueprint(), param_set.blueprint()])
        self.assertEquals(blueprint["body_template"], body_template.blueprint())
        self.assertEquals(blueprint["request_attribute_filter"], attribute_filter.blueprint())

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

    def test_boolean_array(self):
        boolean_array = types.Array(element_template=types.Boolean())
        verb_config = VerbConfig(response_template=boolean_array)
        self.assertEquals(verb_config.response_template, boolean_array)

    def test_float_array(self):
        float_array = types.Array(element_template=types.Float())
        verb_config = VerbConfig(response_template=float_array)
        self.assertEquals(verb_config.response_template, float_array)

    def test_integer_array(self):
        integer_array = types.Array(element_template=types.Integer())
        verb_config = VerbConfig(response_template=integer_array)
        self.assertEquals(verb_config.response_template, integer_array)

    def test_string_array(self):
        string_array = types.Array(element_template=types.String())
        verb_config = VerbConfig(response_template=string_array)
        self.assertEquals(verb_config.response_template, string_array)
