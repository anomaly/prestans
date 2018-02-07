import unittest

from prestans.ext.data import adapters
from prestans.ext.data.adapters import sqlalchemy
from prestans.parser import AttributeFilter
from prestans import types


class SQLAlchemyDataAdaptersTest(unittest.TestCase):

    def test_adapt_persistent_instance(self):

        class RESTModel(types.Model):
            boolean = types.Boolean()
            string = types.String()

        class PersistentModel(object):

            def __init__(self):
                self.boolean = False
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
        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModel, attribute_filter)
        self.assertEquals(adapted_model.boolean, False)

    def test_adapt_persistent_instance_single_child_of_type_model(self):

        class RESTModel(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

        class RESTModelWithChild(types.Model):
            sub_model = RESTModel()

        class PersistentModel(object):

            def __init__(self):
                self.boolean = False
                self.float = 33.3
                self.integer = 33
                self.string = "string"

        class PersistentModelWithChild(object):

            @property
            def sub_model(self):
                return PersistentModel()

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=RESTModelWithChild,
            persistent_model_class=PersistentModelWithChild
        ))

        attribute_filter = AttributeFilter.from_model(RESTModelWithChild(), False)
        attribute_filter.sub_model.boolean = True
        attribute_filter.sub_model.float = True
        attribute_filter.sub_model.integer = True
        attribute_filter.sub_model.string = True

        persistent_model = PersistentModelWithChild()

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModelWithChild, attribute_filter)
        self.assertEquals(adapted_model.sub_model.boolean, False)
        self.assertEquals(adapted_model.sub_model.float, 33.3)
        self.assertEquals(adapted_model.sub_model.integer, 33)
        self.assertEquals(adapted_model.sub_model.string, "string")

    @unittest.skip
    def test_adapt_persistent_instance_children_of_all_types(self):

        class RESTModel(types.Model):
            boolean = types.Boolean()
            string = types.String()

        class RESTModelWithChildren(types.Model):
            boolean = types.Boolean()
            float = types.Float()
            integer = types.Integer()
            string = types.String()

            sub_model = RESTModel()

        class PersistentModel(object):

            def __init__(self):
                self.boolean = False
                self.string = "string"

        class PersistentModelWithChildren(object):

            def __init__(self):
                self.boolean = False
                self.float = 33.3
                self.integer = 33
                self.string = "string"

            def sub_model(self):
                return PersistentModel()

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=RESTModelWithChildren,
            persistent_model_class=PersistentModelWithChildren
        ))

        attribute_filter = AttributeFilter.from_model(RESTModelWithChildren(), False)
        attribute_filter.boolean = True
        attribute_filter.float = True
        attribute_filter.integer = True
        attribute_filter.string = True
        # attribute_filter.sub_model.string = True

        persistent_model = PersistentModelWithChildren()

        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModelWithChildren, attribute_filter)
        self.assertEquals(adapted_model.boolean, False)
        self.assertEquals(adapted_model.float, 33.3)
        self.assertEquals(adapted_model.integer, 33)
        self.assertEquals(adapted_model.string, "string")

        self.assertEquals(adapted_model.sub_model.string, "string")

    def test_adapt_persistent_collection(self):
        pass
