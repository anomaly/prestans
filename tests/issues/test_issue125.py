from prestans.ext.data import adapters
from prestans import types

from mock import patch
import unittest


class Person(object):
    def __init__(self):
        self.first_name = "John"

    @property
    def last_name(self):
        return "Doe"

    @classmethod
    def class_method(cls):
        return "class_method"


class PersonREST(types.Model):
    first_name = types.String()
    last_name = types.String()
    class_method = types.String()


class Issue125(unittest.TestCase):

    def setUp(self):
        adapters.registry.register_persistent_rest_pair(Person, PersonREST)

    def tearDown(self):
        adapters.registry.clear_registered_adapters()

    def test_class_method_not_called(self):

        person = Person()

        person_rest = adapters.adapt_persistent_instance(person, PersonREST)
        self.assertEquals(person_rest.first_name, person.first_name)
        self.assertEquals(person_rest.last_name, person.last_name)
        self.assertIsNone(person_rest.class_method)
