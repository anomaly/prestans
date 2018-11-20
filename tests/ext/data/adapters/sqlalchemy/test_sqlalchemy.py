import unittest

from prestans.ext.data import adapters
from prestans.ext.data.adapters import sqlalchemy
from prestans.parser import AttributeFilter
from prestans import types


class SQLAlchemyDataAdapterAdaptPersistentInstance(unittest.TestCase):

    def test_children_of_type_data_type(self):

        class RESTModel(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

        class PersistentModel(object):

            def __init__(self):
                self.boolean = False
                self.float = 33.3
                self.integer = 33
                self.string = "string"

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=RESTModel,
            persistent_model_class=PersistentModel
        ))

        attribute_filter = AttributeFilter.from_model(RESTModel(), False)
        attribute_filter.string = True

        persistent_model = PersistentModel()
        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModel, attribute_filter)
        self.assertEqual(adapted_model.string, "string")

        attribute_filter.boolean = True
        attribute_filter.float = True
        attribute_filter.integer = True

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModel, attribute_filter)
        self.assertEqual(adapted_model.boolean, False)
        self.assertEqual(adapted_model.float, 33.3)
        self.assertEqual(adapted_model.integer, 33)

    def test_single_child_of_type_data_collection(self):

        class ChildREST(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

        class ParentREST(types.Model):
            child = ChildREST()

        class ChildPersistent(object):

            def __init__(self):
                self.integer = 33
                self.string = "string"

            @property
            def boolean(self):
                return False

            @property
            def float(self):
                return 33.3

        class ParentPersistent(object):

            @property
            def child(self):
                return ChildPersistent()

        adapters.registry.register_persistent_rest_pair(ParentPersistent, ParentREST)
        adapters.registry.register_persistent_rest_pair(ChildPersistent, ChildREST)

        attribute_filter = AttributeFilter.from_model(ParentREST(), False)
        attribute_filter.child.boolean = True
        attribute_filter.child.float = True
        attribute_filter.child.integer = True
        attribute_filter.child.string = True

        self.assertTrue(attribute_filter.is_attribute_visible("child"))
        self.assertTrue(attribute_filter.child.boolean)
        self.assertTrue(attribute_filter.child.float)
        self.assertTrue(attribute_filter.child.integer)
        self.assertTrue(attribute_filter.child.string)

        persistent_model = ParentPersistent()

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, ParentREST, attribute_filter)
        self.assertEqual(adapted_model.child.boolean, False)
        self.assertEqual(adapted_model.child.float, 33.3)
        self.assertEqual(adapted_model.child.integer, 33)
        self.assertEqual(adapted_model.child.string, "string")

    def test_children_of_type_data_type_and_data_collection(self):

        class ChildREST(types.Model):
            c_boolean = types.Boolean()
            c_float = types.Float()
            c_integer = types.Integer()
            c_string = types.String()

        class ParentREST(types.Model):
            p_boolean = types.Boolean()
            p_float = types.Float()
            p_integer = types.Integer()
            p_string = types.String()

            child = ChildREST()

        class ChildPersistent(object):

            def __init__(self):
                self.c_boolean = True
                self.c_float = 44.4
                self.c_integer = 44
                self.c_string = "string_c"

        class ParentPersistent(object):

            def __init__(self):
                self.p_boolean = False
                self.p_float = 33.3
                self.p_integer = 33
                self.p_string = "string_p"

            @property
            def child(self):
                return ChildPersistent()

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=ParentREST,
            persistent_model_class=ParentPersistent
        ))

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=ChildREST,
            persistent_model_class=ChildPersistent
        ))

        attribute_filter = AttributeFilter.from_model(ParentREST(), False)

        self.assertFalse(attribute_filter.as_immutable().p_boolean)
        self.assertFalse(attribute_filter.as_immutable().p_float)
        self.assertFalse(attribute_filter.as_immutable().p_integer)
        self.assertFalse(attribute_filter.as_immutable().p_string)
        self.assertFalse(attribute_filter.as_immutable().is_attribute_visible("child"))
        self.assertFalse(attribute_filter.as_immutable().child.c_boolean)
        self.assertFalse(attribute_filter.as_immutable().child.c_float)
        self.assertFalse(attribute_filter.as_immutable().child.c_integer)
        self.assertFalse(attribute_filter.as_immutable().child.c_string)

        attribute_filter.p_boolean = True
        attribute_filter.p_float = True
        attribute_filter.p_integer = False
        attribute_filter.p_string = True
        attribute_filter.child.c_boolean = True
        attribute_filter.child.c_float = True
        attribute_filter.child.c_integer = True

        self.assertTrue(attribute_filter.p_boolean)
        self.assertTrue(attribute_filter.p_float)
        self.assertFalse(attribute_filter.p_integer)
        self.assertFalse(attribute_filter.is_attribute_visible("p_integer"))
        self.assertTrue(attribute_filter.p_string)
        self.assertTrue(attribute_filter.is_attribute_visible("child"))
        self.assertTrue(attribute_filter.child.c_boolean)
        self.assertTrue(attribute_filter.child.c_float)
        self.assertTrue(attribute_filter.child.c_integer)
        self.assertFalse(attribute_filter.child.is_attribute_visible("c_string"))
        self.assertFalse(attribute_filter.child.c_string)

        self.assertTrue(attribute_filter.as_immutable().p_boolean)
        self.assertTrue(attribute_filter.as_immutable().p_float)
        self.assertFalse(attribute_filter.as_immutable().p_integer)
        self.assertTrue(attribute_filter.as_immutable().p_string)
        self.assertTrue(attribute_filter.as_immutable().is_attribute_visible("child"))
        self.assertTrue(attribute_filter.as_immutable().child.c_boolean)
        self.assertTrue(attribute_filter.as_immutable().child.c_float)
        self.assertTrue(attribute_filter.as_immutable().child.c_integer)
        self.assertFalse(attribute_filter.as_immutable().child.c_string)

        persistent_model = ParentPersistent()
        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, ParentREST, attribute_filter)
        self.assertEqual(adapted_model.p_boolean, False)
        self.assertEqual(adapted_model.p_float, 33.3)
        self.assertIsNone(adapted_model.p_integer)
        self.assertEqual(adapted_model.p_string, "string_p")
        self.assertTrue(isinstance(adapted_model.child, ChildREST))
        self.assertEqual(adapted_model.child.c_boolean, True)
        self.assertEqual(adapted_model.child.c_float, 44.4)
        self.assertEqual(adapted_model.child.c_integer, 44)
        self.assertIsNone(adapted_model.child.c_string)

        attribute_filter.p_integer = True
        attribute_filter.child.c_string = True

        self.assertTrue(attribute_filter.p_integer)
        self.assertTrue(attribute_filter.child.c_string)

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, ParentREST, attribute_filter)
        self.assertEqual(adapted_model.p_boolean, False)
        self.assertEqual(adapted_model.p_float, 33.3)
        self.assertEqual(adapted_model.p_integer, 33)
        self.assertEqual(adapted_model.p_string, "string_p")
        self.assertTrue(isinstance(adapted_model.child, ChildREST))
        self.assertEqual(adapted_model.child.c_boolean, True)
        self.assertEqual(adapted_model.child.c_float, 44.4)
        self.assertEqual(adapted_model.child.c_integer, 44)
        self.assertEqual(adapted_model.child.c_string, "string_c")


class SQLAlchemyDataAdapterAdaptPersistentCollection(unittest.TestCase):

    def test_(self):
        pass
