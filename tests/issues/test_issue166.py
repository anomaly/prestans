from prestans.ext.data import adapters
from prestans.ext.data.adapters import sqlalchemy
from prestans import types

import unittest


class UserPersistent(object):
    first_name = "first"
    last_name = "last"


class UserREST(types.Model):
    first_name = types.String()
    last_name = types.String()


class AuthorREST(types.Model):
    first_name = types.String()
    last_name = types.String()


adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
    rest_model_class=UserREST,
    persistent_model_class=UserPersistent
))

adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
    rest_model_class=AuthorREST,
    persistent_model_class=UserPersistent
))


class Issue166(unittest.TestCase):

    def setUp(self):
        adapters.registry.register_persistent_rest_pair(UserPersistent, UserREST)
        adapters.registry.register_persistent_rest_pair(UserPersistent, AuthorREST)

    def tearDown(self):
        adapters.registry.clear_registered_adapters()

    def test_default_rest_model_lookup(self):

        model_adapter = adapters.registry.get_adapter_for_persistent_model(UserPersistent())
        self.assertEquals(model_adapter.rest_model_class, AuthorREST)
        self.assertNotEquals(model_adapter.rest_model_class, UserREST)

    def test_specific_rest_model_lookup(self):
        model_adapter1 = adapters.registry.get_adapter_for_persistent_model(UserPersistent(), UserREST)
        self.assertEquals(model_adapter1.rest_model_class, UserREST)
        self.assertNotEquals(model_adapter1.rest_model_class, AuthorREST)

        model_adapter2 = adapters.registry.get_adapter_for_persistent_model(UserPersistent(), AuthorREST)
        self.assertEquals(model_adapter2.rest_model_class, AuthorREST)
        self.assertNotEquals(model_adapter2.rest_model_class, UserREST)
