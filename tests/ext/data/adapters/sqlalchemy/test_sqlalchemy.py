import unittest

from prestans.ext.data import adapters
from prestans.ext.data.adapters import sqlalchemy
from prestans.parser import AttributeFilter
from prestans import types


class RESTModel(types.Model):
    name = types.String()


class PersistentModel(object):

    def __init__(self):
        self.name = "name"


class SQLAlchemyDataAdaptersTest(unittest.TestCase):

    def test_adapt_persistent_instance(self):

        adapters.registry.register_adapter(sqlalchemy.ModelAdapter(
            rest_model_class=RESTModel,
            persistent_model_class=PersistentModel
        ))

        attribute_filter = AttributeFilter.from_model(RESTModel(), False)
        attribute_filter.name = True

        persistent_model = PersistentModel()
        adapted_model = sqlalchemy.adapt_persistent_instance(persistent_model, RESTModel, attribute_filter)
        self.assertEquals(adapted_model.name, "name")

    def test_adapt_persistent_collection(self):
        pass
