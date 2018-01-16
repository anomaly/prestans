import unittest

from prestans.http import VERB
from prestans.parser import Config
from prestans.parser import ParameterSet
from prestans.parser import VerbConfig
from prestans import types


class ParameterSetTest(unittest.TestCase):

    def test_invalid_blueprint(self):

        class MyParameterSet(ParameterSet):
            name = types.String()

        self.assertRaises(TypeError, MyParameterSet.blueprint)

    def test_valid_blueprint(self):
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
        self.assertEquals(blueprint["type"], "tests.test_parser.MyParameterSet")

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

    def test_validate(self):
        pass


class AttributeFilterTest(unittest.TestCase):

    def test_init(self):
        pass

    def test_from_model(self):
        pass

    def test_conforms_to_template_filter(self):
        pass

    def test_keys(self):
        pass

    def test_has_key(self):
        pass

    def test_is_filter_at_key(self):
        pass

    def test_is_attribute_visible(self):
        pass

    def test_are_any_attributes_visible(self):
        pass

    def test_are_all_attributes_visible(self):
        pass

    def test_set_all_attribute_values(self):
        pass

    def test_as_dict(self):
        pass

    def test_init_from_dictionary(self):
        pass

    def test_setattr(self):
        pass


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


class ConfigTest(unittest.TestCase):

    def test_init(self):
        # check that invalid config raises exception
        self.assertRaises(TypeError, Config, GET="string")
        self.assertRaises(TypeError, Config, GET=VerbConfig(), HEAD="string")
        self.assertRaises(TypeError, Config, HEAD="string")
        self.assertRaises(TypeError, Config, POST="string")
        self.assertRaises(TypeError, Config, PUT="string")
        self.assertRaises(TypeError, Config, PATCH="string")
        self.assertRaises(TypeError, Config, DELETE="string")
        self.assertRaises(TypeError, Config, OPTIONS="string", PATCH=VerbConfig())

    def test_get_config_for_verb(self):
        get_verb_config = VerbConfig()
        head_verb_config = VerbConfig()
        post_verb_config = VerbConfig()
        put_verb_config = VerbConfig()
        patch_verb_config = VerbConfig()
        delete_verb_config = VerbConfig()
        options_verb_config = VerbConfig()

        config = Config(
            GET=get_verb_config,
            HEAD=head_verb_config,
            POST=post_verb_config,
            PUT=put_verb_config,
            PATCH=patch_verb_config,
            DELETE=delete_verb_config,
            OPTIONS=options_verb_config
        )
        self.assertEquals(config.get_config_for_verb(VERB.GET), get_verb_config)
        self.assertEquals(config.get_config_for_verb(VERB.HEAD), head_verb_config)
        self.assertEquals(config.get_config_for_verb(VERB.POST), post_verb_config)
        self.assertEquals(config.get_config_for_verb(VERB.PUT), put_verb_config)
        self.assertEquals(config.get_config_for_verb(VERB.PATCH), patch_verb_config)
        self.assertEquals(config.get_config_for_verb(VERB.DELETE), delete_verb_config)
        self.assertEquals(config.get_config_for_verb(VERB.OPTIONS), options_verb_config)

    def test_get(self):
        verb_config = VerbConfig()

        config = Config(GET=verb_config)
        self.assertEquals(config.get, verb_config)

    def test_head(self):
        verb_config = VerbConfig()

        config = Config(HEAD=verb_config)
        self.assertEquals(config.head, verb_config)

    def test_post(self):
        verb_config = VerbConfig()

        config = Config(POST=verb_config)
        self.assertEquals(config.post, verb_config)

    def test_put(self):
        verb_config = VerbConfig()

        config = Config(PUT=verb_config)
        self.assertEquals(config.put, verb_config)

    def test_patch(self):
        verb_config = VerbConfig()

        config = Config(PATCH=verb_config)
        self.assertEquals(config.patch, verb_config)

    def test_delete(self):
        verb_config = VerbConfig()

        config = Config(DELETE=verb_config)
        self.assertEquals(config.delete, verb_config)

    def test_options(self):
        verb_config = VerbConfig()

        config = Config(OPTIONS=verb_config)
        self.assertEquals(config.options, verb_config)
