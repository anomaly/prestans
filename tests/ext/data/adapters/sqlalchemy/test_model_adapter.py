import unittest

from prestans import exception
from prestans.ext.data import adapters
from prestans import parser
from prestans import types


class Address(object):
    def __init__(self):
        self.street = "street"


class Person(object):

    def __init__(self):
        self.first_name = "first_name"
        self.last_name = "last_name"


class PersonWithAddress(Person):

    def __init__(self):
        super(PersonWithAddress, self).__init__()
        self.address = Address()


class PersonWithAddresses(Person):

    def __init__(self):
        super(PersonWithAddresses, self).__init__()
        self.addresses = []


class PersonWithBasicArrays(Person):

    def __init__(self):
        super(PersonWithBasicArrays, self).__init__()
        self.booleans = []
        self.floats = []
        self.integers = []
        self.strings = []


class AddressREST(types.Model):
    street = types.String()
    short_string = types.String(required=False, max_length=10)


class PersonREST(types.Model):
    first_name = types.String()
    last_name = types.String()
    short_string = types.String(max_length=10)

    address = AddressREST(required=False)

    addresses = types.Array(element_template=AddressREST())

    booleans = types.Array(element_template=types.Boolean())
    floats = types.Array(element_template=types.Float())
    integers = types.Array(element_template=types.Integer())
    strings = types.Array(element_template=types.String())


class ModelAdapterUnitTest(unittest.TestCase):

    def setUp(self):
        adapters.registry.register_persistent_rest_pair(Address, AddressREST)

    def tearDown(self):
        adapters.registry.clear_registered_adapters()

    def test_init_and_getters(self):

        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)
        self.assertEquals(model_adapter.rest_model_class, PersonREST)
        self.assertEquals(model_adapter.persistent_model_class, Person)

    def test_init_raises_type_error_for_invalid_rest_model(self):
        self.assertRaises(TypeError, adapters.ModelAdapter, rest_model_class=Person, persistent_model_class=None)

    def test_adapt_persistent_to_rest_no_filter(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)

        person = Person()
        person.first_name = "John"
        person.last_name = "Doe"

        person_rest = model_adapter.adapt_persistent_to_rest(person)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertEquals(person.first_name, person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)

    def test_adapt_persistent_to_rest_with_filter(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)

        person = Person()
        person.first_name = "John"
        person.last_name = "Doe"

        attribute_filter = parser.AttributeFilter.from_model(PersonREST(), default_value=False)
        attribute_filter.last_name = True

        person_rest = model_adapter.adapt_persistent_to_rest(person, attribute_filter)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertIsNone(person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)

    def test_adapt_persistent_to_rest_with_model_as_child(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)

        person = PersonWithAddress()
        person.first_name = "John"
        person.last_name = "Doe"
        person.address.street = "123 Street Address"

        attribute_filter = parser.AttributeFilter.from_model(PersonREST(), default_value=False)
        attribute_filter.last_name = True
        attribute_filter.address.street = True

        person_rest = model_adapter.adapt_persistent_to_rest(person, attribute_filter)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertEquals(person.address.street, "123 Street Address")
        self.assertIsNone(person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)
        self.assertEquals(person.address.street, person_rest.address.street)

    def test_adapt_persistent_to_rest_with_model_missing(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)

        person = PersonWithAddress()
        person.first_name = "John"
        person.last_name = "Doe"
        person.address = None

        person_rest = model_adapter.adapt_persistent_to_rest(person)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertEquals(person.first_name, person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)

    def test_adapt_persistent_to_rest_with_basic_arrays_as_children(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=PersonWithBasicArrays)

        person = PersonWithBasicArrays()
        person.first_name = "John"
        person.last_name = "Doe"
        person.booleans.append(True)
        person.floats.append(1.1)
        person.integers.append(2)
        person.strings.append("string")

        person_rest = model_adapter.adapt_persistent_to_rest(person)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertEquals(person.booleans, [True])
        self.assertEquals(person.floats, [1.1])
        self.assertEquals(person.integers, [2])
        self.assertEquals(person.strings, ["string"])

        self.assertEquals(person.first_name, person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)
        self.assertEquals(person.booleans, person_rest.booleans.as_serializable())
        self.assertEquals(person.floats, person_rest.floats.as_serializable())
        self.assertEquals(person.integers, person_rest.integers.as_serializable())
        self.assertEquals(person.strings, person_rest.strings.as_serializable())

    def test_adapt_persistent_to_rest_with_model_array_as_child(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=PersonWithAddresses)

        address = Address()
        address.street = "123 Street Address"

        person = PersonWithAddresses()
        person.first_name = "John"
        person.last_name = "Doe"
        person.addresses.append(address)

        person_rest = model_adapter.adapt_persistent_to_rest(person)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertEquals(person.addresses, [address])

        self.assertEquals(person.first_name, person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)
        self.assertEquals([{"short_string": None, "street": "123 Street Address"}], person_rest.addresses.as_serializable())

    def test_adapt_persistent_to_rest_with_model_array_as_child_filtered(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=PersonWithAddresses)

        address = Address()
        address.street = "123 Street Address"

        person = PersonWithAddresses()
        person.first_name = "John"
        person.last_name = "Doe"
        person.addresses.append(address)

        attribute_filter = parser.AttributeFilter.from_model(PersonREST(), default_value=False)
        attribute_filter.last_name = True
        attribute_filter.addresses.street = True

        person_rest = model_adapter.adapt_persistent_to_rest(person, attribute_filter)
        self.assertEquals(person.first_name, "John")
        self.assertEquals(person.last_name, "Doe")
        self.assertEquals(person.addresses, [address])

        self.assertIsNone(person_rest.first_name)
        self.assertEquals(person.last_name, person_rest.last_name)
        self.assertEquals([{"short_string": None, "street": "123 Street Address"}], person_rest.addresses.as_serializable())

    def test_adapt_persistent_to_rest_inconsistent_data_exception_raised_model(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)

        person = PersonWithAddress()
        person.address.short_string = "a longer string"

        self.assertRaises(exception.InconsistentPersistentDataError, model_adapter.adapt_persistent_to_rest, person)

    def test_adapt_persistent_to_rest_inconsistent_data_exception_raised_array(self):
        model_adapter = adapters.ModelAdapter(rest_model_class=PersonREST, persistent_model_class=Person)

        person = Person()
        person.short_string = "a longer string"

        self.assertRaises(exception.InconsistentPersistentDataError, model_adapter.adapt_persistent_to_rest, person)
