from prestans.ext.data import adapters
from prestans.ext.data.adapters import sqlalchemy
from prestans.parser.attribute_filter import AttributeFilter
from prestans import types

import unittest


class UserPersistent(object):
    first_name = "first"
    last_name = "last"


class AddressPersistent(object):
    street = "street"


class UserREST(types.Model):
    first_name = types.String()
    last_name = types.String()


class AuthorREST(types.Model):
    first_name = types.String()
    last_name = types.String()


class AddressREST(types.Model):
    street = types.String()


adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
    rest_model_class=UserREST,
    persistent_model_class=UserPersistent
))

adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
    rest_model_class=AuthorREST,
    persistent_model_class=UserPersistent
))


class Issue84(unittest.TestCase):
    def test_correct_adaption(self):

        user = UserPersistent()
        user.first_name = "James"
        user.last_name = "Hetfield"

        attribute_filter = AttributeFilter.from_model(UserREST(), False)
        attribute_filter.first_name = True

        adapted_user = sqlalchemy.adapt_persistent_instance(user, UserREST, attribute_filter)
        self.assertEquals(adapted_user.first_name, "James")
        self.assertIsNone(adapted_user.last_name)

    def test_incorrect_adaption_raises_exception(self):
        address = AddressPersistent()
        address.street = "123 Fake Street"

        import logging
        for key, value in iter(adapters.registry._persistent_map.items()):
            logging.error(key+" -> "+value.rest_model_class.__name__)

        for key, value in iter(adapters.registry._rest_map.items()):
            logging.error(key+" -> "+value.persistent_model_class.__name__)

        self.assertRaises(TypeError, sqlalchemy.adapt_persistent_instance, address, UserREST)

