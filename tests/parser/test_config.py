import unittest

from prestans.http import VERB
from prestans.parser import Config
from prestans.parser import VerbConfig


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
