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


class Issue84(unittest.TestCase):

    def setUp(self):
        adapters.registry.register_persistent_rest_pair(UserPersistent, UserREST)
        adapters.registry.register_persistent_rest_pair(UserPersistent, AuthorREST)

    def tearDown(self):
        adapters.registry.clear_registered_adapters()

    def test_correct_adaption_collection(self):

        user = UserPersistent()
        user.first_name = "James"
        user.last_name = "Hetfield"

        users = [user]

        attribute_filter = AttributeFilter.from_model(UserREST(), False)
        attribute_filter.first_name = True

        adapted_users = sqlalchemy.adapt_persistent_collection(users, UserREST, attribute_filter)
        self.assertEquals(adapted_users[0].first_name, "James")
        self.assertIsNone(adapted_users[0].last_name)

    def test_correct_adaption_instance(self):

        user = UserPersistent()
        user.first_name = "James"
        user.last_name = "Hetfield"

        attribute_filter = AttributeFilter.from_model(UserREST(), False)
        attribute_filter.first_name = True

        adapted_user = sqlalchemy.adapt_persistent_instance(user, UserREST, attribute_filter)
        self.assertEquals(adapted_user.first_name, "James")
        self.assertIsNone(adapted_user.last_name)

    def test_incorrect_adaption_raises_exception_collection(self):
        address = AddressPersistent()
        address.street = "123 Fake Street"

        addresses = [address]

        self.assertRaises(TypeError, sqlalchemy.adapt_persistent_collection, addresses, UserREST)

    def test_incorrect_adaption_raises_exception_instance(self):
        address = AddressPersistent()
        address.street = "123 Fake Street"

        self.assertRaises(TypeError, sqlalchemy.adapt_persistent_instance, address, UserREST)

