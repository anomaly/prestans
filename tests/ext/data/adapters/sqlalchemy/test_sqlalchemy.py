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
        self.assertEquals(adapted_model.string, "string")

        attribute_filter.boolean = True
        attribute_filter.float = True
        attribute_filter.integer = True

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModel, attribute_filter)
        self.assertEquals(adapted_model.boolean, False)
        self.assertEquals(adapted_model.float, 33.3)
        self.assertEquals(adapted_model.integer, 33)

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

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=ParentREST,
            persistent_model_class=ParentPersistent
        ))

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=ChildREST,
            persistent_model_class=ChildPersistent
        ))

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
        self.assertEquals(adapted_model.child.boolean, False)
        self.assertEquals(adapted_model.child.float, 33.3)
        self.assertEquals(adapted_model.child.integer, 33)
        self.assertEquals(adapted_model.child.string, "string")

    def test_children_of_type_data_type_and_data_collection(self):

        class ChildREST(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

        class ParentREST(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

            child = ChildREST()

        class ChildPersistent(object):

            def __init__(self):
                self.boolean = True
                self.float = 44.4
                self.integer = 44
                self.string = "string2"

        class ParentPersistent(object):

            def __init__(self):
                self.boolean = False
                self.float = 33.3
                self.integer = 33
                self.string = "string1"

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
        attribute_filter.boolean = True
        attribute_filter.float = True
        attribute_filter.integer = True
        attribute_filter.string = True
        attribute_filter.child.boolean = True
        attribute_filter.child.float = True
        attribute_filter.child.integer = True

        self.assertTrue(attribute_filter.boolean)
        self.assertTrue(attribute_filter.float)
        self.assertTrue(attribute_filter.integer)
        self.assertTrue(attribute_filter.string)
        self.assertTrue(attribute_filter.is_attribute_visible("child"))
        self.assertTrue(attribute_filter.child.boolean)
        self.assertTrue(attribute_filter.child.float)
        self.assertTrue(attribute_filter.child.integer)
        self.assertFalse(attribute_filter.child.string)

        persistent_model = ParentPersistent()

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, ParentREST, attribute_filter)
        self.assertEquals(adapted_model.boolean, False)
        self.assertEquals(adapted_model.float, 33.3)
        self.assertEquals(adapted_model.integer, 33)
        self.assertEquals(adapted_model.string, "string1")
        self.assertTrue(isinstance(adapted_model.child, ChildREST))
        self.assertEquals(adapted_model.child.boolean, True)
        self.assertEquals(adapted_model.child.float, 44.4)
        self.assertEquals(adapted_model.child.integer, 44)
        self.assertEquals(adapted_model.child.string, None)

        attribute_filter.child.string = True

        self.assertTrue(attribute_filter.child.string)

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, ParentREST, attribute_filter)
        self.assertEquals(adapted_model.boolean, False)
        self.assertEquals(adapted_model.float, 33.3)
        self.assertEquals(adapted_model.integer, 33)
        self.assertEquals(adapted_model.string, "string1")
        self.assertTrue(isinstance(adapted_model.child, ChildREST))
        self.assertEquals(adapted_model.child.boolean, True)
        self.assertEquals(adapted_model.child.float, 44.4)
        self.assertEquals(adapted_model.child.integer, 44)
        self.assertEquals(adapted_model.child.string, "string2")


class SQLAlchemyDataAdapterAdaptPersistentCollection(unittest.TestCase):

    def test_(self):
        pass
